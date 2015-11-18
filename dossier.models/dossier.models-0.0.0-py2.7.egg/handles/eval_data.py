
import json
import os

s1 = '''1337 | Shadow008 | H4x0rL1f3 | H4x0r HuSsy | KhantastiC HaXor | InvectuS | Dr.Z0mbie | phpBuGz | madcodE | r00x | Don | MindCracker
Sizziling Leet | Deatth ArrivaLz | MaD GirL | Sn!p3r_GS | DeXter | Neo Haxor | Darksnipper | Ment@l Mind | Error404
Pain006 | b0x | R3DL0F | Sahrawi | 3thicaln00b | Hmei7 | CutY | infinityl33ts | l4m3r | skywalk3r | Sniffer
AL.MaX HaCkEr | M4DSh4K | H3ll-DZ | gujjar(pcp) | KAmi HaXor | BMPoC | H4x0r10ux M1nd
H4x0r_kSa | Gh0St_kSa | H4CK3R $P1D3R | 8thbit | AZ Sn1ff3r (PCP)
Pak Defender | VIRkid | TR4CK3R | _-_ L.a.F.a.n.G.a _-_ | Trafalgar Law
Xpired | NetSpy | d3b~X
    '''
s2 = '''Crusader gerion killxp lelick truegeek'''

usernames_with_saved_data = [
    '3thicaln00b',
    '0xClay',
]

def findall(path):
    texts = []
    return texts

def load_eval_data(username):
    #yield (s1, map(lambda x: x.strip(), s1.split('|')))
    #yield (s2, s2.split())
    path = os.path.join(os.path.dirname(__file__), 'tests/data', username)
    for root, dirs, fnames in os.walk(path):
        for fname in fnames:
            if fname.endswith('.json'):
                fpath = os.path.join(root, fname)
                expected = json.load(open(fpath))
                fpath = fpath[:-5] + '.html'
                raw_data = open(fpath).read()
                yield raw_data, expected
