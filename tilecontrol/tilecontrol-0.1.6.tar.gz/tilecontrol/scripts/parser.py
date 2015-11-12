import click
import json
import os
import time

from . import checker
from . import edgelist
from . import pxmfile


class AwsLsParser(object):
    def __init__(self, sourceid, awslsfile=None, refzoom=13, output_dir=None,
                 mapbox_access_token=None, layerid=None):
        self.sourceid = sourceid
        self.awslsfile = awslsfile
        self.output_dir = output_dir
        self.refzoom = refzoom
        self.mapbox_access_token = mapbox_access_token
        self.layerid = layerid

        # If true, output a file of the list of unique source image names
        # seen in the aws_ls snapshot for the given sourceid
        self.get_unique_sourceimgae = True

        # If true, output a file of the list of zxy tiles seen for the sourceid
        self.get_zxy_coverage = True

        # If true, output a file of the list of zxy tiles seen for the sourceid
        self.get_geojson_list = True

        self.source_image_list = []
        self.unique_source_image_geojson = []
        self.geojson_list = []
        self.zxy_list = []

        # four output files
        self.count = 0

        # store all the output files from AwsLsParser
        self.outputfiles_dict = {}

    def parsefile(self):
        """
        Read's a file and extract's scene metadata per sourceid. Slow.
        """
        with open(self.awslsfile, 'r') as aws_lscache:
            for file in aws_lscache:
                if self.sourceid in file and file.rstrip().split('.').pop() == 'geojson':
                    geojson_file = file.lstrip().rstrip().split().pop()
                    self._readGeoJsonFile(geojson_file)
                    self.count += 1

    def _readGeoJsonFile(self, geojson_filename):
        """
        For each geojson filename identified:
            1. Store it's zxy
            2. keep track of the source image name
        """
        pxmf = pxmfile.PxmFile.getfile(geojson_filename)
        self.zxy_list.append(pxmf.getZXY())
        self.geojson_list.append(geojson_filename)

        if pxmf.getSourceImg() not in self.source_image_list:
            self.source_image_list.append(pxmf.getSourceImg())
            self.unique_source_image_geojson.append(geojson_filename)

    def writefile(self, descrip, data):
        """
        writes out a list line by line into the filename
            [self.sourcied]_[descrip]_[date]
        """
        day = time.strftime("%Y_%m_%d")
        output_filename = "%s_%s_%s" % (self.sourceid, descrip, day)
        output_path = os.path.join(self.output_dir, output_filename)

        data = getattr(self, data)
        with open(output_path, 'w') as outfile:
            for val in data:
                outfile.write(val + "\n")

        return output_path

    def findEdgeTiles(self):
        edge_infile = self.outputfiles_dict['zxy_list']
        edge_outfile = "%s_%s_%s" % (self.sourceid, "edges", time.strftime("%Y_%m_%d"))
        edge_outfile_fullpath = os.path.join(self.output_dir, edge_outfile)

        edgeFinder = edgelist.EdgeFinder(edge_infile, edge_outfile_fullpath, self.refzoom)

        edgeFinder.findEdges()
        edgeFinder.writeFile()

        self.outputfiles_dict['zxy_edge_list'] = edge_outfile_fullpath
        click.echo("output edge files:" + edge_outfile_fullpath)

    def runChecker(self):
        checker_output = self.outputfiles_dict['zxy_list'] + ".NodataMissing"
        click.echo("looking for bad tiles in:" + self.outputfiles_dict['zxy_list'])

        tileChecker = checker.TileChecker(self.layerid, self.outputfiles_dict['zxy_list'], outfile=checker_output, mb_access_token=self.mapbox_access_token)
        tileChecker.findBadTiles()
        tileChecker.outputToFile()
        geojson_path = tileChecker.outputGeojson()

        self.outputfiles_dict['checker_output'] = checker_output
        self.outputfiles_dict['missingNodata_geojson'] = geojson_path
        click.echo("missing/nodata tiles:" + checker_output)
        click.echo("missing/nodata geoJson:" + geojson_path)

    def writeAllFiles(self):
        outfile_path = self.writefile('sourceimgnames', 'source_image_list')
        self.outputfiles_dict['source_images'] = outfile_path

        outfile_path = self.writefile('sourceimgGeojsons',
                                      'unique_source_image_geojson')
        self.outputfiles_dict['source_footprints'] = outfile_path

        outfile_path = self.writefile('zxy', 'zxy_list')
        self.outputfiles_dict['zxy_list'] = outfile_path

        outfile_path = self.writefile('geojsons', 'geojson_list')
        self.outputfiles_dict['all_tile_geojsons'] = outfile_path

        self.outputfiles_dict['sourceid'] = self.sourceid
        self.outputfiles_dict['output_dir'] = self.output_dir

    def writeOutputJson(self):
        # Log the json outputs so that the following steps know where to look
        resultjson = "%s_awsparse_outputs.json" % self.sourceid
        resultjson_path = os.path.join(self.output_dir, resultjson)
        with open(resultjson_path, 'w') as fp:
            json.dump(self.outputfiles_dict, fp)
