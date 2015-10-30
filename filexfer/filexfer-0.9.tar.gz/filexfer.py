
import struct, datetime, sys

__author__ = 'wiml@omnigroup.com'
__version__ = '$Header: svn+ssh://source.omnigroup.com/Source/svn/Omni/trunk/OmniGroup/Scripts/pythonlib/filexfer.py 143689 2011-01-27 06:58:29Z wiml $'
__docformat__ = 'reStructuredText en'
__all__ = [ 'filexfer', 'sftp_popen' ]

class filexfer (object):
    """The filexfer class implements (part of) the client side of the protocol described
    in draft-ietf-secsh-filexfer-02.txt, which is the communication protocol between an
    sftp client and an sftp server process."""
    
    FXP_INIT            =    1
    FXP_VERSION         =    2
    FXP_OPEN            =    3
    FXP_CLOSE           =    4
    FXP_READ            =    5
    FXP_WRITE           =    6
    FXP_LSTAT           =    7
    FXP_FSTAT           =    8
    FXP_SETSTAT         =    9
    FXP_FSETSTAT        =   10
    FXP_OPENDIR         =   11
    FXP_READDIR         =   12
    FXP_REMOVE          =   13
    FXP_MKDIR           =   14
    FXP_RMDIR           =   15
    FXP_REALPATH        =   16
    FXP_STAT            =   17
    FXP_RENAME          =   18
    FXP_READLINK        =   19
    FXP_SYMLINK         =   20
    FXP_STATUS          =  101
    FXP_HANDLE          =  102
    FXP_DATA            =  103
    FXP_NAME            =  104
    FXP_ATTRS           =  105
    FXP_EXTENDED        =  200
    FXP_EXTENDED_REPLY  =  201

    FXF_READ       =     0x00000001
    FXF_WRITE      =     0x00000002
    FXF_APPEND     =     0x00000004
    FXF_CREAT      =     0x00000008
    FXF_TRUNC      =     0x00000010
    FXF_EXCL       =     0x00000020

    FX_OK                        =    0
    FX_EOF                       =    1
    FX_NO_SUCH_FILE              =    2
    FX_PERMISSION_DENIED         =    3
    FX_FAILURE                   =    4
    FX_BAD_MESSAGE               =    5
    FX_NO_CONNECTION             =    6
    FX_CONNECTION_LOST           =    7
    FX_OP_UNSUPPORTED            =    8
    
    protocol_version = 3

    def __init__(self, rpipe, wpipe, proc=None):
        """Creates a new filexfer instance. rpipe and wpipe should be file objects
        for communicating with the server process. proc is an optional argument
        which is expected to be an instance of subprocess.Popen.

        Before any other requests are made, the protocol requires that you
        invoke the `do_setup` method exactly once.
        """
        self.proc = proc
        self.rpipe = rpipe
        self.wpipe = wpipe
        self.reading = None
        self.next_xid = 1
        self.outstanding_requests = { }
        self.completed_requests = { }
        self.trace = 0

    def __del__(self):
        if self.trace > 1:
            print 'del(' + repr(self) + ')'
        if self.rpipe is not None:
            self.shutdown()

    def shutdown(self):
        """Closes and unreferences the communication pipes."""
        if self.trace:
            print repr(self), 'Shutting down.'
        self.flush()
        if self.wpipe:
            if self.trace > 1:
                print repr(self), 'Closing write pipe', repr(self.wpipe)
            self.wpipe.close()
        if self.rpipe and self.rpipe is not self.wpipe:
            if self.trace > 1:
                print repr(self), 'Closing read pipe', repr(self.rpipe)
            self.rpipe.close()
        self.wpipe = None
        self.rpipe = None
        if self.trace:
            print repr(self), 'Waiting for subproc to exit'
        if self.proc:
            self.proc.wait()
        if self.trace:
            print repr(self), 'Done shutting down'

    def flush(self):
        if self.trace:
            print repr(self), 'outstanding:', self.outstanding_requests
            print repr(self), 'completed:', self.completed_requests
        while self.outstanding_requests:
            self.wpipe.flush()
            self._get_response()

    def _send(self, cmd, data):
        hdr = struct.pack('>IB', 1 + len(data), cmd)
        self.wpipe.write(hdr)
        self.wpipe.write(data)
        if self.trace > 2:
            print 'wrote:', repr(hdr+data)

    def _recv(self, required_pkttype=None):
        assert self.reading is None
        if self.trace > 2:
            print repr(self), 'Reading...'
        pkt_header = self.rpipe.read(5)
        if self.trace > 1:
            print ' got', len(pkt_header), 'bytes'
        if pkt_header == '':
            raise EOFError()
        pktlen, pkttype = struct.unpack('>IB', pkt_header)
        if required_pkttype is not None and pkttype not in required_pkttype:
                raise AssertionError( ('Got pkttype %d, needed pkttype %s' % (pkttype, required_pkttype)) )
        self.reading = pktlen - 1
        return pkttype

    def read_done(self, trailing=False):
        """Indicates that the filexfer instance has finished reading a result packet
        received by _recv(). If this violates the protocol, raises an exception. If
        trailing is True, then unread data in this packet is discarded."""
        assert self.reading is not None
        if self.reading == 0:
            self.reading = None
            return
        if not trailing:
            raise AssertionError( ('Packet buffer still contains %d bytes' % self.reading) )
        self.rpipe.read(self.reading)
        self.reading = None
        
    def read_more(self):
        """Return True if there is more data to be read from the current response packet."""
        assert self.reading is not None
        if self.reading == 0:
            return False
        return True

    def read_bytes(self, nbytes):
        """Read and return the indicated number of bytes from the current response packet."""
        assert self.reading is not None
        if self.reading < nbytes:
            raise EOFError('packet underflow: %d bytes requested but only %d remaining' % (nbytes, self.reading))
        if nbytes == 0:
            return ''
        buf = self.rpipe.read(nbytes)
        if buf == '':
            raise EOFError()
        if self.trace > 1:
            print 'read_bytes(%d) -> %d bytes; %d remain' % ( nbytes, len(buf), self.reading )
        self.reading -= len(buf)
        return buf

    def read_uint32(self):
        """Read and return a uint32 as a Python int."""
        (val,) = struct.unpack('>I', self.read_bytes(4))
        return val
    def read_string(self):
        """Read and return a string as a Python string object."""
        slen = self.read_uint32()
        return self.read_bytes(slen)
    def read_uint64(self):
        """Read and return a uint64 as a Python int (or long)."""
        (h, l) = struct.unpack('>II', self.read_bytes(8))
        if h == 0:
            return l
        else:
            return ( h  <<  32 ) | l
        
    def do_setup(self, extensions=None):
        """Send the initial INIT request and parses the VERSION response.
        The `server_version` and `server_extensions` attributes are set from
        the contents of the VERSION response, but are not otherwise acted upon.

        The `extensions` argument may be either a dictionary or a list of (name, value)
        pairs to be sent to the server in the INIT request.
        """
        buf = struct.pack('>I', self.protocol_version)
        if extensions:
            exts = [ ]
            if hasattr(extensions, 'items'):
                kv = extensions.items()
            else:
                kv = extensions
            for k, v in kv:
                assert type(k) == str
                exts.append(k)
                assert type(v) == str
                exts.append(v)
            for s in exts:
                buf += pack('>I', len(s)) + s
        self._send(self.FXP_INIT, buf)
        self.wpipe.flush()
        self._recv( (self.FXP_VERSION,) )
        self.server_version = self.read_uint32()
        self.server_extensions = { }
        while self.read_more():
            extname = self.read_string()
            extvalue = self.read_string()
            self.server_extensions[extname] = extvalue
        self.read_done()

    def _alloc_xid(self, handler):
        xid = self.next_xid
        self.next_xid = xid + 1
        self.outstanding_requests[xid] = handler
        return xid

    def _send_cmd(self, cmd, body, handler):
        xid = self._alloc_xid(handler)
        self._send(cmd, struct.pack('>I', xid) + body )
        return xid

    def _get_response(self):
        pkttype = self._recv( (self.FXP_STATUS,
                               self.FXP_HANDLE,
                               self.FXP_DATA,
                               self.FXP_NAME,
                               self.FXP_ATTRS) )
        xid = self.read_uint32()
        handler = self.outstanding_requests[xid]
        del self.outstanding_requests[xid]
        if self.trace > 1:
            print 'xid %d: resp %d -> handler %s' % ( xid, pkttype, handler )
        try:
            rvalue = handler(self, pkttype)
        except Exception:
            self.completed_requests[xid] = ( None, sys.exc_info() )
            self.read_done(True)
        else:
            self.read_done(False)
            if rvalue is not None:
                self.completed_requests[xid] = rvalue

    def _complete_xid(self, xid):
        while 1:
            while xid not in self.completed_requests:
                assert(xid in self.outstanding_requests)
                self.wpipe.flush()
                self._get_response()
            ( done, result ) = self.completed_requests[xid]
            del self.completed_requests[xid]
            if done is None:
                ( exc_type, exc_value, exc_tb ) = result
                raise exc_type, exc_value, exc_tb
            elif done:
                return result
            else:
                xid = result

    def read_status_tail(self):
        code = self.read_uint32()
        message = self.read_string()
        lang = self.read_string()
        return ( code, message, lang )

    def read_attrs(self):
        """Read an attribute structure from the current response packet and return it.
        The returned value is a dictionary with any (or none) of the following keys:

        size : integer
            The file's size
        uid, gid : integer
            The file's user and group id, as reported by the server
        permissions : integer
            The file's permissions, in POSIX numeric form
        atime, mtime : datetime
            The file's access and modification times
        ext : dictionary
            Any extended information returned by the server
        """
        flags = self.read_uint32()
        attrs = { }
        if flags & 1: # ATTR_SIZE
            attrs['size'] = self.read_uint64()
        if flags & 2: # ATTR_UIDGID
            attrs['uid'] = self.read_uint32()
            attrs['gid'] = self.read_uint32()
        if flags & 4: # ATTR_PERMISSIONS
            attrs['permissions'] = self.read_uint32()
        if flags & 8: # ATTR_ACMODTIME
            atime = self.read_uint32()
            mtime = self.read_uint32()
            attrs['atime'] = datetime.datetime.utcfromtimestamp(atime)
            attrs['mtime'] = datetime.datetime.utcfromtimestamp(mtime)
        if flags & 0x80000000: # ATTR_EXTENDED
            extnum = self.read_uint32()
            extends = { }
            attrs['ext'] = extends
            while extnum > 0:
                stype = self.read_string()
                svalue = self.read_string()
                extends[stype] = svalue
                extnum -= 1
        return attrs

    def do_listdir(self, dirname):
        """List the contents of `dirname`, returning an iterator.

        `dirname` is a string to be interpreted by the sftp server.

        The objects produced by the iterator are dictionaries of information
        about the entry: `filename`, `longname`, and the file's attributes.
        """

        xid = self._alloc_xid(self.DirHandle().did_opendir)
        self._send(self.FXP_OPENDIR, struct.pack('>II', xid, len(dirname)) + dirname)
        return self._complete_xid(xid)


    class Error (EnvironmentError):
        """Error class for filexfer errors other than EOF."""
        pass
    
    def _to_exception(self, code, msg, lang=None):
        if code == self.FX_OK:
            return None
        if code == self.FX_EOF:
            return EOFError(msg)
        return self.Error(code, msg)
                                                
    class Handle (object):
        """Base class for filexfer file and directory handles."""
        
        sftp = None
        xid = None
        hdl = None

        def close(self):
            """Close the file handle. This is a convenience method for closing a
            file handle without doing anything with the result/status of the request."""
            assert self.xid is None
            xid = self.sftp._alloc_xid(lambda x, y: x.read_status_tail() and None)
            self.sftp._send(self.sftp.FXP_CLOSE, struct.pack('>II', xid, len(self.hdl)) + self.hdl)
            self.hdl = None
            self.sftp = None

#        def __del__(self):
#            print 'del(' + repr(self) + ')',
#            if self.hdl is not None and self.sftp is not None:
#                print ' hdl', repr(self.hdl), ' conn', repr(self.sftp)
#                self.close()
#            else:
#                print

    class DirHandle (Handle):
        """Iterator class for enumerating the contents of a directory."""
            
        def did_opendir(self, sftp, pkttype):
            self.entries = [ ]
            if pkttype == sftp.FXP_STATUS:
                csl = sftp.read_status_tail()
                if csl[0] in ( sftp.FX_OK, sftp.FX_EOF ):
                    return ( True, self )
                raise sftp._to_exception(*csl)
            elif pkttype == sftp.FXP_HANDLE:
                self.sftp = sftp
                self.hdl = sftp.read_string()
                self.readdir()
                return ( True, self )

        def readdir(self):
            assert self.xid is None
            self.xid = self.sftp._send_cmd(filexfer.FXP_READDIR, struct.pack('>I', len(self.hdl)) + self.hdl, self.did_readdir)

        def __iter__(self):
            return self
        
        def next(self):
            while not self.entries:
                if self.xid is None:
                    if self.sftp is None or self.hdl is None:
                        raise StopIteration
                    self.readdir()
                self.sftp._complete_xid(self.xid)
            return self.entries.pop(0)

        def did_readdir(self, sftp, pkttype):
            assert self.xid is not None
            self.xid = None
            if pkttype == sftp.FXP_STATUS:
                csl = sftp.read_status_tail()
                self.close()
                self.hdl = None
                self.sftp = None
                if csl[0] in ( sftp.FX_OK, sftp.FX_EOF ):
                    return ( True, None )
                raise sftp._to_exception(*csl)
            elif pkttype == sftp.FXP_NAME:
                num = sftp.read_uint32()
                while num > 0:
                    fn1 = sftp.read_string()
                    fn2 = sftp.read_string()
                    attrs = sftp.read_attrs()
                    entry = { 'filename' : fn1, 'longname' : fn2 }
                    entry.update(attrs)
                    self.entries.append(entry)
                    num -= 1
                return ( True, None )

    class FileHandle (Handle):
        def did_openfile(self, sftp, pkttype):
            if pkttype == sftp.FXP_STATUS:
                csl = sftp.read_status_tail()
                raise sftp._to_exception(*csl)
            elif pkttype == sftp.FXP_HANDLE:
                self.sftp = sftp
                self.hdl = sftp.read_string()
                return ( True, self )

        def blocks(self, start=0, blocksize=65536, readahead=True):
            pos = start
            xid = self._readblock(pos, blocksize)
            while 1:
                try:
                    blob = self.sftp._complete_xid(xid)
                except EOFError:
                    return
                pos += len(blob)
                if readahead:
                    xid = self._readblock(pos, blocksize)
                    self.sftp.wpipe.flush()
                    yield blob
                else:
                    yield blob
                    xid = self._readblock(pos, blocksize)

        def _readblock(self, pos, blocksize):
            cmd = struct.pack('>I', len(self.hdl)) + self.hdl + \
                  struct.pack('>III', 0, pos, blocksize)
            return self.sftp._send_cmd(self.sftp.FXP_READ,
                                       cmd,
                                       self.did_readblock)
            
        def did_readblock(self, sftp, pkttype):
            if pkttype == sftp.FXP_STATUS:
                csl = sftp.read_status_tail()
                raise sftp._to_exception(*csl)
            elif pkttype == sftp.FXP_DATA:
                blob = sftp.read_string()
                return ( True, blob )

    def do_openfile(self, pathname):
        """Open the file at `pathname`, returning a FileHandle instance.
        The FileHandle can act as an iterator which will return chunks of the
        file as strings."""
        
        cmd = struct.pack('>I', len(pathname)) + pathname + struct.pack('>II', self.FXF_READ, 0)
        fh = self.FileHandle()
        return self._complete_xid(self._send_cmd(self.FXP_OPEN, cmd, fh.did_openfile))

def sftp_popen(hostname, sshopts=( '-a', '-C' )):
    """Create a connection to an sftp server by spawning an ssh process with the
    `subprocess` module, and return the resulting `filexfer` instance.
    """
    import subprocess

    # Garbage collection seems to interact badly with the subprocess module,
    # I'm not sure why. Maybe my __del__ methods get called at an inconvenient
    # time in the forked child, or something.
    import gc
    gc.collect()

    cmd = ( 'ssh', '-o', 'BatchMode yes' ) + sshopts + ( '-s', hostname, 'sftp' )
    pope = subprocess.Popen( cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             bufsize=-1 )
    sftp = filexfer(pope.stdout, pope.stdin, pope)
    sftp.do_setup()
    return sftp

