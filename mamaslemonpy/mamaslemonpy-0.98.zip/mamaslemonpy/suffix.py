"""
This module implements a suffix array of a set of strings over an alphabet.
"""

import math
import array
import itertools
from bisect import bisect, bisect_left
import numpy as np

from . import names
from . import seqs
from . import utils

############################################################################        

class SuffixDLL():
    """a suffix array builder that simulates a doubly linked list"""

    def __init__(self, s):
        """prepare building a suffix array of sequence 's',
        which must provide an 'alphabet' attribute (its alphabet class).
        The alphabet must provide its SIZE and an isspecial(ch) method.
        To compute the instance, call one of the build_* methods.
        Remember to explicitly allocate memory for the prv and nxt attributes
        by calling self.allocate() first.
        """
        asize = s.alphabet.SIZE  # alphabet knows its size
        self.isspecial = s.alphabet.isspecial
        self.alphabet = s.alphabet
        self.first = [-1]*asize
        self.last = [-1]*asize
        self.s = s
        self.prv = None
        self.nxt = None

    def allocate(self):
        """allocate memory for prv and nxt attributes."""
        self.prv = utils.filled_array("l", len(self.s))
        self.nxt = array.array("l", self.prv)


    _REPORTINTERVAL = 1000000;
    _REPORTMOD = _REPORTINTERVAL - 1
    def __report(self, p, steps, anyway=False, interval=_REPORTINTERVAL, mod=_REPORTMOD):
        if anyway or (p % interval == mod):
            print((p+1)/1000000,"Mbp remaining;",steps,"steps so far")

    def build_minLR(self):
        """build the suffix array using the minLR method,
        which ist fast, but needs more memory.
        Upon completion, the pos array is represented as self.prv and self.nxt.
        It is obtained by starting at p = self.firtpos()
        and then iterating p = self.nxt[p].
        This method returns the number of steps needed to build the array.
        """
        (first, last) = (self.first, self.last)
        (prv, nxt) = (self.prv, self.nxt)
        asize = self.alphabet.SIZE
        # insert functions that work on first, last, prv, nxt; use asize
        def insertbetween(p1, p2, i):
            """insert i between p1 and p2"""
            prv[i] = p1
            nxt[i] = p2
            if p2 != -1:
                prv[p2] = i
            if p1 != -1:
                nxt[p1] = i
        def insertasfirst(i, ch):
            p = first[ch]
            insertbetween(prv[p], p, i)
            first[ch]=i
        def insertaslast(i, ch):
            p = last[ch]
            insertbetween(p, nxt[p], i)
            last[ch]=i
        def insertasnew(i, ch):
            first[ch] = last[ch] = i
            # find next smaller existing character
            cp = ch - 1
            while (cp >= 0) and (last[cp] == -1):
                cp -= 1
            ip = last[cp] if cp >= 0 else -1
            # find next bigger existing character
            cs = ch + 1
            while (cs < asize) and (first[cs] == -1):
                cs += 1
            js = first[cs] if cs < asize else -1
            insertbetween(ip,js,i)
        # start to build
        s = self.s
        special = self.isspecial  # function to determine which characters are special
        steps = 0
        for (p,ch) in zip(range(len(s)-1, -1, -1), reversed(s)):
            steps += 1
            if first[ch] == -1:  # ch seen for the first time
                insertasnew(p,ch)
                continue
            elif special(ch):    # ch already seen and special
                insertasfirst(p,ch)
                continue
            # ch already seen, and ch is normal character
            pup = pdn = p+1
            while True:
                # look "up"
                steps += 1
                pup = prv[pup]
                if pup == -1:  # end of list: insert as first
                    insertasfirst(p, ch)
                    break  # from while True
                if s[pup-1] == ch:  # found by walking up: insert
                    pup -= 1
                    if last[ch] == pup:
                        insertaslast(p, ch)
                    else:
                        insertbetween(pup, nxt[pup], p)
                    break  # from while True
                # look "down"
                steps += 1
                pdn = nxt[pdn]
                if pdn == -1:  # end of list: insert as last
                    insertaslast(p, ch)
                    break  # from while True
                if s[pdn-1] == ch:  # found by walking down: insert
                    pdn -= 1
                    if first[ch] == pdn:
                        insertasfirst(p, ch)
                    else:
                        insertbetween(prv[pdn], pdn, p)
                    break  # from while True
            steps -= 1
        return steps

    def firstpos(self):
        for p in self.first:
            if p != -1:
                return p
        return -1


############################################################################        

class OccTable():

    def __init__(self, bwt, occrate=128):
        self._occ = None  # 2d numpy array
        self._less = None  # 1d numpy array
        self.occrate = occrate
        self.bwt = bwt
        alphabet = bwt.alphabet
        self.alphabet = alphabet
        self.regulars = alphabet.regulars
        self.firstregular = alphabet.firstregular
        # Closures, functions set at runtime. Remove for pickling.
        self.at = None      # at(r,a) computes occ[r,a]
        self.at_reg = None  # at_reg(r,a_reg) computes occ(r, a_reg+firstregular)
        self.less = None    # less(a) is number of characters < a
        self.less_reg = None  # less_reg(a_reg) is number of characters < a+firstregular
        self.all_at = None  # all_at(r) computes [occ[r,a] for all a]


    def set_at_function(self):
        """
        Return the at function;
        at(r,a) is number of a's up to index r in BWT.
        """
        occ = self._occ
        ocr = self.occrate
        bwt = self.bwt
        reg = self.regulars
        fre = self.firstregular
        occ_item = occ.item

        def _at1(r, a):
            return occ_item(r, a - fre)

        _at_reg1 = occ_item

        def _all_at1(r):
            return occ[r].tolist()

        def _at(r, a):
            if r < 0:
                return 0
            idx = r // ocr
            x = occ_item(idx, a - fre)
            x += sum(b == a for b in bwt[idx*ocr+1 : r+1])
            return x

        def _at_reg(r, a_reg):
            if r < 0:
                return 0
            idx = r // ocr
            x = occ_item(idx, a_reg)
            a = a_reg + fre
            x += sum(b == a for b in bwt[idx*ocr+1 : r+1])
            return x

        def _all_at(r):
            if r < 0:
                return [0] * reg
            idx = r // ocr
            lookup = reg * idx
            x = occ[reg].tolist()
            for b in bwt[idx*ocr+1 : r+1]:
                c = b - fre
                if 0 <= c < reg:
                    x[c] += 1
            return x

        if ocr == 1:
            self.at = _at1
            self.at_reg = _at_reg1
            self.all_at = _all_at1
        else:
            self.at = _at
            self.at_reg = _at_reg
            self.all_at = _all_at


    def set_less_function(self, handle_errors=True):
        """
        Return the less function; less(a) is number of characters < a.
        If handle_errors == True, less(a) returns -1 on invalid a
        """
        fre = self.firstregular
        reg = self.regulars
        ls = self._less.item
        def fless(a):
            a_reg = a -fre
            return ls(a_reg) if 0 <= a_reg < reg else -1  # -1 indicates error
        def fless_reg(a_reg):
            return ls(a_reg) if 0 <= a_reg < reg else -1  # -1 indicates error
        def fless_blind(a):
            return ls(a - fre)
        def fless_blind_reg(a_reg):
            return ls(a_reg)

        if handle_errors:
            self.less = fless
            self.less_reg = fless_reg
        else:
            self.less = fless_blind
            self.less_reg = fless_blind_reg


    def compute_from_bwt(self):
        """compute occ and less from bwt by counting characters"""
        bwt = self.bwt
        occrate = self.occrate
        special = self.alphabet.isspecial
        regulars = self.regulars
        firstregular = self.firstregular
        items = (occrate - 1 + len(bwt)) // occrate
        # use size items+1 to append zeros so that all(occ[-1] == 0)
        occ = np.zeros((items+1, regulars), dtype=np.int32)
        nltr = 0  # number of "less than regular" characters
        for (r,b) in enumerate(bwt):
            if not special(b):
                occ[r // occrate][b - firstregular] += 1
            elif b < firstregular:
                nltr += 1
        np.cumsum(occ, axis=0, out=occ)
        less = np.insert(occ[-2][:-1], 0, nltr)
        np.cumsum(less, out=less)
        self._occ = occ
        self._less = less
        self.set_at_function()
        self.set_less_function()

    def tofile(self, focc):
        """write occ and less to binary file <focc>"""
        self._occ[:-1].tofile(focc)  # drop zeros from occ[-1]
        self._less.tofile(focc)

    def fromfile(self, focc):
        """read occ and less from binary file <focc>"""
        ocr = self.occrate
        items = (ocr - 1 + len(self.bwt)) // ocr
        occ = np.fromfile(focc, dtype=np.int32, count=self.regulars * items)
        # use size items+1 to append zeros so that all(occ[-1] == 0)
        occ.resize(items+1, self.regulars)
        self._occ = occ
        self._less = np.fromfile(focc, dtype=np.int32, count=self.regulars)
        self.set_at_function()
        self.set_less_function()


############################################################################        

class LcpTable:
    def __init__(self):
        self.mode = None
        self._lcp = None
        self._xind = None
        self._xval = None
        self.nexceptions = None
        # closures, remove for pickling
        self.at = None  # self.at(r) == lcp[r]
        self.xfind = None  # self.xfind(r) == lcp[r] if r is a large-value-exception

    def __iter__(self):
        return _LcpIterator(self)

    def fromfile(self, mode=0, fv=None, fx=None):
        typecodes = {0:'l', 1:'B', 2:'H', -1:'B', -2:'H'}
        typecode = typecodes[mode]
        self._lcp = array.array(typecode)
        n = utils.number_of_items_in_file(fv, typecode)
        self._lcp.fromfile(fv, n)
        if mode > 0:  # only load lcp exceptions when mode is positive.
            nx = utils.number_of_items_in_file(fx, "l") // 2
            self._xind = array.array("l")
            self._xval = array.array("l")
            self._xind.fromfile(fx,nx)
            self._xval.fromfile(fx,nx)
            self.nexceptions = nx
        self.mode = mode
        self.set_at_function()

    def set_at_function(self):
        mode = self.mode
        # define exception finder
        _xind = self._xind
        _xval = self._xval
        def xfind(r):
            """Locate the leftmost index exactly equal to r"""
            i = bisect_left(_xind, r)
            if (i != len(_xind)) and (_xind[i] == r):
                return _xval[i]
            raise ValueError("{} should be an lcp exception, but was not found".format(r))
        self.xfind = xfind
        # define item getters, store appropriate one as 'at' method.
        lcp = self._lcp
        def get0(r): return lcp[r]
        def get1(r):
            lv = lcp[r]
            return lv if lv < 255 else xfind(r)
        def get2(r):
            lv = lcp[r]
            return lv if lv < 65535 else xfind(r)
        # set functions in self
        atfunction = {0:get0, 1:get1, 2:get2, -1:get0, -2:get0}[mode]
        self.at = atfunction


class _LcpIterator:
    """iterator over an lcp array, taking into account exceptions"""
    #__slots__ = ['lcp', 'xind', 'xval', 'limit', 'r', 'x', 'n']

    def __init__(self, lcptable):
        self.lcp = lcptable._lcp
        self.xind = lcptable._xind
        self.xval = lcptable._xval
        self.limit = {0:(1<<63)-1, 1:(1<<8)-1, 2:(1<<16)-1, -1:(1<<8)-1, 2:(1<<16)-1}[lcptable.mode]
        self.r = 0
        self.x = 0
        self.n = len(self.lcp)

    def __next__(self):
        r = self.r
        if r >= self.n:
            raise StopIteration
        v = self.lcp[r]
        if v >= self.limit:
            ###assert v == self.limit, "limit is {}, value is {}".format(self.limit, v)
            ###assert self.xind[self.x] == r
            v = self.xval[self.x]
            ###print("lcp exception at r={}: value={}".format(r,v))
            self.x += 1
        self.r += 1
        return v

    def __iter__(self):
        return self
        
############################################################################        

class SuffixArray():
    def __init__(self, s):
        """initialize a new suffix array from a sequence container 's'"""
        self.s = s              # container type from seqs module
        self.alphabet = None    # alphabet type from seqs module
        self.length = None      # int
        self.manifest = None    # list of tuples
        if s is not None:
            self.alphabet = s.alphabet
            self.length = len(s)
            self.manifest = s.manifest
        self.dll = None         # SuffixDLL
        self.firstpos = None    # array("l")
        self.nextpos = None     # array("l")
        self.prevpos = None     # array("l")
        self.buffer = None      # array("l")
        self.pos = None         # array("l")
        self.plcp = None        # array("l")
        self.bwt = None         # container type from seqs module
        self.occ = None         # OccTable
        self.lcp = None         # LcpTable
        self.rindex = None      # array("?"), maps r -> manifest index
        self.lcp_threshold = 0  # interval length below which lcp should be used
        self.has_closures = False

    @classmethod
    def from_indexname(cls, iname):
        sa = cls(None)  # obtain an empty shell for suffix array
        s = seqs.get_container_from_indexname(iname)
        sa.s = s
        sa.alphabet = s.alphabet
        sa.manifest = s.manifest
        sa.length = s.manifest[-1][2] + 1
        return sa

    def __len__(self):
        return self.length

    def set_closures(self):
        occ = self.occ
        if occ is not None:
            occ.set_at_function()
            occ.set_less_function()
        lcp = self.lcp
        if lcp is not None:
            lcp.set_at_function()
        self.has_closures = True

    def remove_closures(self):
        occ = self.occ
        if occ is not None:
            occ.at = occ.at_reg = occ.all_at = occ.less = occ.less_reg = None
        lcp = self.lcp
        if lcp is not None:
            lcp.at = lcp.xfind = None
        self.has_closures = False

    def substring(self, p, q):
        """return the s[p:q] as a human-readable string object,
        where s is the ecoded  sequence in the suffix array"""
        ch = self.alphabet.characters
        s = self.s
        return "".join(ch[s[i]] for i in range(p,q))

    def description_at(self, rank=None, pos=None):
        """return the name/description of the sequence
        at position <pos> or rank <rank> from the manifest.
        Specify either <rank> or <pos>, but not both."""
        if not ((rank is None) ^ (pos is None)):
            raise ValueError("give either pos or rank, but not both")
        desc = self.rindex
        if rank is not None:
            if desc is not None:
                i = desc[rank]
            else:
                pos = self.pos[rank]  # compute via self.pos instead
        if pos is not None:
            # find largest i such that lastssp[i] <= pos
            i = bisect(self.s.lastssp, pos) # see lastssp_index() in seqs
        return self.manifest[i][-1]

    def seq_from_indexname(self, iname):
        """obtain encoded sequence from file"""
        # we assume that s is aleady a container
        # but the sequence buffer is not yet filled.
        manifest = self.manifest
        aclass = self.alphabet
        container = aclass.containerclass
        assert container is self.s.__class__
        seqname = names.seq(iname)
        with open(seqname,"rb") as fbuf:
            s = container.fromfile(fbuf, manifest, aclass)
        self.s = s

    def _initialize_nextpos(self):
        dll = SuffixDLL(self.s)
        dll.allocate()
        self.dll = dll

    def nextpos_from_s(self):
        if self.dll is None:
            self._initialize_nextpos()
        steps = self.dll.build_minLR()
        self.nextpos = self.dll.nxt
        self.prevpos = self.dll.prv
        self.firstpos = self.dll.firstpos()
        self.dll = None
        self.buffer = self.prevpos

    def nextpos_from_indexname(self, iname):
        fname = names.nextpos(iname)
        self.nextpos = utils.ensure_array(self.nextpos, fname)
        # firstpos is the only number in {-1,0,1,...,items-1} that is not in nextpos
        sfull = sum(range(-1, len(self.nextpos)))
        s = sum(self.nextpos)
        self.firstpos = sfull - s

    def pos_from_nextpos(self, p=None):
        # re-use buffer (from prevpos), or allocate new array for pos
        self.prevpos = None
        self.pos = self.buffer
        if self.pos is None:
            self.pos = array.array("l", self.nextpos)
        (pos, nxt) = (self.pos, self.nextpos)
        # start filling pos from position p (default: firstpos)
        if p is None:
            p = self.firstpos
        r = 0
        while p != -1:
            pos[r] = p
            r += 1
            p = nxt[p]

    def pos_from_indexname(self, iname):
        self.pos = utils.ensure_array(self.pos, names.pos(iname))

    def rindex_from_pos(self):
        typecode = utils.typecode_unsigned(len(self.manifest))
        rindex = array.array(typecode)
        pos = self.pos
        lastssp = self.s.lastssp
        for r in range(self.length):
            rindex.append(bisect(lastssp, pos[r]))
        self.rindex = rindex

    def rindex_from_indexname(self, iname):
        typecode = utils.typecode_unsigned(len(self.manifest))
        self.rindex = utils.ensure_array(self.rindex, names.rindex(iname), typecode=typecode)

    def plcp_from_nextpos(self):
        # re-use buffer (from prevpos), or allocate new array for pos
        self.prevpos = None
        self.plcp = self.buffer
        if self.plcp is None:
            self.plcp = array.array("l", self.nextpos)
        (plcp, nxt, s) = (self.plcp, self.nextpos, self.s)
        scmp = s.suffixcmp
        ll = 0
        for (p,pp) in enumerate(nxt):
            # p = 0..n-1 and always pp = nxt[p]
            if ll > 0:
                ll -= 1
            if pp == -1:
                ###assert ll==0
                plcp[self.firstpos] = -1
                continue
            # Compute lcp between suffixes at p and pp, store at pp for now
            # We know the length is at least ll and attempt to compare addl chars.
            (result, ll) = scmp(p,pp,ll)
            ###assert result<0, "lcp({},{})={}, result={}".format(p,pp,ll,result)
            plcp[pp] = ll


    def lcp_from_plcp_generator(self, bufsize=(1<<22)):
        a = array.array("l", [0]*bufsize)
        (plcp, nxt) = (self.plcp, self.nextpos)
        remaining = len(nxt)
        p = self.firstpos
        while remaining >= bufsize:
            for r in range(bufsize):
                a[r] = plcp[p]
                p = nxt[p]
            yield a
            remaining -= bufsize
        a = array.array("l", [0]*remaining)
        for r in range(remaining):
            a[r] = plcp[p]
            p = nxt[p]
        yield a

    def lcpn_from_lcp_streaming(self, flcp, flcpn, flcpnx, n=1, bufsize=(1<<20)):
        if not n in (1, 2):
            raise ValueError("must choose n=1 or n=2")
        data = (None, ("B", 255), ("H", 65535))
        (typecode, maxval) = data[n]
        remaining = len(self.s)
        lcpnxi = array.array("l")
        lcpnxv = array.array("l")
        lcpn = array.array(typecode, [0]*bufsize)
        r = 0
        while True:
            while remaining >= bufsize:
                lcp = array.array("l")
                lcp.fromfile(flcp,bufsize)
                for (rr,lv) in enumerate(lcp):
                    if not (0 <= lv < maxval):
                        lcpn[rr] = maxval
                        lcpnxi.append(r)
                        lcpnxv.append(lv)
                    else:
                        lcpn[rr] = lv
                    r += 1
                lcpn.tofile(flcpn)
                remaining -= bufsize
            if remaining == 0:
                break
            bufsize = remaining
            lcpn = array.array(typecode, [0]*bufsize)
        assert len(lcpnxi) == len(lcpnxv), "lcpn length mismatch"
        lcpnxi.tofile(flcpnx)
        lcpnxv.tofile(flcpnx)
        del lcpnxi, lcpnxv, lcp, lcpn

    def lcp_from_indexname(self, iname, mode=1):
        """set self.lcp to the appropriate LcpTable object,
        read from the given index 'iname'"""
        lname = names.lcp_names[mode](iname)
        lcp = LcpTable()
        if mode != 0:
            xname = names.lcp_xnames[mode](iname)
            with open(lname,"rb") as flcp, open(xname,"rb") as fx:
                lcp.fromfile(mode, flcp, fx)
        else:
            with open(lname,"rb") as flcp:
                lcp.fromfile(mode, flcp, None)
        self.lcp = lcp

    def bwt_from_pos(self):
        (s, pos) = (self.s, self.pos)
        containerclass = s.__class__
        bwt = containerclass(self.alphabet)
        bwt.append_sequence((s[p-1] for p in pos), "__BWT__", encode=False)
        self.bwt = bwt

    def bwt_from_indexname(self, iname, reload=False):
        if (self.bwt is not None) and (not reload):
            return
        s = self.s
        containerclass = s.__class__
        bwtclass = containerclass(self.alphabet)
        bname = names.bwt(iname)
        with open(bname,"rb") as fbwt:
            b = bwtclass.fromfile(fbwt, s.manifest, self.alphabet)
        self.bwt = b

    def occ_from_bwt(self, occrate):
        occ = OccTable(self.bwt, occrate)
        occ.compute_from_bwt()
        self.occ = occ
        self.set_lcp_threshold()

    def occ_from_indexname(self, iname, occrate=0):
        """read occ table from file <iname>.<occrate>.occ.
        If occrate is not given (or <= 0), use the file with the smallest occrate.
        """
        if occrate <= 0:
            occrate, occfile = names.occtables(iname)[0]
        else:
            occfile = names.occ(iname, occrate)
        occ = OccTable(self.bwt, occrate)
        with open(occfile, "rb") as focc:
            occ.fromfile(focc)
        self.occ = occ
        self.set_lcp_threshold()

    # TODO: optimize factor, offset
    def set_lcp_threshold(self, factor=2, offset=1):
        # let k be the current interval length, n the text length
        # After cutting of the last one, it will grow to an expected asize*k,
        # needing (asize-1)*k lcp hops (good for small k)
        # For interval length k, the expected match length is
        # m = log(n/k)/log(asize), since k = n / asize**m.
        # The alternative is to do m-1 (or say, m) backward search steps,
        # which requires an expected (m-1)*occrate/2 lookups.
        # Now find the largest k such that
        # (asize-1)*k  <=  occrate/2 * log(n/k) / log(asize)
        # That k is the lcp_threshold.
        # For shorter intervals (long matches), we should go by lcp.
        # For longer intervals (short matches), we should bo by BWS.
        n = self.length
        log = math.log
        asize = self.alphabet.SIZE
        a1 = asize-1
        C = factor * self.occ.occrate / (2*log(asize))
        def lcptime(k): return a1 * k
        def bwstime(k): return C * log(n/k)
        k = 1
        while lcptime(k) <= bwstime(k):
            k += 1
        # for this k, lcptime(k) > bwstime(k), so subtract 1; then add offset
        t = int(k - 1 + offset)
        self.lcp_threshold = t
        return t


    # search methods  ###################################################
    # all high-level methods yield tuples
    # (left, right, ms, L, R)
    # TODO: is ms with respect to pattern (redundant!) or to text ?!
    # TODO: append error count k ?
    #

    def suffix_search(self, pat, minlen=0, errors=0, less=None, normalized=False):
        """
        yield the longest suffix-matches of length at least <minlen>
        of the pattern <pat> in this suffix array <self>
        with up to <errors> errors as (left, right, ms, L, R).
        """
        mspos = len(pat) - 1
        if errors == 0:
            bms = self.backward_matching_statistics(pat, begin=mspos, end=mspos, less=less, normalized=normalized)
            for (i, left, ms, L, R) in bms:
                if ms >= minlen:
                    yield (left, i, ms, L, R)
        else:
            ems = self.backward_search_with_errors(pat, errors=errors, normalized=normalized)
            for (k, ms, L, R) in ems:
                if ms >= minlen:
                    yield(mspos - ms + 1, mspos, ms, L, R)

    def prefix_search(self, pat, minlen=0, errors=0, less=None):
        """
        yield the longest prefix-matches of length at least <minlen>
        of the pattern <pat> in this suffix array <self>
        with up to <errors> errors as (left, right, ms, L, R).
        """
        bms = self.backward_matching_statistics(pat, errors=errors, less=less)
        for (i, left, ms, L, R) in bms:
            if (left == 0) and (ms >= minlen):
                yield (left, i, ms, L, R)
                break
        
    def mms(self, pat, opt=None, minlen=0, errors=0,
            begin=None, end=None, unique=False, less=None):
        """
        for all pattern-maximal [unique] matches (M[U]Ms)
        of the pattern <pat> in this suffix array <self>
        that are at least <minlen> characters long,
        yield (left, right, ms, L, R), where:
        left   is the left-hand starting position of the match in <pat>
        right  is the right-hand starting position of the match in <pat>,
        ms     is the maximal match length backward from that position,
        [L, R] is the suffix array interval of such matches.
        ((Note the reversal of left and right match position in comparison
        to self.backward_matching_statistics().))

        The tuples are yielded in order of decreasing right,
        starting at <begin>, decreasing towards <end> (both inclusive).
        The actual text positions must be obtained by self.pos[L:R+1].

        Some characters of the pattern may be markes as optional,
        using the boolean list <opt> (of the same length as the pattern).
        Note that compexity may increase as 2^(sum(opt)), so be careful.

        If the flag <unique> is set, only unique matches (L==R) are yielded.
        """
        if opt is None:
            bms = self.backward_matching_statistics(
                pat, begin=begin, end=end, errors=errors, less=less)
        else:
            if errors != 0:
                raise NotImplementedError("errors not supported with optional characters")
            bms = self.backward_matching_statistics_with_optional_characters(
                pat, opt, begin=begin, end=end, less=less)
        oldleft = len(pat)
        for (i, left, ms, L, R) in bms:
            if (left < oldleft) and (ms > 0):  # jump in matching statistics
                if ms >= minlen:  # minimum length requirement ok
                    if (not unique) or (R == L):  # unique necessitates singleton interval
                        yield (left, i, ms, L, R)
            oldleft = left

    def cumms(self, pat, opt=None, minlen=0, errors=0,
              begin=None, end=None, unique=False):
        # cumulate matching statistics above minlen for each sequence in self
        allseqs = len(self.manifest)
        cms = [0] * allseqs
        sms = [0] * allseqs
        rindex = self.rindex
        oldleft = len(pat)
        if minlen == 0:
            minlen = 1  # always at least one match
        bms = self.backward_matching_statistics_with_optional_characters(
                pat, opt, begin=begin, end=end)
        for (i, left, ms, L, R) in bms:
            if (ms >= minlen) and (left < oldleft): # jump in matching statistics
                if (not unique) or (R == L):  # unique necessitates singleton interval
                    for r in range(L, R+1):
                        idx = rindex[r]
                        cms[idx] += ms
                        if ms > sms[idx]:
                            sms[idx] = ms
            oldleft = left
        cms = sorted([(c,ix) for ix, c in enumerate(cms)], reverse=True)
        sms = sorted([(c,ix) for ix, c in enumerate(sms)], reverse=True)
        return cms, sms
        # cms[0] == (17,3) means 17 cumulated matches in seq 3 is highest
        # cms[0][0] == cms[1][0] means a tie between the two top sequences

    #######################################################################
    # lower-level functions (matching statistics, bws)
    # may have varying and different interfaces; see docstrigs.

    def backward_matching_statistics(self, pat,
                begin=None, end=None, errors=0, lcp_threshold=None,
                less=None, normalized=False):
        """
        yield backward matching statistics (i, left, ms, L, R), where:
        i      is the right-hand starting position of the match in <pat>,
        left   is the left-hand starting position of the match in <pat>
        ms     is the maximal match length backward from that position,
        [L, R] is the suffix array interval of such matches.

        The tuples are yielded in order of decreasing i,
        starting at <begin>, decreasing towards <end> (both inclusive).

        This generator requires bwt and occ of the suffix array <self>,
        but *not* pos or the sequence.
        It runs more efficiently if the lcp array is also present,
        as this avoids re-computing everything when i decreases.
        The optional <lcp_threshold> specified, up to which interval length
        the lcp-method should be used to cut off the rightmost character.
        For longer intervals (short matches), everything is re-computed.
        """
        if errors != 0:
            raise NotImplementedError("error-tolerant matching statistics not yet supported")
        n = self.length
        m = len(pat)
        if (begin is None) or (begin > m - 1):
            begin = m - 1
        if (end is None) or (end < 0):
            end = 0
        if end > begin:
            end = begin
        lcp = self.lcp
        if lcp is not None:
            lcp = lcp.at
        else:
            lcp_threshold = -1
        if lcp_threshold is None:
            lcp_threshold = self.lcp_threshold
        if not normalized:
            fre = self.occ.firstregular
            pat = [a - fre for a in pat]
            normalized = True
        if less is None:
            ls = self.occ.less_reg
            less = [ls(a) for a in pat]
        occ = self.occ.at_reg

        j = begin
        for i in range(begin, end-1, -1):
            # start matching backward at position i of the pattern
            # assume that j is set to next position to examine
            if j >= i:  # reset
                j = i
                (L, R) = (0, n-1)
            while j >= 0:
                # cannot use "for j in range(i,-1,-1)" because of break/termination
                # update L,R by prepending letter <a>
                a = pat[j]
                ls = less[j]  # returns a negative value for illegal character
                if ls < 0:
                    break  # failure, keep old interval
                Lnew = ls + occ(L-1, a)
                Rnew = ls + occ(R, a) - 1
                if Lnew > Rnew:
                    break  # failure, keep old interval
                L, R = Lnew, Rnew
                j -= 1
            # successful backward match found at i, of length i - j
            ms = i - j
            yield (i, j+1, ms, L, R)
            # prepare j for the next i (which is i-1)
            if R-L > lcp_threshold:  # always True if lcp is None
                # long interval: recompute next ms from scratch
                ###if ms <= 0:
                    ###assert j == i  and L == 0 and R == n-1  # nothing was matched
                j = i
            else:
                # long match, so widen (L,R) using lcp array
                ms -= 1
                ###assert lcp(L) <= ms and (R == n - 1 or lcp(R+1) <= ms)
                while lcp(L) >= ms:
                    L -= 1
                while (R < n-1) and (lcp(R+1) >= ms):
                    R += 1


    def backward_matching_statistics_with_optional_characters(
        self, pat, opt=None, begin=None, end=None, lcp_threshold=None,
        less=None, normalized=False):
        """yield backward matching statistics of pattern <pat>
        with some characters marked as optional via a boolean list <opt>
        Matching statistics are yielded as tuples (i, len, L, R),
        where i is the starting position of the match in <pat>,
        len is the maximal match length backward from that position,
        and [L, R] is the suffix array interval of such matches.
        Requires bwt and occ of the suffix array, but *not* pos or the sequence.
        """
        # internal representation of suffix array intervals:
        # (ms, i, j, L, R, skipped), where
        #   ms = #matched characters (w/o skipped)
        #    i = rightmost position of match in pattern
        #    j = leftmost position of match in pattern
        #  L,R = suffix array interval
        #  skipped = tuple of skipped pattern positions
        n = self.length
        m = len(pat)
        if (begin is None) or (begin > m - 1):
            begin = m - 1
        if (end is None) or (end < 0):
            end = 0
        if end > begin:
            end = begin
        if opt is None:
            opt = [False] * m

        if lcp_threshold is None:
            lcp_threshold = self.lcp_threshold
        lcp = self.lcp
        if lcp is not None:
            lcp = lcp.at
        else:
            lcp_threshold = -1

        cutlast = self._cut_last
        extend = self._extend
        if not normalized:
            fre = self.occ.firstregular
            pat = [a - fre for a in pat]
            normalized = True
        if less is None:
            ls = self.occ.less_reg
            less = [ls(a) for a in pat]
        occ = self.occ.at_reg

        intervals = []
        for i in range(begin, end-1, -1):
            # cut off last character for each interval for current i
            extended_intervals, cut_intervals = cutlast(
                intervals, i, pat, lcp, lcp_threshold, n, less, normalized)
            #intervals.sort()
            if not extended_intervals and not cut_intervals:
                cut_intervals = [(0, i+1, 0, n-1, tuple())]
            # extend each interval
            intervals = extend(i, extended_intervals, cut_intervals, pat, less, opt, occ)
            intervals.sort()
            ###assert len(intervals) >= 1
            # report longest interval
            ###for iv in intervals: print("       ", iv)
            (ms, j, L, R) = intervals[-1][:4]
            yield (i, j, ms, L, R)


    def _cut_last(self, intervals, i, pat, lcp, lcp_threshold, n, less, normalized):
        cut_intervals = []
        extended_intervals = []
        prev = None
        for interval in intervals:
            if interval == prev:
                continue
            prev = interval
            (ms, j, L, R, skipped) = interval
            oL, oR = L, R
            # update i+1 -> i,  so remove i+1 from skipped
            if skipped and skipped[0] == i+1:
                skipped = skipped[1:]
            else:
                ms -= 1
                if ms < 0:
                    continue
            ###assert all(skip < i+1 for skip in skipped), str((ms,i+1,j,L,R,skipped))
            # update L, R
            if R-L > lcp_threshold:  # always True if lcp is None
                # for a wide interval (short match), re-compute from scratch
                matched = pat[j:i+1]
                matched_less = less[j:i+1]
                for k in skipped:
                    if k >= j:
                        del matched[k-j]
                        del matched_less[k-j]
                (_, _, _, L, R) = next(iter(self.suffix_search(matched, less=matched_less, normalized=normalized)))
                ###assert len(iv) == 1,  "{} / {}".format(iv, matched)
            else:
                # for a narrow interval (long match), cut by lcp
                ###assert lcp(L) <= ms and (R == n - 1 or lcp(R+1) <= ms)
                while lcp(L) >= ms:
                    L -= 1
                while (R < n-1) and (lcp(R+1) >= ms):
                    R += 1
            if (L, R) == (oL, oR):
                extended_intervals.append((ms, j, L, R, skipped))
            else:
                cut_intervals.append((ms, j, L, R, skipped))
        return extended_intervals, cut_intervals

    def _extend(self, i, extended_intervals, cut_intervals, pat, less, opt, occ):
        intervals = cut_intervals
        for (ms, j, L, R, skipped) in intervals:
            # j is the last position that was successfully matched
            while j > 0:
                jnew = j - 1  # attempt the next j
                if opt[jnew] and jnew < i:  # branch by skipping this jnew
                    intervals.append((ms, jnew, L, R, skipped+(jnew,)))
                # attempt to update [L,R]
                ls = less[jnew]  # returns a negative value for illegal character
                if ls < 0:
                    break  # failure, keep old interval
                a = pat[jnew]
                Lnew = ls + occ(L-1, a)
                Rnew = ls + occ(R, a) - 1
                if Lnew > Rnew:
                    break  # failure, keep old interval
                L, R, j = Lnew, Rnew, jnew
                ms += 1
            extended_intervals.append((ms, j, L, R, skipped))
        return extended_intervals


    def backward_search_with_errors(self, pat, errors=0, normalized=False):
        # error-tolerant matching inspired by NFA
        # after an idea by Dominik Kopczynski
        # execute row-by-row.
        m = len(pat)
        n = self.length
        o = self.occ.all_at
        if not normalized:
            fre = self.occ.firstregular
            pat = [a - fre for a in pat]
            normalized = True
        allless = self.occ._less
        firstreg = self.occ.firstregular
        regulars = self.occ.regulars
        thisrow = [set() for j in range(m+1)]
        thisrow[0] = set([(0,n-1)])
        for k in range(errors+1):
            # thisrow has received updated values from the previous row.
            # Process cells left-to-right.
            nextrow = [set() for j in range(m+1)]
            for j in range(m+1):
                intervals = thisrow[j]
                if len(intervals) == 0:
                    ###assert j > 0
                    for (L,R) in thisrow[j-1]:
                        yield (k, j-1, L, R)
                    break
                if j == m:
                    for (L,R) in intervals:
                        yield (k, m, L, R)
                #a = pat[m-1-j] - firstreg  # j==0 -> pat[m-1]
                a = pat[m-1-j]  # j==0 -> pat[m-1]
                for (L,R) in intervals:
                    # compute list of [L,R] updates with each character
                    ###assert L <= R
                    LL = o(L-1)
                    RR = o(R)
                    for c, ls in enumerate(allless):
                        LL[c] += ls
                        RR[c] += ls - 1
                    if k < errors:
                        # insertion
                        for (l,r) in zip(LL,RR):
                            if l <= r:
                                nextrow[j].add((l,r))
                        if j < m:
                            # substitution
                            for c, (l,r) in enumerate(zip(LL,RR)):
                                if (c != a) and (l <= r):
                                    nextrow[j+1].add((l,r))
                            # deletion
                            nextrow[j+1].add((L,R))
                    # match
                    if (j < m) and (0 <= a < regulars):
                        l = LL[a]
                        r = RR[a]
                        if l <= r:
                            thisrow[j+1].add((l,r))
            # done processing a whole row => swap rows
            thisrow = nextrow

############################################################################        
