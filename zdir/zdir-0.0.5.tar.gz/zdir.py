import hashlib
import binascii
import os
import io
import datetime
import zipfile
import shutil


def mkdir(path):
    try:
        os.makedirs(path)
    except:
        pass


def generate_key(name, content, shard=2):
    try:
        sha1 = hashlib.sha1(content).digest()
    except:
        sha1 = hashlib.sha1(
            to_bytes(content)
        ).digest()

    key = binascii.hexlify(sha1)
    if shard:
        return "%s/%s" % (key[:shard], key)
    return key


class Processor(object):

    def __init__(self):
        self.steps = []

    def step(self, fun):
        self.steps.append(fun)

    def process(self, value):
        x = value
        for f in self.steps:
            x = f(x)
        return x


def to_bytes(content):
    if type(content) == type(""):
        return content

    if type(content) == type(u""):
        return content.encode("utf-8")
    return str(content)


def to_unicode(value):
    if type(value) == type(u""):
        return value
    if type(value) == type(""):
        return value.decode("utf-8")
    return unicode(value)


class Bin(object):

    def __init__(self, path):
        self.path = path
        mkdir(path)
        self.unicode = Processor()
        self.unicode.step(to_unicode)
        self.unicode.step(lambda x: x.replace("\t", "\\t"))
        self.unicode.step(lambda x: x.replace("\n", "\\n"))

        self.bytes = Processor()
        self.bytes.step(to_bytes)

    def log(self, logname, *args):
        logpath = os.path.join(self.path, logname)
        args = [self.unicode.process(x) for x in args]
        r = u"%s\t%s\n" % (
            datetime.datetime.utcnow().isoformat(), "\t".join(args))
        with io.open(logpath, "a", encoding="utf-8") as f:
            f.write(r)

    def put(self, name, mime, content):
        key = generate_key(name, content)
        p = os.path.join(self.path, key)
        mkdir("/".join(p.split("/")[0:-1]))
        self.log("logfile.txt", key, name, mime, len(content))
        if not os.path.exists(p):
            with io.open(p, "wb") as f:
                f.write(self.bytes.process(content))

    def comment(self, content):
        self.log("comments.txt", content)

    @property
    def items(self):
        with io.open(os.path.join(self.path, "logfile.txt")) as f:
            t = [parse_logline(self.path, x) for x in f if x.strip()]
        return t


def parse_logline(bin, line):
    d, k, n, m, l = line.split("\t")
    return (
        os.path.join(bin, k),
        datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f"),
        n,
        m,
        int(l.strip()),
    )


def tree(p):
    for root, dirs, files in os.walk(p):
        for fn in files:
            yield os.path.join(root, fn)


class Z(object):

    def __init__(self, base):
        self.base = base
        mkdir(base)
        self.bin = self.find_bin()
        self.items_cache = {}

    def find_bin(self):
        for x in os.listdir(self.base):
            if x.endswith(".zdir"):
                return Bin(os.path.join(self.base, x))
        return None

    def create_bin(self):
        k = "%s-%s.zdir" % (
            datetime.datetime.utcnow().strftime("%Y%m%d"),
            binascii.hexlify(os.urandom(2))
        )
        self.bin = Bin(os.path.join(self.base, k))
        return self.bin

    def finalize(self):
        if self.bin is None:
            return
        n = self.bin.path + ".zip"
        tempname = os.path.join(self.base, binascii.hexlify(os.urandom(6)))
        os.rename(self.bin.path, tempname)

        self.bin = None

        with zipfile.ZipFile(n, 'w') as f:
            for g in tree(tempname):
                name = g[len(tempname):]
                f.write(g, name)

        shutil.rmtree(tempname)

        with io.open(n, 'rb') as f:
            zip_sha = hashlib.sha1( f.read()).digest()

        nn = n.split(".")[0].split("/")[-1]
        zip_sha_hex = binascii.hexlify(zip_sha)
        name = n.replace(nn, zip_sha_hex)
        os.rename(n,name)



    def put(self, name, mime, content):
        if self.bin is None:
            self.bin = self.create_bin()
        self.bin.put(name, mime, content)

    def comment(self, content):
        if self.bin is None:
            self.bin = self.create_bin()
        self.bin.comment(content)

    @property
    def items(self):
        results = []
        items = [os.path.join(self.base, x)
                 for x in os.listdir(self.base) if ".zdir" in x]
        for z in [x for x in items if x.endswith(".zip")]:
            with zipfile.ZipFile(z) as f:
                t = [parse_logline(z, x) for x in f.read(
                    "logfile.txt").split("\n") if x.strip()]
            results.extend(t)
        if self.bin:
            results.extend(self.bin.items)

        return results

    def filter(self, fun):
        for x in self.items:
            if fun(x):
                yield x, self.read(x[0])

    def read(self, key):
        ext = ".zip"
        if ext in key:
            i = key.index(ext)
            fn, kn = key[:i+len(ext)], key[i+len(ext)+1:]
            with zipfile.ZipFile(fn) as f:
                data = f.read(kn).decode("utf-8")
        else:
            with io.open(key, encoding="utf-8") as f:
                data = f.read()
        return data
