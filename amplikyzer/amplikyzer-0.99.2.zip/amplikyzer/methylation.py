# amplikyzer.methylation
# (c) Sven Rahmann 2011--2013

# FIXME: update docstring for NOMe-seq modes
"""
Analyze the Cs and CpGs of an alignment for methylation.
Reads can be selected for conversion rate and valid CpGs.
Output the results as text or as image.
Two types of analyses exist (selected by the --type option).

(1) Individual sample analysis:
Show the methylation state of each CpG in each read
of a given set of reads selected by locus, MID, and allele.

(2) Comparative analysis:
shows the methylation rate of each CpG in each read set for a given locus.
The read set is specified my MID and/or allele.

"""

import sys
import os.path
from random import random
from collections import namedtuple, OrderedDict
from operator import itemgetter
from functools import partial
from itertools import tee

from .core import *
from . import utils
from . import align
from . import graphics


AnalysisMode = namedtuple("AnalysisMode",
                          ["text", "meth_pattern", "neutral_pattern"])
MODES = {"cg":   AnalysisMode("CpG", ("CG" , 0), ("CH" , 0)),
         "gch":  AnalysisMode("GpC", ("GCH", 1), ("HCH", 1)),
         "nome": AnalysisMode("GpC", ("GCH", 1), ("HCH", 1)),
         "hcg":  AnalysisMode("CpG", ("HCG", 1), ("HCH", 1)),
         "gcg":  AnalysisMode("GpCpG", ("GCG", 1), ("HCH", 1)),
         "wcg":  AnalysisMode("CpG", ("WCG", 1), ("HCH", 1))}
MODES_LIST = ("cg", "gch", "nome", "hcg", "gcg", "wcg")  # valid modes
ALL_MODES_LIST = ("cg", "gch", "hcg", "gcg", "wcg")  # modes without aliases ("all" choice)

############################################################
# build parser

def buildparser(p):
    """populate the ArgumentParser p with options"""
    align.buildparser_common(p)  # re-use some of align's arguments

    p.add_argument("--mode",
        nargs="+", choices=MODES_LIST + ("all",), default=[MODES_LIST[0]],
        help="analysis mode (pattern) [default: cg;  nome==gch]")
    p.add_argument("--type", "-t",
        choices=("individual", "comparative", "all", "smart"), default="smart",
        help="type of methylation analysis (individual or comparative)")
    p.add_argument("--format", "-f",
        choices=("png", "svg", "pdf", "text", "txt"), default="png",
        help="output format ('text' or image type)")
    p.add_argument("--style",
        choices=("color", "bw"), default="color",
        help="output style for images (color or bw)")
    p.add_argument("--conversionrate", "-c",
        type=float, metavar="FLOAT", default=0.95,
        help="minimum bisulfite conversion rate for using a read")
    badmeth = p.add_mutually_exclusive_group()
    badmeth.add_argument("--badmeth", "-b",
        type=float, metavar="INT/FLOAT", default=2.0,
        help=("max number (>=1) or rate (<1.0) of undetermined CpG "
              "(GpC for mode 'nome') states to use a read"))
    #badmeth.add_argument("--badcpgs",
    #    type=float, metavar="INT/FLOAT",
    #    help="[deprecated] alias for --badmeth.")
    p.add_argument("--outpath", "-o",
        metavar="PATH", default=DEFAULT_METHYLATIONPATH,
        help="output path (joined to --path; use '-' for stdout)"),
    p.add_argument("--analysisfiles",
         nargs="+", metavar="FILE", default=["*"+EXT_AMPLIKYZER],
        help="analysis file(s) from which to generate the alignment(s)")
    show = p.add_mutually_exclusive_group()
    show.add_argument("--show",
        nargs="+", choices=("index", "position", "c-index"), default=["index"],
        help="show indices, positions or cytosine indices. ")
    #show.add_argument("--showpositions", "-p",
    #    action="store_true",
    #    help="show CpG (GpC for mode 'nome') positions instead of simple indices."
    #         " Synonym for '--show position'")
    p.add_argument("--sort", "-s",
        nargs="+", metavar="OPTION", default=["meth:down"],
        help=("by methylation ('meth:down', 'meth:up'), "
              "given MIDs ('mids:MID17,MID13,...'), "
              "alleles ('alleles:GA,GG,CA,CG')") )
    p.add_argument("--includemode",
        action="store_true",
        help="include analysis mode (option --mode) in output file names. "
             "Implicit when analyzing in more than one mode")


############################################################
# comparative methylation analysis

# attribute order determines sorting order
SampleSummary = namedtuple("SampleSummary",
                           ["total_meth_rate",
                            "allele",
                            "mid",
                            "label",
                            "nreads",
                            "meth_rates",
                            "meth_positions",
                            "meth_c_indices"])


class ComparativeAnalysis:
    """
    Comparative methylation analysis of one locus
    between different individuals (MIDs).
    """
    def __init__(self, mode, locus, allele=None, mid=None, label=None, remark=None):
        self.mode = mode
        self.locus = locus
        self.allele = allele
        self.mid = mid  # only if mid is constant, generally not specified
        self.label = label  # only if mid is constant, generally not specified
        self.remark = remark  # string, any user-defined remark for plots
        self._samples = []  # private list of individual analyses

    def __len__(self):
        return len(self._samples)

    @property
    def shape(self):
        """matrix shape: a pair (number of samples, number of CpGs (GpCs for 'nome'))"""
        samples = self._samples
        if not samples:
            return (0, 0)
        nrows = len(samples)
        ncols = len(samples[0].meth_rates)
        if any(ncols != len(a.meth_rates) for a in samples):
            return (nrows, None)
        return (nrows, ncols)

    @property
    def meth_positions(self):
        """list of reference positions of CpGs (GpCs for 'nome'); or None if inconsistent"""
        samples = self._samples
        if not samples:
            return None

        pos = samples[0].meth_positions
        if any(pos != a.meth_positions for a in samples):
            return None
        return pos

    @property
    def meth_c_indices(self):
        samples = self._samples
        if not samples:
            return None

        indices = samples[0].meth_c_indices
        if any(indices != a.meth_c_indices for a in samples):
            return None
        return indices

    @property
    def title(self):
        L = [self.locus]
        if self.allele is not None:
            L.append(self.allele)
        if self.label is not None:
            L.append(self.label)
        return " / ".join(L)

    def add_sample(self, s):
        if not isinstance(s, SampleSummary):
            raise TypeError("argument 's' must be a SampleSummary instance")
        self._samples.append(s)

    def sample_names(self):
        """
        yield a minimal printable name
        for each SampleSummary in this ComparativeAnalysis
        """
        for s in self._samples:
            name = []
            if self.label is None:
                name.append(s.label)
            if self.allele is None:
                name.append(s.allele)
            yield " ".join(name)

    def sort(self, sortoption):
        """sort the samples in this comparative analysis by the given option"""
        logs = []
        so = sortoption.lower()
        if so in {"meth:up", "meth"}:
            self._samples.sort()
        elif so in {"meth:dn", "meth:down"}:
            self._samples.sort(reverse=True)
        elif so.startswith("mids:"):
            # sort by given MIDs
            mids = [m.strip() for m in sortoption[len("mids:"):].split(",")]
            result = list()
            for mid in mids:
                found = [s for s in self._samples if s.mid == mid]
                result.extend(found)
                if not found:
                    logs.append("Warning: MID '{}' not found in samples."
                                .format(mid))
            self._samples = result
        elif so.startswith("alleles:"):
            # sort comparative analysis by given alleles
            alleles = [a.strip() for a in sortoption[len("alleles:"):].split(",")]
            result = list()
            for allele in alleles:
                found = [s for s in self._samples if s.allele.startswith(allele)]
                result.extend(found)
            self._samples = result
        else:
            raise ValueError("unknown --sort option '{}'".format(sortoption))
        return logs

    def as_matrix(self):
        """return a samples x CpG (GpC for 'nome') matrix (list of lists) of methylation rates"""
        return [s.meth_rates for s in self._samples]

    def write(self, fname, format, style, options=None):
        """
        write the comparative analysis to file named <fname>,
        according to <format> (text/image) and <style> (bw/color),
        using the given options dictionary (showpositions).
        Return the success state.
        """
        if format in ("text", "txt"):
            m, n = self.shape
            if n is None:
                return False
            if fname == "-":
                result = self.write_text(sys.stdout, style, options)
            else:
                with open(fname + ".txt", "wt") as f:
                    result = self.write_text(f, style, options)
        elif format in ("png", "svg", "pdf"):
            if fname != "-":
                fname = fname + "." + format
            result = graphics.plot_comparative(self, fname, format, style, options)
        else:
            raise ArgumentError("Output format '{}' not implemented".format(format))
        return result


    def write_text(self, f, style=None, options=None):
        pos = self.meth_positions
        if pos is None:
            return False

        fprint = partial(print, file=f)

        fprint("Comparative Analysis of {}".format(self.title))
        if self.remark is not None:
            fprint(self.remark)
        m, n = self.shape
        fprint("{} samples, {} {}s".format(m, n, self.mode.text), end="\n\n")
        if m == 0 or n == 0:
            return False

        if options is None:
            options = dict()

        for pos_type in options.get("show", ["index"]):
            if pos_type == "position":
                fprint(" ".join(["@{:d}".format(p) for p in pos]))
            elif pos_type == "c-index":
                fprint(" ".join(["c{:d}".format(c) for c in self.meth_c_indices]))
            else: #  pos_type == "index":
                fprint(" ".join(["#{:d}".format(i+1) for i in range(len(pos))]))

        for s, name in zip(self._samples, self.sample_names()):
            # s is a SampleSummary instance
            fprint(name, end=" ")
            fprint("".join(["{:4.0%} ".format(x) for x in s.meth_rates]), end="")
            fprint(" ({:5.1%}, {:4d} reads)".format(s.total_meth_rate, s.nreads))
        return True


############################################################
# individual methylation analysis class

class MethylationAnalysis(align.Alignment):
    """MethylationAnalysis annotates an Alignment with methylation information"""

    def __init__(self, mode, locus, allele, mid, label, builder,
                 minconvrate=0.0, maxbadmeth=0.99999, remark=None):
        """
        set attributes
            .rows: selected rows from alignment passing filter
            .meth_positions: positions of CpGs (GpCs for 'nome') in reference (1-based)
            .meth_rates: methylation rate per CpG (GpC for 'nome')
            .conversion_rates: bisulfite conversion rate per read
            .bad_meth_rates: fraction of unidentified CpG (GpC for 'nome') status per read
            .read_meth_rates: methylation rate per read
            .total_meth_rate:  overall methylation rate (float)
        """
        super().__init__(locus, allele, mid, label, builder, mode.meth_pattern, remark)
        self.mode = mode
        refpos = self.builder.refpos_for_col
        self.meth_positions = [refpos[c]+1 for c in self.columns]
        c_indices = {c:i for i,c in enumerate(self.choose_columns(("C",0)))}
        self.meth_c_indices = [c_indices[c]+1 for c in self.columns]
        # compute initial per-read statistics
        (convrates, badrates, _) = self.per_read_statistics()
        # pick rows with sufficient conversion rate and reduce alignment
        maxbadrate = maxbadmeth/self.ncols if maxbadmeth >= 1.0 else maxbadmeth
        self.rows = [i for i,c,b in zip(self.rows, convrates, badrates)
                     if c >= minconvrate and b <= maxbadrate]
        # re-compute per-read statistics for selected rows
        (self.conversion_rates, self.bad_meth_rates, self.read_meth_rates) = self.per_read_statistics()
        # compute column and overall methylation rates
        (self.meth_rates, self.total_meth_rate) = self.per_pos_and_overall_statistics()
        self.sort("random")


    def sort(self, sortoption):
        """re-sort the individual reads according to a given sort option"""
        # permutes self.rows according to sort option.
        # consequently also permutes
        # self.read_meth_rates, self.conversion_rates, self.bad_meth_rates
        so = sortoption.lower()
        L = len(self.rows)
        permutation = list(range(L))  # identity permutation
        if so == "random":
            permutation.sort(key=lambda i: random())
        elif so in {"meth:up", "meth"}:
            permutation.sort(key=lambda i: self.read_meth_rates[i])
        elif so in {"meth:dn", "meth:down"}:
            permutation.sort(key=lambda i: self.read_meth_rates[i], reverse=True)
        elif so.startswith("mids:"):
            # ignore sorting by MID here, makes no sense
            pass
        elif so.startswith("alleles:"):
            alleles = [a.strip() for a in sortoption[len("alleles:"):].split(",")]
            rowalleles = [self.builder.alleles[r] for r in self.rows]
            permutation = list()
            for allele in alleles:
                found = [i for (i,a) in enumerate(rowalleles) if a.startswith(allele)]
                permutation.extend(found)
            # TODO: might be necessary to check 'len(permutation) == L'
        else:
            raise ValueError("unknown --sort option '{}'".format(sortoption))
        for attr in (self.rows, self.read_meth_rates,
                     self.conversion_rates, self.bad_meth_rates):
            assert len(attr) == L
            attr[:] = [attr[i] for i in permutation]


    def per_read_statistics(self):
        """
        Return 3 lists:
        (conversion_rates, bad_meth_rates, read_methylation_rates).
        Each list contains one value (a rate) for each read.
        """
        bcols = self.builder.columns
        nrows = len(self.rows)
        neutral_columns = self.filter_columns(*self.mode.neutral_pattern)
        meth_columns = self.filter_columns(*self.mode.meth_pattern)
        convrates = [0.0] * nrows
        methrates = [0.0] * nrows
        badrates = [1.0] * nrows
        for i, r in enumerate(self.rows):
            neutral_good = neutral_bad = 0
            for j in neutral_columns:
                seen = bcols[j][r]
                if seen == "T":
                    neutral_good += 1
                elif seen == "C":
                    neutral_bad += 1

            meth = unmeth = bad_meth = 0
            for j in meth_columns:
                seen = bcols[j][r]
                if seen == "T":
                    unmeth += 1
                elif seen == "C":
                    meth += 1
                else:
                    bad_meth += 1
            total_meth = unmeth + meth + bad_meth

            if neutral_good > 0:
                convrates[i] = neutral_good / (neutral_good + neutral_bad)
            if total_meth > 0:
                badrates[i] = bad_meth / total_meth
            if meth > 0:
                methrates[i] = meth / (meth + unmeth)
        return (convrates, badrates, methrates)

    def per_pos_and_overall_statistics(self):
        """
        Return a pair of a list and a float:
        (methylation_rates, total_methylation_rate).
        The list contains the methylation rate for each CpG (GpC for 'nome') in order.
        """
        bcols = self.builder.columns
        rows = self.rows
        meth_columns = self.filter_columns(*self.mode.meth_pattern)
        rates = [0.0] * len(meth_columns)
        total_meth = total_unmeth = 0
        for i, j in enumerate(meth_columns):
            col = bcols[j]
            meth = unmeth = 0
            for r in rows:
                seen = col[r]
                if seen == "T":
                    unmeth += 1
                elif seen == "C":
                    meth += 1
            if meth > 0:
                rates[i] = meth / (meth + unmeth)
            total_meth += meth
            total_unmeth += unmeth
        total_rate = 0.0
        if total_meth > 0:
            total_rate = total_meth / (total_meth + total_unmeth)
        return (rates, total_rate)

    def as_matrix(self):
        """
        Return CpG (GpC for 'nome) methylation states as matrix (list of lists).
        Each value is in {0: unmethylated, 0.5: unknown, 1: methylated}.
        """
        getread = self.builder.get_read
        conv = self.reduce_row_to_style
        return [conv(getread(row), "bisulfite_numeric", *self.mode.meth_pattern)
                for row in self.rows]

    def write(self, fname, format, style, options=None):
        """
        write the analysis to file named <fname>,
        according to <format> and <style>.
        """
        if format in ("text", "txt"):
            if fname == "-":
                self.write_text(sys.stdout, style, options)
            else:
                with open(fname + ".txt", "wt") as f:
                    self.write_text(f, style, options)
        elif format in ("png", "svg", "pdf"):
            if fname != "-":
                fname = fname + "." + format
            graphics.plot_individual(self, fname, format, style, options)
        else:
            raise ArgumentError("Output format '{}' not implemented".format(format))


    def write_text(self, f, style=None, options=None):
        fprint = partial(print, file=f)

        fprint("Methylation Analysis of {}".format(self.title))
        if self.remark is not None:
            print(self.remark)
        fprint("{} reads, {} {}s".format(self.nrows, self.ncols, self.mode.text))
        if self.nrows == 0 or self.ncols == 0:
            return

        fprint("Methylation rate: {:.1%}\n".format(self.total_meth_rate))
        fprint(" ".join(["{:.0%}".format(m) for m in self.meth_rates]))

        if options is None:
            options = dict()

        pos = self.meth_positions
        for pos_type in options.get("show", ["index"]):
            if pos_type == "position":
                fprint(" ".join(["@{:d}".format(p) for p in pos]))
            elif pos_type == "c-index":
                fprint(" ".join(["c{:d}".format(c) for c in self.meth_c_indices]))
            else:  # pos_type == "index"
                fprint(" ".join(["#{:d}".format(i+1) for i in range(len(pos))]))

        getread = self.builder.get_read
        for r, m in zip(self.rows, self.read_meth_rates):
            row = self.reduce_row_to_style(getread(r), "bisulfite", *self.mode.meth_pattern)
            fprint("{} {:4.0%}".format(row, m))

    def write_fasta(self, f, style=None, genomicname=None, options=None):
        raise NotImplementedError("FASTA format not available for MethylationAnalysis")


############################################################
# main routine

def individual_analyses(mode_name, builders, alleles, labels, args):
    mode = MODES[mode_name]
    for aps in align.all_alignment_parameters(builders, alleles, args.minreads):
        # produce a new individual sample MethylationAnalysis
        (locus, allele, mid, builder) = aps
        label = utils.get_label(labels, mid, locus)
        ma = MethylationAnalysis(mode, locus, allele, mid, label, builder,
                                 args.conversionrate, args.badmeth,
                                 remark=args.remark)
        if ma.nrows < args.minreads:
            continue
        # sort the reads according to sort options
        for sortoption in reversed(args.sort):
            ma.sort(sortoption)
        yield ma


def comparative_analyses(mode_name, mas, args):
    mode = MODES[mode_name]
    cas = dict()  # locus -> ComparativeAnalysis instance
    for ma in mas:
        if ma.locus not in cas:
            cas[ma.locus] = ComparativeAnalysis(mode, ma.locus, remark=args.remark)
        # collect summary information of this individual sample analysis
        asy = SampleSummary(ma.total_meth_rate, ma.allele, ma.mid,
                            ma.label, ma.nrows, tuple(ma.meth_rates),
                            tuple(ma.meth_positions), tuple(ma.meth_c_indices))
        cas[ma.locus].add_sample(asy)
    for _, ca in sorted(cas.items(), key=itemgetter(0)):
        # sort and filter the samples of the comparative analysis
        logs = []
        for sortoption in reversed(args.sort):
            logs.extend(ca.sort(sortoption))
        if (len(ca) == 0) or (len(ca) < 2 and args.type == "smart"):
            continue
        yield ca, logs


def write_individual(mode_name, args, style, outpath, ma):
    afname = "__".join((ma.locus, ma.allele, ma.mid, "individual", style))
    if args.includemode:
        afname = "__".join((afname, mode_name))
    outname = "-" if outpath == "-" else os.path.join(outpath, afname)
    options = {"show": args.show}
    ma.write(outname, args.format, args.style, options)
    return "Individual Analysis {}: {} reads, {} {}s".format(
           afname, ma.nrows, ma.ncols, ma.mode.text)


def write_comparative(mode_name, args, style, outpath, ca_sort_logs):
    ca, sort_logs = ca_sort_logs
    afname = "__".join((ca.locus, "comparative", style))
    if args.includemode:
        afname = "__".join((afname, mode_name))
    outname = "-" if outpath == "-" else os.path.join(outpath, afname)
    options = {"show": args.show}
    result = ca.write(outname, args.format, args.style, options)
    logs = list(sort_logs)
    logs.append("Comparative Analysis {}: {} individual samples"
                .format(afname, len(ca)))
    if not result:
        # failed because of different number of analyzed positions
        logs.append("Comparative Analysis {}: FAILED, different numbers of {}s"
                    .format(afname, ca.mode.text))
    return "\n".join(logs)


def analyze_methylation(mode_name, builders, alleles, labels,
                        args, outpath, style, map_):
    mas = individual_analyses(mode_name, builders, alleles, labels, args)
    mas, mas_for_cas = tee(mas)

    mas_logs, cas_logs = (), ()

    # output individual results if desired
    if args.type in ("individual", "all", "smart"):
        write = partial(write_individual, mode_name, args, style, outpath)
        mas_logs = map_(write, mas)

    if args.type != "individual":
        cas = comparative_analyses(mode_name, mas_for_cas, args)
        write = partial(write_comparative, mode_name, args, style, outpath)
        cas_logs = map_(write, cas)

    return mas_logs, cas_logs


def print_logs(mas_logs, cas_logs, args, clock, log):
    analyzed = 0
    # output individual results if desired
    if args.type in ("individual", "all", "smart"):
        for log_msg in mas_logs:
            analyzed += 1
            log(log_msg)
    else:
        analyzed += sum(1 for _ in mas)

    # done processing all alignments.
    log(clock.toc(), "Analyzed {} alignments"
                     " with >= {} reads with conversion >= {}"
                     .format(analyzed, args.minreads, args.conversionrate))

    # next, do comparison analysis, if requested
    if args.type != "individual":
        analyzed = 0
        for log_msg in cas_logs:
            analyzed += 1
            log(log_msg)
        log(clock.toc(), "Finished comparative analysis for {} loci"
                         .format(analyzed))


def main(args):
    clock = utils.TicToc()  # get a new clock
    log = partial(print, file=sys.stdout)

    if args.badcpgs is not None:
        log("Warning: '--badcpgs' is deprecated,"
            " use alias '--badmeth' instead.")
        args.badmeth = args.badcpgs

    if args.showpositions:
        log("Warning: '--showpositions' is deprecated,"
            " use '--show position' instead.")
        args.show = ["position"]

    style = "simple" if args.format in ("text", "txt") else args.style

    if args.outpath == "-":
        outpath = "-"
    else:
        outpath = os.path.join(args.path, args.outpath)
        utils.ensure_directory(outpath)

    # read labels from config files
    log(clock.toc(), "Reading configuration information...")
    configinfo = utils.read_config_files(args.path, args.conf)
    labels = utils.labels_from_config(configinfo)

    # determine list of alleles to process, must not be empty
    alleles = list(args.alleles)
    if not alleles:
        alleles = [""]

    with utils.get_executor(args.parallel) as executor:
        # build all required alignments
        log(clock.toc(), "Building all requested alignments...")
        builders = align.build_alignments(args.path, args.analysisfiles,
                                          args.loci, args.mids, executor)
        # process all alignments to produce each individual sample analysis
        log(clock.toc(), "Formatting alignments...")

        mode_names = OrderedDict.fromkeys(args.mode)
        if "all" in mode_names:
            mode_names.update(OrderedDict.fromkeys(ALL_MODES_LIST))
            del mode_names["all"]
        if len(mode_names) > 1:
            args.includemode = True

        map_ = map if outpath == "-" else executor.map

        mode_names_builders = zip(tee(builders, len(mode_names)), mode_names)
        mas_cas_logs = (analyze_methylation(mode_name, bs, alleles, labels,
                                            args, outpath, style, map_)
                        for bs, mode_name in mode_names_builders)

        for (mas_logs, cas_logs) in mas_cas_logs:
            print_logs(mas_logs, cas_logs, args, clock, log)
            
