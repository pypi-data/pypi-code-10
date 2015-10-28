import os
import json
import click

# import scripts.checker_parser as Checker_parser
import scripts.edgelist as Edgelist
import scripts.parser as Parser
import scripts.checker as Checker


@click.group()
def cli():
    """
    Utilities for Satellite basemap quality control
    """
    pass


@cli.command()
@click.argument('sourceid')
@click.argument('layerid')
@click.argument('cachefile', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=False))
@click.option('--zoom', default=13, help='Zoom level')
@click.option('--token', help='Mapbox Access Token')
def parse(sourceid, layerid, cachefile, output_dir, zoom, token):
    """
    For a sourceid, generates a list of ZXY tiles that need to be QC'd
    """
    # Ensure output dir exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    parser = Parser.AwsLsParser(sourceid, cachefile, zoom, output_dir, token, layerid)
    parser.parsefile()
    parser.writeAllFiles()
    parser.findEdgeTiles()
    # parser.runChecker()
    parser.writeOutputJson()


@cli.command()
@click.argument('inzxy', type=click.Path(exists=True))
@click.argument('outzxy', type=click.Path(exists=False))
@click.option('--zoom', default=13, help='Zoom level')
def edges(inzxy, outzxy, zoom):
    """
    Finds the edge tiles of a file containing a list of ZXY tiles.
    Outputs are written to a user-specified file.
    """
    edgeFinder = Edgelist.EdgeFinder(inzxy, outzxy, zoom)
    edgeFinder.findEdges()
    edgeFinder.writeFile()


@cli.command()
@click.argument('layerid')
@click.argument('inzxy', type=click.Path(exists=True))
@click.argument('edgelist')
@click.argument('geojsonfileslist')
@click.option('--token', default=None, help='Mapbox Access Token')
@click.option('--zoom', default=13, help='Zoom level')
def checker(layerid, inzxy, token, edgelist, geojsonfileslist, zoom):
    """
    Finds the edge tiles of a file containing a list of ZXY tiles.
    Outputs are written to a user-specified file.
    """
    output = inzxy + ".badTiles"
    tileChecker = Checker.TileChecker(layerid, inzxy, outfile=output,
        mb_access_token=token, edgefile=edgelist, allscenegeojson_file=geojsonfileslist)

    tileChecker.findBadTiles()
    tileChecker.outputToFile()
    geojson_path = tileChecker.outputGeojson()

    # Write list of zxy files selecting out the edges
    tileChecker.outputZXYtoFile()
    tileChecker.findSourceImages()


# @cli.command()
# @click.option('--s3parsejson', default="0", help='json file with necessary specs for this mosaic')
# @click.option('--checkeroutput', default="0", help='checker outputs collected into a text file of json entries')
# def checkparse(s3parsejson, checkeroutput):
#     """
#     Parses the checker output into a zxy lists
#     The raw watchbot checker output from s3 looks like this:
#     Cross reference against edge tiles list
#     This script reads a whole directory of them and outputs them into two files,
#         - one of missing zxy
#         - one of nodata zxy
#     """
#     with open(s3parsejson, 'r') as s3outputsfile:
#         s3outputs = json.loads(s3outputsfile.read())

#     edge_zxy_file = s3outputs['zxy_edge_list']
#     sourceid = s3outputs['sourceid']
#     output_dir = s3outputs['output_dir']
#     allscenegeojson_file = s3outputs['all_tile_geojsons']

#     checker = Checker_parser.CheckerParser()
#     checker(sourceid, edge_zxy_file, checkeroutput, allscenegeojson_file,  output_dir)
