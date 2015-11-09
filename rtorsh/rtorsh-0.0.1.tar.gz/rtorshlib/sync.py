import sqlite3


class Synchronizer:
    def __init__(self, dbfile, rtorrent, rfs, verbose=False):
        self.verbose = verbose
        self._dbfile = dbfile
        self._rtorrent = rtorrent
        self._rfs = rfs
        self._db = sqlite3.connect(self._dbfile)
        self._cur = self._db.cursor()
        self._cur.execute('CREATE TABLE IF NOT EXISTS torrent_sync (hash text, done bool)')

    def is_synced(self, tor_hash):
        self._cur.execute('SELECT done FROM torrent_sync WHERE done=True AND hash=?', tor_hash)
        return self._cur.fetchone()

    def sync_torrent(self, tor_hash, sync_dir):
        if not self.is_synced(tor_hash):
            tor_dir = self._rtorrent.get_directory(tor_hash)
            self._rfs.get(tor_dir, sync_dir)
        elif self.verbose:
            print("Torrent already synced.")
        return
