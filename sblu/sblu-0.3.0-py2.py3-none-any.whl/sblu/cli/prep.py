import os
import tempfile

import click
from path import Path

from ..pdb import (parse_pdb_stream, fix_atom_records, split_segments,
                   SKIP_RESIDUES, RESNAME_FIXES, RECORD_FIXES)


@click.command()
@click.argument("pdb_file", type=click.File(mode='r'))
@click.option("--all-het-to-atom",
              is_flag=True,
              help="Change all HETATM records to ATOM")
@click.option("--no-skips",
              is_flag=True,
              help="Skip the following residues: " + " ".join(SKIP_RESIDUES))
@click.option(
    "--no-record-fixes",
    is_flag=True,
    help="Change the record_type to ATOM for the following residues: " +
    " ".join(RECORD_FIXES))
@click.option("--no-resname-fixes",
              is_flag=True,
              help="Fix the following residue names:\n" + "\n".join([
                  '\t{} -> {}'.format(k, v) for k, v in list(RESNAME_FIXES.items())
              ]))
@click.option("--outfile",
              type=click.File(mode='w'),
              default=click.open_file('-', 'w'))
def clean(pdb_file, all_het_to_atom, no_skips, no_record_fixes,
          no_resname_fixes, outfile):
    records = fix_atom_records(parse_pdb_stream(pdb_file),
                               no_skips=no_skips,
                               all_het_to_atom=all_het_to_atom,
                               no_record_fixes=no_record_fixes,
                               no_resname_fixes=no_resname_fixes)

    for record in records:
        outfile.write(str(record))


@click.command()
@click.argument("pdb_file", type=click.File(mode='r'))
@click.option("--renum", is_flag=True, help="Renumber residues")
@click.option("--segid/--no-segid", default=True)
@click.option("--output-prefix",
              default=None,
              help="Use this prefix for the output files.")
def splitsegs(pdb_file, renum, segid, output_prefix):
    records = parse_pdb_stream(pdb_file)

    if output_prefix is None:
        if pdb_file.name != "<stdin>":
            output_prefix = os.path.splitext(pdb_file.name)[0]
        else:
            output_prefix = "split_pdb"

    for (segment, chain, segid) in split_segments(records, add_segid=segid):
        out_file = "{}-{}.{:04d}.pdb".format(output_prefix, chain, segid)

        with open(out_file, "w") as ofp:
            for record in segment:
                ofp.write(str(record))


@click.command()
@click.argument("segments")
@click.option("--link")
@click.option("--first")
@click.option("--last")
@click.option("--smod", default="")
@click.option("--wdir")
@click.option("--psfgen", default="psfgen")
@click.option("--nmin", default="nmin")
@click.option("--prm")
@click.option("--rtf")
@click.option("--nsteps", default=1000, type=click.INT)
@click.option("--auto-disu/--no-auto-disu", default=True)
@click.option("--osuffix")
def psfgen(segments):
    pass


@click.command()
@click.argument("pdb_file", type=click.File(mode='r'))
@click.argument("psf_file", type=click.File(mode='r'))
def nmin(pdb_file, psf_file):
    pass


@click.command()
@click.option("--clean/--no-clean", default=True)
@click.option("--minimize/--no-minimize", default=True)
@click.option("--xplor-psf/--no-xplor-psf", default=False)
def prep(pdb_file, chains, minimize, outfile):
    workdir = tempfile.mkdtemp()
    workdir = Path(workdir)

    cleaned = workdir / "cleaned.pdb"
    with open(cleaned, "w") as f:
        clean(pdb_file, all_het_to_atom=False, outfile=f)

    with open(cleaned, "r") as inp:
        segments = splitsegs(cleaned)

    outputs = psfgen(segments)
    if minimize:
        nmin(None, None)

    pass
