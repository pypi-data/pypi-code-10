"""rtorsh - CLI to rtorrent's XMLRPC interface.

Please file any bug reports on the project's Github page.
"""

try:
    import tabulate
    IMP_TABULATE = True
except ImportError:
    IMP_TABULATE = False

import argparse
import configparser
import pyrtor
import rtorshlib.remotefs
import sys
import os.path


class RtorrentShell:
    """Not a shell, but it is called from a shell.

    This is mostly a wrapper around the pyrtor library to expose it's features through bash.
    """

    def __init__(self, URL, user, password):
        """Builds the parser for rtorsh and initializes features.

        Args:
            URL (str): The URL to rtorrent (including http:// or https://)
            user (str): The username to connect as.
            password (str): The password to use for the connection.
        """

        pp = argparse.ArgumentParser(add_help=False)
        pp.add_argument("-v", "--verbose", action="store_true")

        pp_views = argparse.ArgumentParser(add_help=False)
        pp_views_view = pp_views.add_mutually_exclusive_group()
        pp_views_view.add_argument("--seeding", dest="view", action="store_const", const="seeding",
                                   help="Only show seeding torrents.")
        pp_views_view.add_argument("--active", dest="view", action="store_const", const="active",
                                   help="Only show active torrents.")
        pp_views_view.add_argument("--leeching", dest="view", action="store_const",
                                   const="leeching", help="Filter for leeching torrents.")
        pp_views.set_defaults(view="main")

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(help="Action Categories")

        torrent_parser = subparsers.add_parser("torrent", help="View and manipulate torrents.")
        torrent_sub = torrent_parser.add_subparsers(help="Actions for torrents.")
        torrent_list = torrent_sub.add_parser("list", help="List torrents on the rtorrent server.",
                                              parents=[pp, pp_views])
        torrent_list.set_defaults(func=self.list_torrents)
        torrent_list.add_argument("-l", "--label", action="store_true",
                                  help="Add torrent labels to the list.")
        torrent_list.add_argument("-n", "--name", action="store_true",
                                  help="Remove torrent names from the list.")
        torrent_list.add_argument("-s", "--hash", action="store_true",
                                  help="Remove torrent hashes from the list.")
        torrent_list.add_argument("-p", "--pretty", action="store_true",
                                  help="Print pretty human-readable tables.")

        torrent_ratio = torrent_sub.add_parser("ratio", parents=[pp],
                                               help="Show the ratio for a torrent.")
        torrent_ratio.set_defaults(func=self.get_ratio)
        torrent_ratio.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_label = torrent_sub.add_parser("label", help="Show or set the label on a torrent.",
                                               parents=[pp])
        torrent_label.set_defaults(func=self.get_label)
        torrent_label.add_argument("hash",
                                   help="Hash of the torrent to retrieve.")

        torrent_size = torrent_sub.add_parser("size", parents=[pp],
                                              help="Shows the size of a torrent.")
        torrent_size.set_defaults(func=self.get_size)
        torrent_size.add_argument("hash", help="Hash of the torrent to retrieve.")
        torrent_size_unit = torrent_size.add_mutually_exclusive_group()
        torrent_size_unit.add_argument("-g", action="store_true", help="Print size in Gigabytes.")
        torrent_size_unit.add_argument("-m", action="store_true", help="Print size in Megabytes.")
        torrent_size_unit.add_argument("-p", action="store_true")

        torrent_message = torrent_sub.add_parser("message", parents=[pp],
                                                 help="Shows the tracker message for a torrent.")
        torrent_message.set_defaults(func=self.get_message)
        torrent_message.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_complete = torrent_sub.add_parser("complete", parents=[pp],
                                                  help="Returns whether the torrent is complete or not.")
        torrent_complete.set_defaults(func=self.is_complete)
        torrent_complete.add_argument("hash", help="Hash of the torrent to retrieve.")
        torrent_complete_unit = torrent_complete.add_mutually_exclusive_group()
        torrent_complete_unit.add_argument("-p", action="store_true")
        torrent_complete_unit.add_argument("-b", action="store_true")

        torrent_pause = torrent_sub.add_parser("pause", parents=[pp], help="Pauses a torrent.")
        torrent_pause.set_defaults(func=self.pause_torrent)
        torrent_pause.add_argument("hash", help="Hash of the torrent to retrieve.")
        torrent_pause.add_argument("-n", "--name", action="store_true")

        torrent_stop = torrent_sub.add_parser("stop", parents=[pp], help="Stops a torrent.")
        torrent_stop.set_defaults(func=self.stop_torrent)

        torrent_resume = torrent_sub.add_parser("resume", parents=[pp], help="Resumes a torrent.")
        torrent_resume.set_defaults(func=self.resume_torrent)
        torrent_resume.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_start = torrent_sub.add_parser("start", parents=[pp], help="Starts a torrent.")
        torrent_start.set_defaults(func=self.start_torrent)
        torrent_start.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_path = torrent_sub.add_parser("path", parents=[pp],
                                              help="Shows the path to a torrent.")
        torrent_path.set_defaults(func=self.get_path)
        torrent_path.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_folder = torrent_sub.add_parser("folder", parents=[pp],
                                                help="Prints the path to the folder containing a torrent.")
        torrent_folder.set_defaults(func=self.get_folder)
        torrent_folder.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_add = torrent_sub.add_parser("add", parents=[pp], help="Add a torrent from a file.")
        torrent_add.set_defaults(func=self.add_torrent)
        torrent_add.add_argument("path", help="Path to the torrent file to add.")
        torrent_add.add_argument("-n", "--nostart", action="store_true",
                                 help="Do not start the torrent after adding it.")

        torrent_recheck = torrent_sub.add_parser("recheck", parents=[pp],
                                                 help="Force a recheck on a torrent.")
        torrent_recheck.set_defaults(func=self.recheck)
        torrent_recheck.add_argument("hash", help="Hash of the torrent to retrieve.")

        torrent_move = torrent_sub.add_parser("move", parents=[pp],
                                              help="Move a torrent's storage.")
        torrent_move.set_defaults(func=self.move)
        torrent_move.add_argument("hash", help="Hash of the torrent to move.")
        torrent_move.add_argument("path", help="Folder to move the torrent into.")

        torrent_download = torrent_sub.add_parser("download", parents=[pp],
                                                  help="Download a torrent's files.")
        torrent_download.set_defaults(func=self.download)
        torrent_download.add_argument("hash", help="Hash of the torrent to download.")
        torrent_download.add_argument("-l", "--local", default=None, help="Local path to download to")

        cache_parser = subparsers.add_parser("cache", help="View cache statistics.")
        cache_sub = cache_parser.add_subparsers()
        cache_stats = cache_sub.add_parser("stats", parents=[pp], help="Show cache statistics.")
        cache_stats.set_defaults(func=self.cache_stats)

        self.rtorrent = pyrtor.RtorrentServer(URL, user, password, 15)
        self._fs = None

    def runonce(self):
        """The main entry point for rtorsh.

        Parses the command string and executes the related function.
        """

        args = self.parser.parse_args()
        args.func(args)

    def set_fs(self, rfs):
        """Sets the internal variable self._fs

        Mostly exists to discourage tampering with self._fs directly.
        Potentially used for validation in the future.

        Args:
            fs (rtorshlib.remotefs.*): The RemoteFS implementation to use.
        """

        self._fs = rfs

    def cache_stats(self, args):
        """Dumps the cache statistics for performance evaluation purposes"""

        print("Hits:        {}".format(self.rtorrent.cache.hit_count))
        print("Misses:      {}".format(self.rtorrent.cache.miss_count))
        print("Hit Percent: {}%".format(float(self.rtorrent.cache.hit_count)/float(self.rtorrent.cache.miss_count + self.rtorrent.cache.hit_count)*100.0))
        print("Writes:      {}".format(self.rtorrent.cache.writes))
        print("Reads:       {}".format(self.rtorrent.cache.reads))

    def pause_torrent(self, args):
        """Pauses the selected torrent.

        Args:
            args (namedtuple): The arguments passed by ArgumentParser.
        """

        _check_hash_len(args.hash)
        tor = self.rtorrent.get_torrent(args.hash)
        tor.pause()

    def resume_torrent(self, args):
        _check_hash_len(args.hash)
        tor = self.rtorrent.get_torrent(args.hash)
        tor.resume()

    def stop_torrent(self, args):
        _check_hash_len(args.hash)
        tor = self.rtorrent.get_torrent(args.hash)
        tor.stop()

    def start_torrent(self, args):
        _check_hash_len(args.hash)
        self.rtorrent.get_torrent(args.hash).start()

    def list_torrents(self, args):
        """
        Prints a list of the torrents, with variable fields.

        Args:
            args (namedtuple): Passed in by argparse.
        """

        if args.pretty and not IMP_TABULATE:
            print("tabulate failed to import. Cannot print pretty tables.")
            return
        fields = ["hash", "name"]
        sort = True
        sort_index = 1
        if args.label:
            fields.append("label")
        if args.hash:
            fields.remove("hash")
            sort_index = 0
        if args.name:
            fields.remove("name")
        table = self._get_list(args.view, fields)
        if sort:
            table = sorted(table, key=lambda torrent: torrent[sort_index])
        if args.pretty:
            print(tabulate.tabulate(table,
                                    map(lambda x: x[0].upper() + x[1:].lower(), fields),
                                    tablefmt="grid"))
        else:
            for row in table:
                print("\t |".join(row))

    def _get_list(self, view, fields):
        table = []
        for tor in self.rtorrent.multi(view, fields):
            tmp_list = []
            for i in fields:
                tmp_list.append(tor[i])
            table.append(tmp_list)
        return table

    def get_label(self, args):
        _check_hash_len(args.hash)
        print(self.rtorrent.get_torrent(args.hash).label)

    def is_complete(self, args):
        _check_hash_len(args.hash)
        tor = self.rtorrent.get_torrent(args.hash)
        if args.p:
            print("{0:.2f}%".format(float(tor.completed_bytes())/float(tor.size_bytes())*100))
        elif args.b:
            print("{} B".format(tor.completed_bytes()))
        else:
            print(self.rtorrent.get_torrent(args.hash).is_complete())

    def get_message(self, args):
        _check_hash_len(args.hash)
        tor = self.rtorrent.get_torrent(args.hash)
        print(tor.message)

    def get_size(self, args):
        _check_hash_len(args.hash)
        tor = self.rtorrent.get_torrent(args.hash)
        size = tor.size_bytes()
        if args.g:
            print("{0:.2f} GB".format(size/(1024**3)))
            return
        elif args.m:
            print("{0:.2f} MB".format(size/(1024**2)))
            return
        else:
            print(str(size)+" B")
            return

    def get_ratio(self, args):
        _check_hash_len(args.hash)
        print(self.rtorrent.get_torrent(args.hash).get_ratio())

    def get_path(self, args):
        _check_hash_len(args.hash)
        print(self.rtorrent.get_torrent(args.hash).base_path())

    def get_folder(self, args):
        _check_hash_len(args.hash)
        print(self.rtorrent.get_torrent(args.hash).directory())

    def add_torrent(self, args):
        _check_hash_len(args.hash)
        with open(args.path, mode='rb') as content_file:
            content = content_file.read()
        if args.nostart:
            self.rtorrent.load(content, start=False)
        else:
            self.rtorrent.load(content, start=True)

    def recheck(self, args):
        _check_hash_len(args.hash)
        self.rtorrent.get_torrent(args.hash).recheck()

    def move(self, args):
        """Moves a torrent's local storage and updates rtorrent's path.

        Args:
            args (namedtuple): The arguments passed by argparse.
        """

        if self._fs is None:
            print("remotefs not configured.  Cannot execute this command.")
            sys.exit(1)
        tor = self.rtorrent.get_torrent(args.hash)
        old_path = tor.directory()
        base = old_path.split('/')[-1]
        tor.stop()
        tor.set_directory('/'.join([args.path, base]))
        self._fs.move(old_path, args.path)
        tor.start()
        return

    def download(self, args):
        """Downlaods all of the files for a selected torrent using a RemoteFS implementation.

        Args:
            args (namedtuple): The arguments passed by argparse.
        """

        if self._fs is None:
            print("remotefs not configured.  Cannot execute this command.")
            sys.exit(1)
        tor = self.rtorrent.get_torrent(args.hash)
        tor_dir = tor.directory()
        if args.local is not None:
            local_path = args.local
        else:
            local_path = os.path.join(os.getcwd(), tor.name)

        print("Downloading {} to {}.".format(tor_dir, local_path))
        if not os.path.isdir(local_path):
            os.mkdir(local_path)
        if self._fs.isdir(tor_dir):
            self._fs.get_folder(tor_dir, local_path)
        else:
            self._fs.get_file(tor_dir, local_path)


def run():
    """The entry point for the application, to prevent global variables."""

    conf_path = os.path.expanduser("~/.rtorsh.conf")
    if not os.path.isfile(conf_path):
        print("Configuration file {} does not exist.".format(conf_path))
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.rtorsh.conf"))
    shell = RtorrentShell(config["rtorrent"]["url"], config["rtorrent"]["user"],
                          config["rtorrent"]["password"])
    if "remotefs" in config.sections():
        if config["remotefs"]["type"] == "sftp":
            rfs = rtorshlib.remotefs.SFTPFS(config["remotefs"]["host"],
                                            config["remotefs"]["user"],
                                            config["remotefs"]["password"])
            shell.set_fs(rfs)
        else:
            print("Unrecognized connection type {} in remotefs config.".format(config["remotefs"]["type"]))
    shell.runonce()


def _check_hash_len(tor_hash):
    """Ensures that the hash given is of the appropriate length.

    Args:
        tor_hash (str): The hash to check the length of.
    """

    if len(tor_hash) != 40:
        print("Incorrect length for torrent hash.")
        sys.exit(1)

if __name__ == "__main__":
    run()
