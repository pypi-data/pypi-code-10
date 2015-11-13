import sys
import click

import numpy as np
from prody import parsePDB, parsePDBStream
from sblu.rmsd import rmsd, interface, interface_pwrmsd
from sblu.rmsd import pwrmsd as pwrmsd_func
from sblu.ft import (read_rotations, read_ftresults_stream,
                     apply_ftresults_atom_group)


@click.command()
@click.argument("pdb_crys", type=click.Path(exists=True))
@click.argument("pdb_files", type=click.Path(exists=True), nargs=-1)
@click.option("--only-CA", is_flag=True, help="Only C-alpha atoms")
@click.option("--only-backbone", is_flag=True, help="Only backbone atoms")
@click.option("--only-interface", is_flag=True, help="Only interface atoms")
@click.option("--interface-radius", type=click.FLOAT, default=10.0)
@click.option("--rec",
              type=click.Path(exists=True),
              help="PDB to use for calculating interface")
@click.option("--oneline", is_flag=True)
def srmsd(pdb_crys, pdb_files, only_ca, only_backbone, only_interface,
          interface_radius, rec, oneline):
    if only_interface and rec is None:
        click.echo("--only-interface requires --rec")
        sys.exit(1)

    crys = parsePDB(pdb_crys)
    pdbs = (parsePDB(f) for f in pdb_files)

    if only_ca:
        crys = crys.calpha
        pdbs = tuple(map(lambda p: p.calpha, pdbs))
    elif only_backbone:
        crys = crys.backbone
        pdbs = tuple(map(lambda p: p.backbone, pdbs))

    crys_coords = crys.getCoords()
    pdb_coords = (p.getCoords() for p in pdbs)

    if only_interface:
        rec = parsePDB(rec)
        i = interface(rec, crys, interface_radius)

        crys_coords = crys_coords[i]
        pdb_coords = (c[i] for c in pdb_coords)

    rmsds = (str(rmsd(crys_coords, coords)) for coords in pdb_coords)
    sep = "\n"
    if oneline:
        sep = ","

    print(sep.join(rmsds))


@click.command()
@click.argument("pdb_file", type=click.Path(exists=True))
@click.argument("ftfile", type=click.File(mode='r'))
@click.argument("rotprm", type=click.File(mode='r'))
@click.option("--sort-ftresults",
              is_flag=True,
              help="Sort ftresults before using")
@click.option("-n", "--nftresults",
              type=click.INT,
              default=1000,
              help="Number of ftresults to use")
@click.option("--only-CA", is_flag=True, help="Only C-alpha atoms")
@click.option("--only-backbone", is_flag=True, help="Only backbone atoms")
@click.option("--interface", is_flag=True)
@click.option("--interface-radius", type=click.FLOAT, default=10.0)
@click.option("--rec",
              type=click.Path(exists=True),
              help="PDB to use for calculating interface")
@click.option("-o", "--output",
              type=click.File(mode="w"),
              default=click.open_file('-', 'w'))
def pwrmsd(pdb_file, ftfile, rotprm, sort_ftresults, nftresults, only_ca,
           only_backbone, interface, interface_radius, rec, output):
    if interface and rec is None:
        click.echo("--interface requires --rec")
        sys.exit(1)

    lig = parsePDB(pdb_file)

    if sort_ftresults:
        ftresults = read_ftresults_stream(ftfile, limit=-1)
        ftresults.sort(order='E', kind='mergesort')
        if nftresults != -1:
            ftresults = ftresults[:nftresults]
    else:
        ftresults = read_ftresults_stream(ftfile, limit=nftresults)

    rotations = read_rotations(rotprm)

    center = np.mean(lig._getCoords(), axis=0)
    if only_ca:
        lig = lig.calpha
    elif only_backbone:
        lig = lig.backbone

    transformed = apply_ftresults_atom_group(lig, ftresults, rotations,
                                             center=center)

    if interface:
        rec = parsePDB(rec)

        pairwise_dists = interface_pwrmsd(rec, transformed,
                                          interface_d=interface_radius)
    else:
        pairwise_dists = pwrmsd_func(transformed)

    for rms in pairwise_dists.flat:
        output.write("{:.2f}\n".format(rms))
