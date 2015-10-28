# Python implementation of the MySQL client-server protocol
# http://dev.mysql.com/doc/internals/en/client-server-protocol.html
# Error codes:
# http://dev.mysql.com/doc/refman/5.5/en/error-messages-client.html
from __future__ import print_function
from ._compat import PY2, range_type, text_type, str_type, JYTHON, IRONPYTHON
DEBUG = False

import errno
from functools import partial
import hashlib
import io
import os
import socket
import struct
import sys
import warnings

try:
    import ssl
    SSL_ENABLED = True
except ImportError:
    ssl = None
    SSL_ENABLED = False

if PY2:
    import ConfigParser as configparser
else:
    import configparser

try:
    import getpass
    DEFAULT_USER = getpass.getuser()
    del getpass
except ImportError:
    DEFAULT_USER = None

from tornado import gen, ioloop, iostream

from .charset import MBLENGTH, charset_by_name, charset_by_id
from .cursors import Cursor
from .constants import CLIENT, COMMAND, FIELD_TYPE, SERVER_STATUS
from .util import byte2int, int2byte
from .converters import (
    escape_item, encoders, decoders, escape_string, through)
from .err import (
    raise_mysql_exception, Warning, Error,
    InterfaceError, DataError, DatabaseError, OperationalError,
    IntegrityError, InternalError, NotSupportedError, ProgrammingError)
from . import err

_py_version = sys.version_info[:2]


TEXT_TYPES = set([
    FIELD_TYPE.BIT,
    FIELD_TYPE.BLOB,
    FIELD_TYPE.LONG_BLOB,
    FIELD_TYPE.MEDIUM_BLOB,
    FIELD_TYPE.STRING,
    FIELD_TYPE.TINY_BLOB,
    FIELD_TYPE.VAR_STRING,
    FIELD_TYPE.VARCHAR])

sha_new = partial(hashlib.new, 'sha1')

NULL_COLUMN = 251
UNSIGNED_CHAR_COLUMN = 251
UNSIGNED_SHORT_COLUMN = 252
UNSIGNED_INT24_COLUMN = 253
UNSIGNED_INT64_COLUMN = 254

DEFAULT_CHARSET = 'latin1'

MAX_PACKET_LEN = 2**24-1


def dump_packet(data):
    def is_ascii(data):
        if 65 <= byte2int(data) <= 122:
            if isinstance(data, int):
                return chr(data)
            return data
        return '.'

    try:
        print("packet length:", len(data))
        print("method call[1]:", sys._getframe(1).f_code.co_name)
        print("method call[2]:", sys._getframe(2).f_code.co_name)
        print("method call[3]:", sys._getframe(3).f_code.co_name)
        print("method call[4]:", sys._getframe(4).f_code.co_name)
        print("method call[5]:", sys._getframe(5).f_code.co_name)
        print("-" * 88)
    except ValueError:
        pass
    dump_data = [data[i:i+16] for i in range_type(0, min(len(data), 256), 16)]
    for d in dump_data:
        print(' '.join(map(lambda x: "{:02X}".format(byte2int(x)), d)) +
              '   ' * (16 - len(d)) + ' ' * 2 +
              ' '.join(map(lambda x: "{}".format(is_ascii(x)), d)))
    print("-" * 88)
    print()


def _scramble(password, message):
    if not password:
        return b'\0'
    if DEBUG: print('password=' + password)
    stage1 = sha_new(password).digest()
    stage2 = sha_new(stage1).digest()
    s = sha_new()
    s.update(message)
    s.update(stage2)
    result = s.digest()
    return _my_crypt(result, stage1)


def _my_crypt(message1, message2):
    length = len(message1)
    result = struct.pack('B', length)
    for i in range_type(length):
        x = (struct.unpack('B', message1[i:i+1])[0] ^
             struct.unpack('B', message2[i:i+1])[0])
        result += struct.pack('B', x)
    return result

# old_passwords support ported from libmysql/password.c
SCRAMBLE_LENGTH_323 = 8


class RandStruct_323(object):
    def __init__(self, seed1, seed2):
        self.max_value = 0x3FFFFFFF
        self.seed1 = seed1 % self.max_value
        self.seed2 = seed2 % self.max_value

    def my_rnd(self):
        self.seed1 = (self.seed1 * 3 + self.seed2) % self.max_value
        self.seed2 = (self.seed1 + self.seed2 + 33) % self.max_value
        return float(self.seed1) / float(self.max_value)


def _scramble_323(password, message):
    hash_pass = _hash_password_323(password)
    hash_message = _hash_password_323(message[:SCRAMBLE_LENGTH_323])
    hash_pass_n = struct.unpack(">LL", hash_pass)
    hash_message_n = struct.unpack(">LL", hash_message)

    rand_st = RandStruct_323(hash_pass_n[0] ^ hash_message_n[0],
                             hash_pass_n[1] ^ hash_message_n[1])
    outbuf = io.BytesIO()
    for _ in range_type(min(SCRAMBLE_LENGTH_323, len(message))):
        outbuf.write(int2byte(int(rand_st.my_rnd() * 31) + 64))
    extra = int2byte(int(rand_st.my_rnd() * 31))
    out = outbuf.getvalue()
    outbuf = io.BytesIO()
    for c in out:
        outbuf.write(int2byte(byte2int(c) ^ byte2int(extra)))
    return outbuf.getvalue()


def _hash_password_323(password):
    nr = 1345345333
    add = 7
    nr2 = 0x12345671

    for c in [byte2int(x) for x in password if x not in (' ', '\t')]:
        nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF
        nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
        add= (add + c) & 0xFFFFFFFF

    r1 = nr & ((1 << 31) - 1) # kill sign bits
    r2 = nr2 & ((1 << 31) - 1)

    # pack
    return struct.pack(">LL", r1, r2)


def pack_int24(n):
    return struct.pack('<I', n)[:3]


class MysqlPacket(object):
    """Representation of a MySQL response packet.

    Provides an interface for reading/parsing the packet results.
    """
    __slots__ = ('_position', '_data')

    def __init__(self, data, encoding):
        self._position = 0
        self._data = data

    def get_all_data(self):
        return self._data

    def read(self, size):
        """Read the first 'size' bytes in packet and advance cursor past them."""
        result = self._data[self._position:(self._position+size)]
        if len(result) != size:
            error = ('Result length not requested length:\n'
                     'Expected=%s.  Actual=%s.  Position: %s.  Data Length: %s'
                     % (size, len(result), self._position, len(self._data)))
            if DEBUG:
                print(error)
                self.dump()
            raise AssertionError(error)
        self._position += size
        return result

    def read_all(self):
        """Read all remaining data in the packet.

        (Subsequent read() will return errors.)
        """
        result = self._data[self._position:]
        self._position = None  # ensure no subsequent read()
        return result

    def advance(self, length):
        """Advance the cursor in data buffer 'length' bytes."""
        new_position = self._position + length
        if new_position < 0 or new_position > len(self._data):
            raise Exception('Invalid advance amount (%s) for cursor.  '
                            'Position=%s' % (length, new_position))
        self._position = new_position

    def rewind(self, position=0):
        """Set the position of the data buffer cursor to 'position'."""
        if position < 0 or position > len(self._data):
            raise Exception("Invalid position to rewind cursor to: %s." % position)
        self._position = position

    def get_bytes(self, position, length=1):
        """Get 'length' bytes starting at 'position'.

        Position is start of payload (first four packet header bytes are not
        included) starting at index '0'.

        No error checking is done.  If requesting outside end of buffer
        an empty string (or string shorter than 'length') may be returned!
        """
        return self._data[position:(position+length)]

    if PY2:
        def read_uint8(self):
            result = ord(self._data[self._position])
            self._position += 1
            return result
    else:
        def read_uint8(self):
            result = self._data[self._position]
            self._position += 1
            return result

    def read_uint16(self):
        result = struct.unpack_from('<H', self._data, self._position)[0]
        self._position += 2
        return result

    def read_uint24(self):
        low, high = struct.unpack_from('<HB', self._data, self._position)
        self._position += 3
        return low + (high << 16)

    def read_uint32(self):
        result = struct.unpack_from('<I', self._data, self._position)[0]
        self._position += 4
        return result

    def read_uint64(self):
        result = struct.unpack_from('<Q', self._data, self._position)[0]
        self._position += 8
        return result

    def read_length_encoded_integer(self):
        """Read a 'Length Coded Binary' number from the data buffer.

        Length coded numbers can be anywhere from 1 to 9 bytes depending
        on the value of the first byte.
        """
        c = self.read_uint8()
        if c == NULL_COLUMN:
            return None
        if c < UNSIGNED_CHAR_COLUMN:
            return c
        elif c == UNSIGNED_SHORT_COLUMN:
            return self.read_uint16()
        elif c == UNSIGNED_INT24_COLUMN:
            return self.read_uint24()
        elif c == UNSIGNED_INT64_COLUMN:
            return self.read_uint64()

    def read_length_coded_string(self):
        """Read a 'Length Coded String' from the data buffer.

        A 'Length Coded String' consists first of a length coded
        (unsigned, positive) integer represented in 1-9 bytes followed by
        that many bytes of binary data.  (For example "cat" would be "3cat".)
        """
        length = self.read_length_encoded_integer()
        if length is None:
            return None
        return self.read(length)

    def read_struct(self, fmt):
        s = struct.Struct(fmt)
        result = s.unpack_from(self._data, self._position)
        self._position += s.size
        return result

    def is_ok_packet(self):
        return self._data[0:1] == b'\0'

    def is_eof_packet(self):
        # http://dev.mysql.com/doc/internals/en/generic-response-packets.html#packet-EOF_Packet
        # Caution: \xFE may be LengthEncodedInteger.
        # If \xFE is LengthEncodedInteger header, 8bytes followed.
        return len(self._data) < 9 and self._data[0:1] == b'\xfe'

    def is_resultset_packet(self):
        field_count = ord(self._data[0:1])
        return 1 <= field_count <= 250

    def is_load_local_packet(self):
        return self._data[0:1] == b'\xfb'

    def is_error_packet(self):
        return self._data[0:1] == b'\xff'

    def check_error(self):
        if self.is_error_packet():
            self.rewind()
            self.advance(1)  # field_count == error (we already know that)
            errno = self.read_uint16()
            if DEBUG: print("errno =", errno)
            raise_mysql_exception(self._data)

    def dump(self):
        dump_packet(self._data)


class FieldDescriptorPacket(MysqlPacket):
    """A MysqlPacket that represents a specific column's metadata in the result.

    Parsing is automatically done and the results are exported via public
    attributes on the class such as: db, table_name, name, length, type_code.
    """

    def __init__(self, data, encoding):
        MysqlPacket.__init__(self, data, encoding)
        self.__parse_field_descriptor(encoding)

    def __parse_field_descriptor(self, encoding):
        """Parse the 'Field Descriptor' (Metadata) packet.

        This is compatible with MySQL 4.1+ (not compatible with MySQL 4.0).
        """
        self.catalog = self.read_length_coded_string()
        self.db = self.read_length_coded_string()
        self.table_name = self.read_length_coded_string().decode(encoding)
        self.org_table = self.read_length_coded_string().decode(encoding)
        self.name = self.read_length_coded_string().decode(encoding)
        self.org_name = self.read_length_coded_string().decode(encoding)
        self.charsetnr, self.length, self.type_code, self.flags, self.scale = (
            self.read_struct('<xHIBHBxx'))
        # 'default' is a length coded binary and is still in the buffer?
        # not used for normal result sets...

    def description(self):
        """Provides a 7-item tuple compatible with the Python PEP249 DB Spec."""
        return (
            self.name,
            self.type_code,
            None,  # TODO: display_length; should this be self.length?
            self.get_column_length(),  # 'internal_size'
            self.get_column_length(),  # 'precision'  # TODO: why!?!?
            self.scale,
            self.flags % 2 == 0)

    def get_column_length(self):
        if self.type_code == FIELD_TYPE.VAR_STRING:
            mblen = MBLENGTH.get(self.charsetnr, 1)
            return self.length // mblen
        return self.length

    def __str__(self):
        return ('%s %r.%r.%r, type=%s, flags=%x'
                % (self.__class__, self.db, self.table_name, self.name,
                   self.type_code, self.flags))


class OKPacketWrapper(object):
    """
    OK Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet):
        if not from_packet.is_ok_packet():
            raise ValueError('Cannot create ' + str(self.__class__.__name__) +
                             ' object from invalid packet type')

        self.packet = from_packet
        self.packet.advance(1)

        self.affected_rows = self.packet.read_length_encoded_integer()
        self.insert_id = self.packet.read_length_encoded_integer()
        self.server_status, self.warning_count = self.read_struct('<HH')
        self.message = self.packet.read_all()
        self.has_next = self.server_status & SERVER_STATUS.SERVER_MORE_RESULTS_EXISTS

    def __getattr__(self, key):
        return getattr(self.packet, key)


class EOFPacketWrapper(object):
    """
    EOF Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet):
        if not from_packet.is_eof_packet():
            raise ValueError(
                "Cannot create '{0}' object from invalid packet type".format(
                    self.__class__))

        self.packet = from_packet
        self.warning_count, self.server_status = self.packet.read_struct('<xhh')
        if DEBUG: print("server_status=", self.server_status)
        self.has_next = self.server_status & SERVER_STATUS.SERVER_MORE_RESULTS_EXISTS

    def __getattr__(self, key):
        return getattr(self.packet, key)


class LoadLocalPacketWrapper(object):
    """
    Load Local Packet Wrapper. It uses an existing packet object, and wraps
    around it, exposing useful variables while still providing access
    to the original packet objects variables and methods.
    """

    def __init__(self, from_packet):
        if not from_packet.is_load_local_packet():
            raise ValueError(
                "Cannot create '{0}' object from invalid packet type".format(
                    self.__class__))

        self.packet = from_packet
        self.filename = self.packet.get_all_data()[1:]
        if DEBUG: print("filename=", self.filename)

    def __getattr__(self, key):
        return getattr(self.packet, key)


class Connection(object):
    """
    Representation of a socket with a mysql server.

    The proper way to get an instance of this class is to call
    connect().
    """

    #: :type: tornado.iostream.IOStream
    _stream = None

    def __init__(self, host="localhost", user=None, password="",
                 database=None, port=3306, unix_socket=None,
                 charset='', sql_mode=None,
                 read_default_file=None, conv=decoders, use_unicode=None,
                 client_flag=0, cursorclass=Cursor, init_command=None,
                 connect_timeout=None, ssl=None, read_default_group=None,
                 compress=None, named_pipe=None, no_delay=False,
                 autocommit=False, db=None, passwd=None, local_infile=False,
                 io_loop=None):
        """
        Establish a connection to the MySQL database. Accepts several
        arguments:

        host: Host where the database server is located
        user: Username to log in as
        password: Password to use.
        database: Database to use, None to not use a particular one.
        port: MySQL port to use, default is usually OK.
        unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
        charset: Charset you want to use.
        sql_mode: Default SQL_MODE to use.
        read_default_file:
            Specifies  my.cnf file to read these parameters from under the [client] section.
        conv:
            Decoders dictionary to use instead of the default one.
            This is used to provide custom marshalling of types. See converters.
        use_unicode:
            Whether or not to default to unicode strings.
            This option defaults to true for Py3k.
        client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
        cursorclass: Custom cursor class to use.
        init_command: Initial SQL statement to run when connection is established.
        connect_timeout: Timeout before throwing an exception when connecting.
        ssl:
            A dict of arguments similar to mysql_ssl_set()'s parameters.
            For now the capath and cipher arguments are not supported.
        read_default_group: Group to read from in the configuration file.
        compress; Not supported
        named_pipe: Not supported
        no_delay: Disable Nagle's algorithm on the socket
        autocommit: Autocommit mode. None means use server default. (default: False)
        io_loop: Tornado IOLoop
        local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)

        db: Alias for database. (for compatibility to MySQLdb)
        passwd: Alias for password. (for compatibility to MySQLdb)
        """
        self.io_loop = io_loop or ioloop.IOLoop.current()

        if use_unicode is None and sys.version_info[0] > 2:
            use_unicode = True

        if db is not None and database is None:
            database = db
        if passwd is not None and not password:
            password = passwd

        if compress or named_pipe:
            raise NotImplementedError("compress and named_pipe arguments are not supported")

        if local_infile:
            client_flag |= CLIENT.LOCAL_FILES

        if ssl and ('capath' in ssl or 'cipher' in ssl):
            raise NotImplementedError('ssl options capath and cipher are not supported')

        self.ssl = False
        if ssl:
            if not SSL_ENABLED:
                raise NotImplementedError("ssl module not found")
            self.ssl = True
            client_flag |= CLIENT.SSL
            for k in ('key', 'cert', 'ca'):
                v = None
                if k in ssl:
                    v = ssl[k]
                setattr(self, k, v)

        if read_default_group and not read_default_file:
            if sys.platform.startswith("win"):
                read_default_file = "c:\\my.ini"
            else:
                read_default_file = "/etc/my.cnf"

        if read_default_file:
            if not read_default_group:
                read_default_group = "client"

            cfg = configparser.RawConfigParser()
            cfg.read(os.path.expanduser(read_default_file))

            def _config(key, default):
                try:
                    return cfg.get(read_default_group, key)
                except Exception:
                    return default

            user = _config("user", user)
            password = _config("password", password)
            host = _config("host", host)
            database = _config("database", database)
            unix_socket = _config("socket", unix_socket)
            port = int(_config("port", port))
            charset = _config("default-character-set", charset)

        self.host = host
        self.port = port
        self.user = user or DEFAULT_USER
        self.password = password or ""
        self.db = database
        self.no_delay = no_delay
        self.unix_socket = unix_socket
        if charset:
            self.charset = charset
            self.use_unicode = True
        else:
            self.charset = DEFAULT_CHARSET
            self.use_unicode = False

        if use_unicode is not None:
            self.use_unicode = use_unicode

        self.encoding = charset_by_name(self.charset).encoding

        client_flag |= CLIENT.CAPABILITIES | CLIENT.MULTI_STATEMENTS
        if self.db:
            client_flag |= CLIENT.CONNECT_WITH_DB
        self.client_flag = client_flag

        self.cursorclass = cursorclass
        self.connect_timeout = connect_timeout

        self._result = None
        self._affected_rows = 0
        self.host_info = "Not connected"

        #: specified autocommit mode. None means use server default.
        self.autocommit_mode = autocommit

        self.encoders = encoders  # Need for MySQLdb compatibility.
        self.decoders = conv
        self.sql_mode = sql_mode
        self.init_command = init_command

    def close(self):
        """Close the socket without sending quit message."""
        stream = self._stream
        if stream is None:
            return
        self._stream = None
        stream.close()

    @gen.coroutine
    def close_async(self):
        """Send the quit message and close the socket"""
        if self._stream is None or self._stream.closed():
            self._stream = None
            return
        send_data = struct.pack('<i', 1) + int2byte(COMMAND.COM_QUIT)
        yield self._stream.write(send_data)
        self.close()

    @property
    def open(self):
        return self._stream is not None

    def __del__(self):
        self.close()

    @gen.coroutine
    def autocommit(self, value):
        self.autocommit_mode = bool(value)
        current = self.get_autocommit()
        if value != current:
            yield self._send_autocommit_mode()

    def get_autocommit(self):
        return bool(self.server_status &
                    SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT)

    @gen.coroutine
    def _read_ok_packet(self):
        pkt = yield self._read_packet()
        if not pkt.is_ok_packet():
            raise OperationalError(2014, "Command Out of Sync")
        ok = OKPacketWrapper(pkt)
        self.server_status = ok.server_status
        raise gen.Return(ok)

    @gen.coroutine
    def _send_autocommit_mode(self):
        ''' Set whether or not to commit after every execute() '''
        yield self._execute_command(
            COMMAND.COM_QUERY,
            "SET AUTOCOMMIT = %s" % self.escape(self.autocommit_mode))
        yield self._read_ok_packet()

    @gen.coroutine
    def begin(self):
        """Begin transaction."""
        yield self._execute_command(COMMAND.COM_QUERY, "BEGIN")
        yield self._read_ok_packet()

    @gen.coroutine
    def commit(self):
        ''' Commit changes to stable storage '''
        yield self._execute_command(COMMAND.COM_QUERY, "COMMIT")
        yield self._read_ok_packet()

    @gen.coroutine
    def rollback(self):
        ''' Roll back the current transaction '''
        yield self._execute_command(COMMAND.COM_QUERY, "ROLLBACK")
        yield self._read_ok_packet()

    @gen.coroutine
    def show_warnings(self):
        """SHOW WARNINGS"""
        yield self._execute_command(COMMAND.COM_QUERY, "SHOW WARNINGS")
        result = MySQLResult(self)
        yield result.read()
        raise gen.Return(result.rows)

    @gen.coroutine
    def select_db(self, db):
        '''Set current db'''
        yield self._execute_command(COMMAND.COM_INIT_DB, db)
        yield self._read_ok_packet()

    def escape(self, obj):
        ''' Escape whatever value you pass to it  '''
        if isinstance(obj, str_type):
            return "'" + self.escape_string(obj) + "'"
        return escape_item(obj, self.charset)

    def literal(self, obj):
        '''Alias for escape()'''
        return self.escape(obj)

    def escape_string(self, s):
        if (self.server_status &
                SERVER_STATUS.SERVER_STATUS_NO_BACKSLASH_ESCAPES):
            return s.replace("'", "''")
        return escape_string(s)

    def cursor(self, cursor=None):
        ''' Create a new cursor to execute queries with '''
        if cursor:
            return cursor(self)
        return self.cursorclass(self)

    # The following methods are INTERNAL USE ONLY (called from Cursor)
    @gen.coroutine
    def query(self, sql, unbuffered=False):
        if DEBUG:
            print("DEBUG: sending query:", sql)
        if isinstance(sql, text_type) and not (JYTHON or IRONPYTHON):
            sql = sql.encode(self.encoding)
        yield self._execute_command(COMMAND.COM_QUERY, sql)
        yield self._read_query_result(unbuffered=unbuffered)
        raise gen.Return(self._affected_rows)

    @gen.coroutine
    def next_result(self, unbuffered=False):
        yield self._read_query_result(unbuffered=unbuffered)
        raise gen.Return(self._affected_rows)

    def affected_rows(self):
        return self._affected_rows

    @gen.coroutine
    def kill(self, thread_id):
        arg = struct.pack('<I', thread_id)
        yield self._execute_command(COMMAND.COM_PROCESS_KILL, arg)
        yield self._read_ok_packet()

    @gen.coroutine
    def ping(self, reconnect=True):
        """Check if the server is alive"""
        if self._stream is None:
            if reconnect:
                yield self.connect()
                reconnect = False
            else:
                raise Error("Already closed")
        try:
            yield self._execute_command(COMMAND.COM_PING, "")
            yield self._read_ok_packet()
        except Exception:
            if reconnect:
                yield self.connect()
                yield self.ping(False)
            else:
                raise

    @gen.coroutine
    def set_charset(self, charset):
        # Make sure charset is supported.
        encoding = charset_by_name(charset).encoding
        yield self._execute_command(COMMAND.COM_QUERY, "SET NAMES %s" % self.escape(charset))
        yield self._read_packet()
        self.charset = charset
        self.encoding = encoding

    @gen.coroutine
    def connect(self):
        #TODO: Set close callback
        #raise OperationalError(2006, "MySQL server has gone away (%r)" % (e,))
        sock = None
        try:
            if self.unix_socket and self.host in ('localhost', '127.0.0.1'):
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                addr = self.unix_socket
                self.host_info = "Localhost via UNIX socket: " + self.unix_socket
            else:
                sock = socket.socket()
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                addr = (self.host, self.port)
                self.host_info = "socket %s:%d" % (self.host, self.port)
            stream = iostream.IOStream(sock)
            # TODO: handle connect_timeout
            yield stream.connect(addr)
            self._stream = stream

            if self.no_delay:
                stream.set_nodelay(True)

            yield self._get_server_information()
            yield self._request_authentication()

            self.connected_time = self.io_loop.time()

            if self.sql_mode is not None:
                yield self.query("SET sql_mode=%s" % (self.sql_mode,))

            if self.init_command is not None:
                yield self.query(self.init_command)
                yield self.commit()

            if self.autocommit_mode is not None:
                yield self.autocommit(self.autocommit_mode)
        except BaseException as e:
            if sock is not None:
                try:
                    sock.close()
                except socket.error:
                    pass
            self._stream = None
            if isinstance(e, err.MySQLError):
                raise
            raise OperationalError(
                2003, "Can't connect to MySQL server on %r (%s)" % (self.host, e))

    @gen.coroutine
    def _read_packet(self, packet_type=MysqlPacket):
        """Read an entire "mysql packet" in its entirety from the network
        and return a MysqlPacket type that represents the results.
        """
        buff = b''
        try:
            while True:
                packet_header = yield self._stream.read_bytes(4)
                if DEBUG: dump_packet(packet_header)

                btrl, btrh, packet_number = struct.unpack('<HBB', packet_header)
                bytes_to_read = btrl + (btrh << 16)
                #TODO: check sequence id
                recv_data = yield self._stream.read_bytes(bytes_to_read)
                if DEBUG: dump_packet(recv_data)
                buff += recv_data
                if bytes_to_read < MAX_PACKET_LEN:
                    break
        except iostream.StreamClosedError as e:
            raise OperationalError(2006, "MySQL server has gone away (%s)" % (e,))
        packet = packet_type(buff, self.encoding)
        packet.check_error()
        raise gen.Return(packet)

    def _write_bytes(self, data):
        return self._stream.write(data)

    @gen.coroutine
    def _read_query_result(self, unbuffered=False):
        if unbuffered:
            try:
                result = MySQLResult(self)
                yield result.init_unbuffered_query()
            except:
                result.unbuffered_active = False
                result.connection = None
                raise
        else:
            result = MySQLResult(self)
            yield result.read()
        self._result = result
        self._affected_rows = result.affected_rows
        if result.server_status is not None:
            self.server_status = result.server_status

    def insert_id(self):
        if self._result:
            return self._result.insert_id
        else:
            return 0

    @gen.coroutine
    def _execute_command(self, command, sql):
        if not self._stream:
            raise InterfaceError("(0, 'Not connected')")

        # If the last query was unbuffered, make sure it finishes before
        # sending new commands
        if self._result is not None and self._result.unbuffered_active:
            warnings.warn("Previous unbuffered result was left incomplete")
            yield self._result._finish_unbuffered_query()

        if isinstance(sql, text_type):
            sql = sql.encode(self.encoding)

        chunk_size = min(MAX_PACKET_LEN, len(sql) + 1)  # +1 is for command

        prelude = struct.pack('<iB', chunk_size, command)
        self._write_bytes(prelude + sql[:chunk_size-1])
        if DEBUG: dump_packet(prelude + sql)

        if chunk_size < MAX_PACKET_LEN:
            return

        seq_id = 1
        sql = sql[chunk_size-1:]
        while True:
            chunk_size = min(MAX_PACKET_LEN, len(sql))
            prelude = struct.pack('<i', chunk_size)[:3]
            data = prelude + int2byte(seq_id%256) + sql[:chunk_size]
            self._write_bytes(data)
            if DEBUG: dump_packet(data)
            sql = sql[chunk_size:]
            if not sql and chunk_size < MAX_PACKET_LEN:
                break
            seq_id += 1

    @gen.coroutine
    def _request_authentication(self):
        self.client_flag |= CLIENT.CAPABILITIES
        if self.server_version.startswith('5'):
            self.client_flag |= CLIENT.MULTI_RESULTS

        if self.user is None:
            raise ValueError("Did not specify a username")

        charset_id = charset_by_name(self.charset).id
        if isinstance(self.user, text_type):
            self.user = self.user.encode(self.encoding)

        data_init = struct.pack('<iIB23s', self.client_flag, 1, charset_id, b'')

        next_packet = 1

        if self.ssl:
            data = pack_int24(len(data_init)) + int2byte(next_packet) + data_init
            next_packet += 1

            if DEBUG: dump_packet(data)

            yield self._write_bytes(data)
            yield self._stream.start_tls(
                False,
                {'keyfile': self.key,
                 'certfile': self.cert,
                 'ssl_version': ssl.PROTOCOL_TLSv1,
                 'cert_reqs': ssl.CERT_REQUIRED,
                 'ca_certs': self.ca})

        data = data_init + self.user + b'\0' + \
            _scramble(self.password.encode('latin1'), self.salt)

        if self.db:
            if isinstance(self.db, text_type):
                self.db = self.db.encode(self.encoding)
            data += self.db + int2byte(0)

        data = pack_int24(len(data)) + int2byte(next_packet) + data
        next_packet += 2

        if DEBUG: dump_packet(data)

        self._write_bytes(data)

        auth_packet = yield self._read_packet()

        # if old_passwords is enabled the packet will be 1 byte long and
        # have the octet 254

        if auth_packet.is_eof_packet():
            # send legacy handshake
            data = _scramble_323(self.password.encode('latin1'), self.salt) + b'\0'
            data = pack_int24(len(data)) + int2byte(next_packet) + data
            self._write_bytes(data)
            auth_packet = self._read_packet()

    # _mysql support
    def thread_id(self):
        return self.server_thread_id[0]

    def character_set_name(self):
        return self.charset

    def get_host_info(self):
        return self.host_info

    def get_proto_info(self):
        return self.protocol_version

    @gen.coroutine
    def _get_server_information(self):
        i = 0
        packet = yield self._read_packet()
        data = packet.get_all_data()

        if DEBUG: dump_packet(data)
        self.protocol_version = byte2int(data[i:i+1])
        i += 1

        server_end = data.find(int2byte(0), i)
        self.server_version = data[i:server_end].decode('latin1')
        i = server_end + 1

        self.server_thread_id = struct.unpack('<I', data[i:i+4])
        i += 4

        self.salt = data[i:i+8]
        i += 9  # 8 + 1(filler)

        self.server_capabilities = struct.unpack('<H', data[i:i+2])[0]
        i += 2

        if len(data) >= i + 6:
            lang, stat, cap_h, salt_len = struct.unpack('<BHHB', data[i:i+6])
            i += 6
            self.server_language = lang
            self.server_charset = charset_by_id(lang).name

            self.server_status = stat
            if DEBUG: print("server_status: %x" % stat)

            self.server_capabilities |= cap_h << 16
            if DEBUG: print("salt_len:", salt_len)
            salt_len = max(12, salt_len - 9)

        # reserved
        i += 10

        if len(data) >= i + salt_len:
            # salt_len includes auth_plugin_data_part_1 and filler
            self.salt += data[i:i+salt_len]
        # TODO: AUTH PLUGIN NAME may appeare here.

    def get_server_info(self):
        return self.server_version

    Warning = Warning
    Error = Error
    InterfaceError = InterfaceError
    DatabaseError = DatabaseError
    DataError = DataError
    OperationalError = OperationalError
    IntegrityError = IntegrityError
    InternalError = InternalError
    ProgrammingError = ProgrammingError
    NotSupportedError = NotSupportedError


class MySQLResult(object):

    def __init__(self, connection):
        self.connection = connection
        self.affected_rows = None
        self.insert_id = None
        self.server_status = None
        self.warning_count = 0
        self.message = None
        self.field_count = 0
        self.description = None
        self.rows = None
        self.has_next = None
        self.unbuffered_active = False

    @gen.coroutine
    def read(self):
        try:
            first_packet = yield self.connection._read_packet()

            if first_packet.is_ok_packet():
                self._read_ok_packet(first_packet)
            elif first_packet.is_load_local_packet():
                self._read_load_local_packet(first_packet)
            else:
                yield self._read_result_packet(first_packet)
        finally:
            self.connection = None

    @gen.coroutine
    def init_unbuffered_query(self):
        self.unbuffered_active = True
        first_packet = yield self.connection._read_packet()

        if first_packet.is_ok_packet():
            self._read_ok_packet(first_packet)
            self.unbuffered_active = False
            self.connection = None
        else:
            self.field_count = first_packet.read_length_encoded_integer()
            yield self._get_descriptions()

            # Apparently, MySQLdb picks this number because it's the maximum
            # value of a 64bit unsigned integer. Since we're emulating MySQLdb,
            # we set it to this instead of None, which would be preferred.
            self.affected_rows = 18446744073709551615

    def _read_ok_packet(self, first_packet):
        ok_packet = OKPacketWrapper(first_packet)
        self.affected_rows = ok_packet.affected_rows
        self.insert_id = ok_packet.insert_id
        self.server_status = ok_packet.server_status
        self.warning_count = ok_packet.warning_count
        self.message = ok_packet.message
        self.has_next = ok_packet.has_next

    def _read_load_local_packet(self, first_packet):
        load_packet = LoadLocalPacketWrapper(first_packet)
        sender = LoadLocalFile(load_packet.filename, self.connection)
        sender.send_data()

        ok_packet = self.connection._read_packet()
        if not ok_packet.is_ok_packet():
            raise OperationalError(2014, "Commands Out of Sync")
        self._read_ok_packet(ok_packet)

    def _check_packet_is_eof(self, packet):
        if packet.is_eof_packet():
            eof_packet = EOFPacketWrapper(packet)
            self.warning_count = eof_packet.warning_count
            self.has_next = eof_packet.has_next
            return True
        return False

    @gen.coroutine
    def _read_result_packet(self, first_packet):
        self.field_count = first_packet.read_length_encoded_integer()
        yield self._get_descriptions()
        yield self._read_rowdata_packet()

    @gen.coroutine
    def _read_rowdata_packet_unbuffered(self):
        # Check if in an active query
        if not self.unbuffered_active:
            raise gen.Return()

        packet = yield self.connection._read_packet()
        if self._check_packet_is_eof(packet):
            self.unbuffered_active = False
            self.connection = None
            self.rows = None
            raise gen.Return()

        row = self._read_row_from_packet(packet)
        self.affected_rows = 1
        self.rows = (row,)  # rows should tuple of row for MySQL-python compatibility.
        raise gen.Return(row)

    @gen.coroutine
    def _finish_unbuffered_query(self):
        # After much reading on the MySQL protocol, it appears that there is,
        # in fact, no way to stop MySQL from sending all the data after
        # executing a query, so we just spin, and wait for an EOF packet.
        while self.unbuffered_active:
            packet = yield self.connection._read_packet()
            if self._check_packet_is_eof(packet):
                self.unbuffered_active = False
                self.connection = None  # release reference to kill cyclic reference.

    @gen.coroutine
    def _read_rowdata_packet(self):
        """Read a rowdata packet for each data row in the result set."""
        rows = []
        while True:
            packet = yield self.connection._read_packet()
            if self._check_packet_is_eof(packet):
                self.connection = None  # release reference to kill cyclic reference.
                break
            rows.append(self._read_row_from_packet(packet))

        self.affected_rows = len(rows)
        self.rows = tuple(rows)

    def _read_row_from_packet(self, packet):
        row = []
        for encoding, converter in self.converters:
            data = packet.read_length_coded_string()
            if data is not None:
                if encoding is not None:
                    data = data.decode(encoding)
                if DEBUG: print("DEBUG: DATA = ", data)
                if converter is not None:
                    data = converter(data)
            row.append(data)
        return tuple(row)

    @gen.coroutine
    def _get_descriptions(self):
        """Read a column descriptor packet for each column in the result."""
        self.fields = []
        self.converters = []
        use_unicode = self.connection.use_unicode
        description = []
        for i in range_type(self.field_count):
            field = yield self.connection._read_packet(FieldDescriptorPacket)
            self.fields.append(field)
            description.append(field.description())
            field_type = field.type_code
            if use_unicode:
                if field_type in TEXT_TYPES:
                    charset = charset_by_id(field.charsetnr)
                    if charset.is_binary:
                        # TEXTs with charset=binary means BINARY types.
                        encoding = None
                    else:
                        encoding = charset.encoding
                else:
                    encoding = 'ascii'
            else:
                encoding = None
            converter = self.connection.decoders.get(field_type)
            if converter is through:
                converter = None
            if DEBUG: print("DEBUG: field={}, converter={}".format(field, converter))
            self.converters.append((encoding, converter))

        eof_packet = yield self.connection._read_packet()
        assert eof_packet.is_eof_packet(), 'Protocol error, expecting EOF'
        self.description = tuple(description)


class LoadLocalFile(object):
    def __init__(self, filename, connection):
        self.filename = filename
        self.connection = connection

    def send_data(self):
        """Send data packets from the local file to the server"""
        if not self.connection.socket:
            raise InterfaceError("(0, '')")

        # sequence id is 2 as we already sent a query packet
        seq_id = 2
        try:
            with open(self.filename, 'rb') as open_file:
                chunk_size = MAX_PACKET_LEN
                prelude = b""
                packet = b""
                packet_size = 0

                while True:
                    chunk = open_file.read(chunk_size)
                    if not chunk:
                        break
                    packet = struct.pack('<i', len(chunk))[:3] + int2byte(seq_id)
                    format_str = '!{0}s'.format(len(chunk))
                    packet += struct.pack(format_str, chunk)
                    self.connection._write_bytes(packet)
                    seq_id += 1
        except IOError:
            raise OperationalError(1017, "Can't find file '{0}'".format(self.filename))
        finally:
            # send the empty packet to signify we are done sending data
            packet = struct.pack('<i', 0)[:3] + int2byte(seq_id)
            self.connection._write_bytes(packet)

# g:khuno_ignore='E226,E301,E701'
