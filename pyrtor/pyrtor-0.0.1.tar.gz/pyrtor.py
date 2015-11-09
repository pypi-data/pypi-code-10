import xmlrpc.client
import time


class XmlrpcException(Exception):
    def __init__(self, message, raw_out):
        super(XmlrpcException, self).__init__(message)
        self.raw_out = raw_out


class Cache:
    """Very basic caching implementation for RtorrentServer and Torrent

    This could become memory intensive for commands operating on a large range of torrents.
    It currently does not write to disk, and caches solely in memory.
    """

    def __init__(self, cache_time=-1):
        """Just initializes attributes.

        Args:
            cache_time (int): The time (in seconds) to cache results.
        """

        self.cache = {}
        self.cache_time = cache_time
        self.hit_count = 0
        self.miss_count = 0
        self.writes = 0
        self.reads = 0

    def get_key(self, tor_hash, field):
        """Fetches a value from the cache.

        Args:
            hash (str): The hash of the torrent whose field you want to fetch.
            field (str): The field you want to fetch (i.e. name).
        """

        self.reads += 1
        if tor_hash in self.cache:
            if field in self.cache[tor_hash]:
                if time.time() - self.cache[tor_hash][field][1] < self.cache_time:
                    self.hit_count += 1
                    return self.cache[tor_hash][field][0]
        self.miss_count += 1
        return None

    def set_key(self, tor_hash, field, value):
        """Sets a value in the cache.

        Args:
            hash (str): The hash of the torrent whose field you want to set.
            field (str): The field you want to set (i.e. name).
            value (str): The value to set for the field.
        """

        self.writes += 1
        if hash not in self.cache:
            self.cache[tor_hash] = {}
        self.cache[tor_hash][field] = (value, time.time())

    def clean_cache(self):
        """Removes all entries older than the instances cache_time."""

        for tor_hash, torrent in self.cache.items():
            for field, val_tuple in self.cache[tor_hash]:
                if val_tuple[1] - time.time() > self.cache_time:
                    self.cache[tor_hash].pop(field, None)

    def empty_cache(self):
        """Removes all of the entries from the cache."""

        self.cache = {}


class RtorrentServer:
    """Represents a connection to the Rtorrent Server

    Attributes:
        client (xmlrpc.client.ServerProxy): The XMLRPC connection to make direct XMLRPC calls.

    Note:
        Changing the url, username or password attributes will not change active connections.
    """

    def __init__(self, url, username, password, cache_time=-1):
        """Sets attributes, initiates the connection to Rtorrent, and initializes the cache.

        Args:
            url (str): The URL to the rtorrent XMLRPC endpoint (i.e. https://my.server.come/xmlrpc).
            username (str): The username to use to connect to rtorrent.
            password (str): The password to use to connect to rtorrent.
            cache_time (int): The time to cache XMLRPC results in seconds, passed to ``Cache``.
        """

        self.url = url
        self.username = username
        self.password = password
        self._login()
        self.cache = Cache(cache_time)

    def _login(self):
        """Initializes the client attribute with an XMLRPC client connection."""

        if self.url.find("http://") == 0:
            full_url = "http://{}:{}@{}".format(self.username,
                                                self.password, self.url[7:])
        if self.url.find("https://") == 0:
            full_url = "https://{}:{}@{}".format(self.username,
                                                 self.password, self.url[8:])
        else:
            raise Exception("URL does not start with http:// or https://")
        self.client = xmlrpc.client.ServerProxy(full_url)

    def seeding(self):
        """Retrieves the torrents in the seeding state.

        Returns:
            A list of Torrent objects.
        """

        ret_list = []
        for tor in self.client.d.multicall("seeding", "d.get_hash="):
            ret_list.append(Torrent(self.client, ''.join(tor), self.cache))
        return ret_list

    def multi(self, view, fields):
        field_map = {
            "hash": "d.get_hash=",
            "name": "d.get_name=",
            "label": "d.get_custom1=",
        }
        ret_list = []
        mapped_list = []
        for val in fields:
            mapped_list.append(field_map[val])
        ind = fields.index('hash')
        for tor in self.client.d.multicall(view, *mapped_list):
            tor_dict = {}
            for i in range(len(fields)):
                if "hash" in fields:
                    if fields[i] == "hash":
                        pass
                    else:
                        self.cache.set_key(tor[ind], fields[i], tor[i])
                tor_dict[fields[i]] = tor[i]
            ret_list.append(tor_dict)
        return ret_list

    def get_torrent(self, tor_hash):
        """Gets a torrent by its hash.

        Note:
            This does not check if the specified hash is valid.

        Args:
            hash (str): The hash of the torrent to initiate.

        Returns:
            A Torrent object representing the selected hash.
        """

        return Torrent(self.client, tor_hash, self.cache)

    def load(self, tor_content, start=True):
        """Adds a torrent to rtorrent.

        Args:
            torContent (str): The contents of the .torrent file you want to add.
            start (bool): Automatically starts the torrent after adding it if True.
        """
        if start:
            self.client.load_raw_start(tor_content)
        else:
            self.client.load_raw(tor_content)


class Torrent:
    """Represents a torrent on the rtorrent server."""
    def __init__(self, client, tor_hash, cache=None):
        """Just initializes the class attributes.

        Args:
            client (xmlrpc.client.ServerProxy): XMLRPC connection passed from parent.
            hash (str): The hash of the torrent this instance should represent.
            cache (Cache): Passed down instance of the Cache object.
        """

        self.client = client
        self._tor_hash = tor_hash
        self.cache = cache

    @property
    def name(self):
        """Gets the name of the torrent.

        Returns:
            A string for the name of the torrent.
        """

        tname = None
        if self.cache is not None:
            tname = self.cache.get_key(self._tor_hash, "name")
        if tname is None:
            tname = self.client.d.get_name(self._tor_hash)
            if self.cache is not None:
                self.cache.set_key(self._tor_hash, "name", tname)
        return tname

    @property
    def label(self):
        """Gets a torrent's label.

        Returns:
            The label of the torrent as a string.
        """

        tlabel = None
        if self.cache is not None:
            tlabel = self.cache.get_key(self._tor_hash, "label")
        if tlabel is None:
            tlabel = self.client.d.get_custom1(self._tor_hash)
            if self.cache is not None:
                self.cache.set_key(self._tor_hash, "label", tlabel)
        return tlabel

    @label.setter
    def label(self, label):
        """Sets a torrent's label.

        Args:
            label (str): The new label to set for the torrent.
        """

        self.client.d.set_custom1(self._tor_hash, label)
        if self.cache is not None:
            self.cache.set_key(self._tor_hash, "label", label)

    @property
    def message(self):
        """Gets the message for a torrent, such as 'Tracker unavailable'.

        Returns:
            The message for the torrent as a string.
        """

        tmess = None
        if self.cache is not None:
            tmess = self.cache.get_key(self._tor_hash, "message")
        if tmess is None:
            tmess = self.client.d.get_message(self._tor_hash)
            if self.cache is not None:
                self.cache.set_key(self._tor_hash, "message", tmess)
        return tmess

    @message.setter
    def message(self, message):
        self.client.d.set_message(self._tor_hash, message)
        if self.cache is not None:
            self.cache.set_key(self._tor_hash, "message", message)

    def pause(self):
        """Pauses the torrent."""

        self.client.d.pause(self._tor_hash)

    def resume(self):
        """Resumes the torrent."""

        self.client.d.resume(self._tor_hash)

    def stop(self):
        """Stops the torrent."""

        self.client.d.stop(self._tor_hash)

    def start(self):
        """Starts the torrent."""

        self.client.d.start(self._tor_hash)

    def is_complete(self):
        """Checks whether the torrent is complete.

        Returns:
            True if torrent is complete, False otherwise.
        """

        ret = self.client.d.complete(self._tor_hash)
        if ret == 1:
            return True
        return False

    def size_bytes(self):
        """Checks the size of a torrent (not the currently downloaded portion).

        Returns:
            int - Size of the torrent in bytes.
        """

        tsize = None
        if self.cache is not None:
            tsize = self.cache.get_key(self._tor_hash, "size_bytes")
        if tsize is None:
            tsize = self.client.d.get_size_bytes(self._tor_hash)
            if self.cache is not None:
                self.cache.set_key(self._tor_hash, "size_bytes", tsize)
        return tsize

    def completed_bytes(self):
        """Checks the number of completed bytes.

        Returns:
            int - The number of bytes downloaded.
        """

        return self.client.d.get_completed_bytes(self._tor_hash)

    def get_ratio(self):
        """Checks the ration of a torrent.

        Returns:
            float - The ratio as a whole number (e.g. 1 for a 1:1 ratio, .5 for a 1:2 ratio)
        """

        return self.client.d.get_ratio(self._tor_hash)/1000

    def base_path(self):
        return self.client.d.get_base_path(self._tor_hash)

    def directory(self):
        return self.client.d.get_directory(self._tor_hash)

    def set_directory(self, directory):
        self.client.d.set_directory(self._tor_hash, directory)
        self.client.d.set_directory_base(self._tor_hash, directory)

    def recheck(self):
        """Forces a rehash of the torrent."""

        self.client.d.check_hash(self._tor_hash)
