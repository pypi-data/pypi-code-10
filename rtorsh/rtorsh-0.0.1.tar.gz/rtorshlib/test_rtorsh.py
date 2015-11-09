import pytest
import rtorshlib.rtorsh
import os


@pytest.fixture
def shell():
    myshell = rtorshlib.rtorsh.RtorrentShell(os.environ['RTORRENT_URL'], os.environ['RTORRENT_USER'],
                                   os.environ['RTORRENT_PASSWORD'])
    return myshell


def test_check_hash_len_short():
    with pytest.raises(SystemExit):
        rtorshlib.rtorsh._check_hash_len('E5423423GH1')


def test_check_hash_len_long():
    with pytest.raises(SystemExit):
        rtorshlib.rtorsh._check_hash_len('WSI31O5EZACJYDKPL6WDCBTH5EAO5UWZSG07SGAG57IX4NFHQE')


def test_list(shell):
    args = shell.parser.parse_args(["torrent", "list"])
    args.func(args)


def test_list_pretty(shell):
    args = shell.parser.parse_args(["torrent", "list", "-p"])
    args.func(args)
