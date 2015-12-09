import collections
import os
import os.path
import stat


class SFTPFS:
    def __init__(self, host, username, password):
        self._pm = __import__("paramiko")
        self._host = host
        self._username = username
        self._password = password

    def _login(self):
        """Handles the login process and returns a usable SFTP handle."""

        ssh = self._pm.SSHClient()
        ssh.set_missing_host_key_policy(self._pm.AutoAddPolicy())
        ssh.connect(self._host, username=self._username, password=self._password)
        sftp = ssh.open_sftp()
        SFTPConn = collections.namedtuple('SFTPConn', ['sftp', 'ssh'])
        conn = SFTPConn(sftp=sftp, ssh=ssh)
        return conn

    def ls(self, directory):
        """Returns a list of files/folders in the specified directory"""

        conn = self._login()
        ret = conn.sftp.listdir(directory)
        conn.sftp.close()
        conn.ssh.close()
        return ret

    def move(self, cur_path, new_dir):
        """Moves a selected file/folder into a new folder."""

        conn = self._login()
        base = cur_path.split('/')[-1]
        conn.sftp.rename(cur_path, '/'.join([new_dir, base]))
        conn.sftp.close()
        conn.ssh.close()
        return

    def get_file(self, rfile, lfile):
        conn = self._login()
        conn.sftp.get(rfile, lfile)
        conn.sftp.close()
        conn.ssh.close()
        return

    def get_folder(self, rdir, ldir):
        conn = self._login()
        for tor_file in conn.sftp.listdir(path=rdir):
            local_path = os.path.join(ldir, tor_file.split("/")[-1])
            if self.isdir("/".join([rdir, tor_file])):
                if not os.path.isdir(local_path):
                    os.mkdir(local_path)
                self.get_folder("/".join([rdir, tor_file]), local_path)
            else:
                self.get_file("/".join([rdir, tor_file]), local_path)
        conn.sftp.close()
        conn.ssh.close()
        return

    def get(self, rdir, dl_dir):
        ldir = dl_dir + rdir.split("/")[-1]
        if self.isdir(rdir):
            self.get_folder(rdir, ldir)
        else:
            self.get_file(rdir, ldir)

    def isdir(self, rpath):
        conn = self._login()
        ret = stat.S_ISDIR(conn.sftp.stat(rpath).st_mode)
        conn.sftp.close()
        return ret
