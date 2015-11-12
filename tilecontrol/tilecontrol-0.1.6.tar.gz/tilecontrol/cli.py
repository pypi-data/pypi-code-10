import os

import click

from tilecontrol.scripts.checker import TileChecker
from tilecontrol.scripts.edgelist import EdgeFinder
from tilecontrol.scripts.parser import AwsLsParser
from tilecontrol.scripts.checker_parser import CheckerParser


@click.group()
def tlc():
    """
    Utilities for Satellite basemap quality control
    """
    pass


@tlc.command()
@click.argument('source_id')
@click.argument('layer_id')
@click.argument('cache', type=click.Path(exists=True))
@click.argument('destination', type=click.Path(exists=False))
@click.option('--zoom', default=13, help='Zoom level')
@click.option('--token', help='Mapbox Access Token')
def init(source_id, layer_id, cache, destination, zoom, token):
    """
    Bootstrap the QC process.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    initer = AwsLsParser(source_id, cache, zoom, destination, token, layer_id)
    initer.parsefile()
    initer.writeAllFiles()
    initer.findEdgeTiles()
    initer.writeOutputJson()


@tlc.command()
@click.argument('inzxy', type=click.Path(exists=True))
@click.argument('outzxy', type=click.Path(exists=False))
@click.option('--zoom', default=13, help='Zoom level')
def edges(inzxy, outzxy, zoom):
    """
    Finds the edges of a set of tiles.
    """
    edgeFinder = EdgeFinder(inzxy, outzxy, zoom)
    edgeFinder.findEdges()
    edgeFinder.writeFile()


@tlc.command()
@click.argument('layer_id')
@click.argument('inzxy', type=click.Path(exists=True))
@click.argument('edges')
@click.argument('geojsons')
@click.option('--token', default=None, help='Mapbox Access Token')
@click.option('--zoom', default=13, help='Zoom level')
def check(layer_id, inzxy, token, edges, geojsons, zoom):
    """
    Catch HTTP and Nodata errors.
    """
    output = inzxy + ".badTiles"

    tileChecker = TileChecker(layer_id, inzxy, outfile=output, mb_access_token=token, edgefile=edges, allscenegeojson_file=geojsons)
    tileChecker.findBadTiles()
    tileChecker.outputToFile()
    tileChecker.outputZXYtoFile()
    tileChecker.findSourceImages()
    tileChecker.outputGeojson()


@tlc.command()
@click.argument('source_id')
@click.argument('edges', type=click.Path(exists=True))
@click.argument('checker_output', type=click.Path(exists=False))
@click.argument('geojsons', type=click.Path(exists=True))
@click.argument('destination')
def parse_checker_results(source_id, edges, checker_output, geojsons, destination):
    """
    Legacy - Parse `checker` output.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    parser = CheckerParser(source_id, edges, checker_output, geojsons, destination)
