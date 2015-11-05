from subprocess import *

args = [
    'ssh',
    'root@jupyter.pl.sophia.inria.fr',
    'hostname'
]

proc = Popen(
    args,
    stdout = PIPE,
    stderr = PIPE,
    universal_newlines=True,
    )

#out, err = proc.communicate()
#proc.wait()

