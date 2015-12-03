"""
just a demo of what overprint can do
"""

from overprint import overprint
import time
import random
import withlog

t = 35

def random_message():
    return random.choice([
        "Computing transverse dispersion",
        "Inverting retroactive flux",
        "Charging flux capacitor",
        "Calibrating power coupler",
        "Compensate for vacuum fluctuation",
        "Adjusting for time distortion",
        "Activation of trans-dimensional swap device",
        "Pre-Heating warp drive",
        "Internalisation of the TCP-IP stack",
        "Generation of secure Crypto-scheme",
        "Spawning quantum threads",
        "Protect wave function against collapse",
        ])

with withlog.Warning('Updating HyperDrive') as w, overprint(w) as (reprint, print):
    print(' == This is a combined demo of `overprint` and `withlog`')
    print('')
    for i in range(40):
        reprint('Step {} of 40 : '.format(i) + random_message())
        if random.randint(0,10) > 8:
            print(random_message())
        time.sleep(random.randint(1, t)/100)
        reprint('')

