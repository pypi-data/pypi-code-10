import pwd
import os
import re
import subprocess

__author__ = 'umairghani'

# Random functions

def execute(args, user="root"):
    """
    Runs SHELL command as a certain user
    :param args:
    :param user:
    :return: stdout, stderr
    """
    _uid = pwd.getpwnam(user).pw_uid
    os.setuid(_uid)
    os.seteuid(_uid)
    os.setreuid(_uid, _uid)
    p = subprocess.Popen(args, bufsize=0, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate()


def parseIO(iostat):
    """
    Parses the iostat in an array if info
    :param iostat
    :return: array of dict
    """
    data = []
    for disk, stat in iostat.items():
        data.append({
            disk: {
                "read_count": stat.read_count,
                "write_count": stat.write_count,
                "read_bytes": stat.read_bytes,
                "write_bytes": stat.write_bytes,
                "read_time": stat.read_time,
                "write_time": stat.write_time,
            },
        })
    return data


def parseNetstat(stats):
    """
    Parses an array of stats
    and organizes in an array of dict
    :param netstat output
    :return: array of dict
    """
    result = []
    for stat in stats:
      if stat:
        _nstat = re.split("\s+", stat.strip())
        if _nstat[0] == 'Netid': 
            continue
        elif _nstat[0]:
            _nresult = {
                "netid": _nstat[0],
                "state": _nstat[1],
                "recv-Q": _nstat[2],
                "send-Q": _nstat[3],
                "address": [
                    { 
                        "local": _nstat[4].split(":")[0], 
                        "port": None if len(_nstat[4].split(':')) == 1 else _nstat[4].split(':')[1] 
                    },
                    { 
                        "peer": _nstat[5].split(":")[0], 
                        "port": None if len(_nstat[5].split(':')) == 1 else _nstat[5].split(':')[1] 
                    },
                ]
                #"LocalAddress:Port": _nstat[3],
                #"PeerAddress:Port": _nstat[4],
            }
            result.append(_nresult)
    return result


def parseIfcfg(ifconfig):
    """
    Parses the ifconfig in an array if info
    :param iostat
    :return: array of dict
    """
    data = []
    for nic,stat in ifconfig.items():
        data.append({
            nic: {
                "bytes_sent": stat.bytes_sent,
                "bytes_recv": stat.bytes_recv,
                "packets_sent": stat.packets_sent,
                "packets_recv": stat.packets_recv,
                "errin": stat.errin,
                "errout": stat.errout,
                "dropin": stat.dropin,
                "dropout": stat.dropout,
            },
        })
    return data


def parseProcesses(processes):
    """
    Parses an array of process
    and organizes in an array of dict
    :param processes
    :return: array of dict
    """
    result = []
    for p in processes:
        if p:
            _pinfo = re.split("\s+", p)
            _starttime = "%s %s %s %s %s" % \
                          (_pinfo[4], _pinfo[5], _pinfo[6], _pinfo[7], _pinfo[8])
            _presult = {
                "user": _pinfo[0],
                "pid": _pinfo[1],
                "pcpu": _pinfo[2],
                "pmem": _pinfo[3],
                "starttime": _starttime,
                "args": " ".join(_pinfo[9:]),
                "threadcount": ""
            }   

            # Get threadcount of the process
            cmd = "ps -eLF | grep %s | grep -v grep | wc -l" % _pinfo[1]
            try:
                out, err = execute(cmd)
                _presult["threadcount"] = out.strip()
            except Exception:
                pass

            result.append(_presult)
    return result
