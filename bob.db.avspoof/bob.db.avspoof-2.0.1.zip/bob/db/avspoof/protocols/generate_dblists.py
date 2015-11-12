#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Mon  18 Aug 23:12:22 CEST 2015
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the ipyplotied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
#import numpy
import math
import argparse


def listFiles(rootdir="."):
    objs = []
    for root, dirs, files in os.walk(rootdir):
        _, path = root.split(rootdir)
        path = path.split(os.path.sep)
        gender = "male"  # female also ends with "male", so we cover both
        if gender in root:
            for file in files:
                    file, ext = os.path.splitext(file)
                    if ext == ".wav":
                        subpath = path[1:]
                        subpath.append(file)
                        start_id_indx = root.index(gender)+len(gender)+1
                        id = root[start_id_indx:start_id_indx+4]
                        objs.append((os.path.join(*subpath), id))
    return objs


def getIds(rootdir=".", gender="male", filter="genuine"):
    ids = []
    for root, dirs, files in os.walk(rootdir):
        curdir = os.path.basename(root)
        if curdir == gender and filter in root:
            ids = dirs
            break
    return ids


def getSubIds(ids, set="train"):
    subids = []

    if not ids:
        return subids

#  indices=numpy.arange(len(ids))

    sublen = int(math.floor(len(ids)/3))

    if set == "train":
        subids = ids[0:sublen]
    elif set == "devel":
        subids = ids[sublen:2*sublen]
    elif set == "test":
        subids = ids[2*sublen:]

    return subids

#  numpy.choice(ids)


def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--database-directory', required=False,
                        help="The root directory of database data.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def main(command_line_parameters=None):
    """Reads score files, computes error measures and plots curves."""

    args = command_line_arguments(command_line_parameters)

    rootdir = os.path.curdir
    if args.database_directory:
        rootdir = args.database_directory

    filters = ["genuine", "attack"]
    sets = ["train", "devel", "test"]
    prefix = "-grandtest-allsupports"
#    prefix = "-smalltest-allsupports"

    # fix ids split for the whole thing, so we are consistent accross diff filters
    male_ids = getIds(rootdir, "male", filters[0])
    female_ids = getIds(rootdir, "female", filters[0])

    # traverse database and constract the whole list of files
    list = listFiles(rootdir)

    fid = open("clients%s.txt" % (prefix), "w")
    for set in sets:
        #   if not os.path.exists(set):
        #     os.makedirs(set)
        set_ids = getSubIds(male_ids[0:3], set)
        set_ids.extend(getSubIds(female_ids[0:3], set))
        print "set %s, set_ids: %s " % (set, " ".join(id for id in set_ids))
        fid.write('\n'.join("%s %s" % (id, set) for id in set_ids))
        fid.write('\n')
        for filter in filters:
            # get ids for the specific set
            # set_ids = getSubIds(male_ids, set)
            # set_ids.extend(getSubIds(female_ids, set))
            # print "set %s, set_ids: %s " %(set, " ".join(id for id in set_ids))
            # get only sublist for this set and this filter/type
            list4set = []
#            counter=1
            for item in list:
                if item[1] in set_ids and filter in item[0]:
                    list4set.append(item[0])
#                    counter+=1
#                    if counter == 5:
#                        break
#            print list4set
            if filter == "genuine":
                filename = "real%s-%s.txt" % (prefix, set)
            if filter == "attack":
                filename = "attack%s-%s.txt" % (prefix, set)

            with open(filename, "w") as f:
                    f.write('\n'.join(stem for stem in list4set))
                    f.close()


#      else:
#        if filter == "attack":
#          filename=os.path.join(set, "for_scores.lst")
#          with open(filename, "w") as f:
#            for stem, id in list4set:
#              stemsplit = stem.split(os.path.sep)
#              f.write('%s %s %s %s\n' % (stem, id, id, stemsplit[1]) )
#            f.close()
#        if filter == "genuine":
#          filename=os.path.join(set, "for_models.lst")
#          with open(filename, "w") as f:
#            f.write('\n'.join("%s %s %s" %(stem, id, id) for stem,id in list4set))
#            f.close()
#
    fid.close()
if __name__ == '__main__':
    main()
