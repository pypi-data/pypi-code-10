#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Wed Oct  3 19:34:52 CEST 2012

''' This script separates the frames of REPLAY-ATTACK into folders and creates listfiles that need to be used as input into FaceRecLib'''

import numpy, random, os
import sys
import faceloc
import utils
from itertools import chain
import bob.io.base
import bob.ip.color
import bob.io.video


basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

INPUT_DIR = os.path.join(basedir, 'database')

def main():

  import argparse

  import bob.db.replay

  protocols = [k.name for k in bob.db.replay.Database().protocols()]

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  
  parser.add_argument('-d', '--frameoutputdir', metavar='DIR', type=str, default=OUTDIR, help='Directory where the extracted frames will be stored')

  parser.add_argument('-n', '--nthframe', metavar='NTHFRAME', type=int, default=10, dest='nthframe', help='All the frames with frame numbers divisible with this argument will be extracted')

  parser.add_argument('-p', '--protocol', metavar='PROTOCOL', type=str, dest="protocol", default='grandtest', help='The REPLAY-ATTACK protocol type may be specified instead of the id switch to subselect a smaller number of files to operate on', choices=protocols)
  
  parser.add_argument('-c', '--cls', metavar='CLASS', type=str, dest="cls", default=('real', 'attack', 'enroll'), help='The REPLAY-ATTACK classes may be specified instead of the id switch to subselect a smaller number of files to operate on', choices=['real', 'attack', 'enroll'], nargs='+')

  parser.add_argument('-g', '--groups', metavar='GROUPS', type=str, dest="groups", default=('train', 'devel', 'test'), help='The REPLAY-ATTACK groups may be specified instead of the id switch to subselect a smaller number of files to operate on', choices=['train', 'devel', 'test'], nargs='+')
  
  parser.add_argument('--sm', '--separate-modeling', dest='separate_modeling', action='store_true', default=False, help='Will create additional files (norm/train_world.lst) in separate directories for real and spoof data (needed for ISV modelling of subspace, for example)')

  parser.add_argument('--sf', '--save_frames', dest='save_frames', action='store_true', default=False, help='If True, will save the extracted frames, alongside with the generated listfiles.')
  
  parser.add_argument('-f', '--force', dest='force', action='store_true', default=False, help='Force to erase former data if already exists')

  args = parser.parse_args()

  db = bob.db.replay.Database()
  objects = db.objects(cls=args.cls, protocol=args.protocol, groups=args.groups)
  #objects = db.objects(cls=('real', 'attack', 'enroll'), protocol=args.protocol, group='train')
  
  # When evaluating a spoofing database, we need to separately do the scoring for the real accesses and for the attacks. Therefore, we need two folders: licit and spoof, in which we will keep the model and scoring files needed for the FaceRecLib. The model files are the same both for real accesses and attacks (i.e. the content of the files defined in list_files_formodels-real and list_files_formodels-attack is the same)
  list_files_formodels_real = {'world':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'norm', 'train_world.lst'), 'devel':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'dev', 'for_models.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'eval', 'for_models.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'train', 'for_models.lst')} 
  list_files_formodels_attack = {'world':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'norm', 'train_world.lst'), 'devel':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'dev', 'for_models.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'eval', 'for_models.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'train', 'for_models.lst')} 
  list_files_forseparatemodels = {'licit':os.path.join(args.frameoutputdir, 'listfiles', 'separate-models', 'licit', 'norm', 'train_world.lst'), 'spoof':os.path.join(args.frameoutputdir, 'listfiles', 'separate-models', 'spoof', 'norm', 'train_world.lst')}
  
  for key, fname in list_files_formodels_real.items():
    utils.ensure_dir(os.path.dirname(fname))
  for key, fname in list_files_formodels_attack.items():
    utils.ensure_dir(os.path.dirname(fname))
  if args.separate_modeling:  
    for key, fname in list_files_forseparatemodels.items():
      utils.ensure_dir(os.path.dirname(fname))

  list_files_forscores_real = {'devel':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'dev', 'for_scores.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'eval', 'for_scores.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'train', 'for_scores.lst')}
  list_files_forscores_attack = {'devel':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'dev', 'for_scores.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'eval', 'for_scores.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'train', 'for_scores.lst')}
  for key, fname in list_files_forscores_real.items():
    utils.ensure_dir(os.path.dirname(fname))
  for key, fname in list_files_forscores_attack.items():
    utils.ensure_dir(os.path.dirname(fname))

  # The content of the files defined in list_files_fortnorm-real and list_files_fortnorm-attack is the same
  list_files_fortnorm_real = {'devel':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'dev', 'for_tnorm.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'eval', 'for_tnorm.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'train', 'for_tnorm.lst')}
  list_files_fortnorm_attack = {'devel':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'dev', 'for_tnorm.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'eval', 'for_tnorm.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'train', 'for_tnorm.lst')}
  for key, fname in list_files_fortnorm_real.items():
    utils.ensure_dir(os.path.dirname(fname))
  for key, fname in list_files_fortnorm_attack.items():
    utils.ensure_dir(os.path.dirname(fname))
  # The content of the files defined in list_files_forznorm-real and list_files_forznorm-attack is the same
  list_files_forznorm_real = {'devel':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'dev', 'for_znorm.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'eval', 'for_znorm.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'licit', 'train', 'for_znorm.lst')}
  list_files_forznorm_attack = {'devel':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'dev', 'for_znorm.lst'), 'test':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'eval', 'for_znorm.lst'), 'train':os.path.join(args.frameoutputdir, 'listfiles', 'spoof', 'train', 'for_znorm.lst')}
  for key, fname in list_files_forznorm_real.items():
    utils.ensure_dir(os.path.dirname(fname))
  for key, fname in list_files_forznorm_attack.items():
    utils.ensure_dir(os.path.dirname(fname))


   
  # list of client id's 
  obj_devel = db.objects(cls='enroll', groups=('devel'), protocol=args.protocol)
  obj_eval = db.objects(cls='enroll', groups=('test'), protocol=args.protocol)
  obj_train = db.objects(cls='enroll', groups=('train'), protocol=args.protocol)
  client_ids_devel = []; client_ids_eval = []; client_ids_train = []
  for obj in obj_devel:  
    client_ids_devel.append(obj.client_id)
  for obj in obj_eval:  
    client_ids_eval.append(obj.client_id)
  for obj in obj_train:  
    client_ids_train.append(obj.client_id)
  client_ids = {'devel':set(client_ids_devel), 'test':set(client_ids_eval), 'train':set(client_ids_train)}

  counter = 0
  for obj in objects:
    counter +=1
    sys.stdout.write("Processing file '%s' (%d/%d)" % (obj.path, counter, len(objects)))
    sys.stdout.flush()
    
    # bootstraps video reader for client
    video = bob.io.video.reader(str(obj.videofile(directory=INDIR))) 

    # loads face locations - roll localization
    flocfile = obj.facefile(INDIR)
    locations = faceloc.read_face(str(flocfile))
    locations = faceloc.expand_detections(locations, video.number_of_frames) # at the end we have face bounding boxes

    for frame_index, frame in enumerate(video):

      if (frame_index+1) % args.nthframe: 
        sys.stdout.write('_')
        sys.stdout.flush()
        continue

      outputdir = os.path.join(args.frameoutputdir, '%03d' % (frame_index+1))
      eye_outputdir = os.path.join(args.frameoutputdir, 'eyecenters', '%03d' % (frame_index+1))
      output_filename = obj.make_path(outputdir, '.png') # .jpg, .hdf5
      eyecenters_filename = obj.make_path(eye_outputdir, '.pos')

      if frame_index >= len(locations) or not locations[frame_index] or \
          not locations[frame_index].is_valid():
        sys.stdout.write('x')
        sys.stdout.flush()
        continue

      # if we continue, there was a detected face for the present frame.

      # create the output folders if they do not exist
      utils.ensure_dir(os.path.dirname(output_filename))
      utils.ensure_dir(os.path.dirname(os.path.join(eyecenters_filename)))

      # some house-keeping commands
      if os.path.exists(output_filename) and not args.force:
        raise RuntimeError, "Output file path %s already exists and you did not --force" % output_filename

      # save the frame
      if args.save_frames:
        obj.save(frame, outputdir, '.png') # could be .jpg, .hdf5 

        # save the eye locations
        anthropo = faceloc.Anthropometry19x19(locations[frame_index])
        eyecenters = anthropo.eye_centers()
        f = open(eyecenters_filename, 'w')
        f.write(str(int(eyecenters[0][0])) + ' ' + str(int(eyecenters[0][1])) + ' ' + str(int(eyecenters[1][0])) + ' ' + str(int(eyecenters[1][1])))
        f.close()

      # write the filename and client id into the corresponding list file
      if obj.is_real():
        if obj.get_realaccess().purpose == 'enroll': enroll = True
        else: 
          enroll = False
      #cls = str(obj.path.split('/')[0])
      
      
      # if it is enroll file, put it into train_world.lst subset, or for_models.lst, depending on the group it belongs to
      if enroll: # write into the model files, the same data into the model files for real accesses and attacks
        f = open(list_files_formodels_real[str(obj.client.set)], 'a')
        f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
        f.close()
        f = open(list_files_formodels_attack[str(obj.client.set)], 'a')
        f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
        f.close()
        
        if str(obj.client.set) == 'train': # the training enrollment files should go into the world set + they can be used for zt normalization both for devel and eval sets
          f = open(list_files_formodels_real['world'], 'a')
          f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
          f.close()
          f = open(list_files_formodels_attack['world'], 'a')
          f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
          f.close()

          if not args.separate_modeling: #z-norm and t-norm are populated with enrollment samples
            for key, fname in list_files_fortnorm_real.items():
              f = open(fname, 'a')
              f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id + client id
              f.close()
            for key, fname in list_files_fortnorm_attack.items():
              f = open(fname, 'a')
              f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id + client id
              f.close()
            for key, fname in list_files_forznorm_real.items():
              f = open(fname, 'a')
              f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
              f.close()
            for key, fname in list_files_forznorm_attack.items():
              f = open(fname, 'a')
              f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
              f.close()

      else: # NOT enrollment data
        if args.separate_modeling: # write separate 
          if str(obj.client.set) == 'train':
            if obj.is_real():
              f = open(list_files_forseparatemodels['licit'], 'a')
            else:  
              f = open(list_files_forseparatemodels['spoof'], 'a')
            f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
            f.close()

            # the following needs a rearrangement  
            if obj.is_real() or not obj.is_real():
              for key, fname in list_files_forznorm_real.items():
                f = open(fname, 'a')
                f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
                f.close()
              for key, fname in list_files_fortnorm_real.items():
                f = open(fname, 'a')
                f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id + client id
                f.close() 
            #else:
              for key, fname in list_files_forznorm_attack.items():
                f = open(fname, 'a')
                f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id
                f.close() 
              for key, fname in list_files_fortnorm_attack.items():
                f = open(fname, 'a')
                f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + '\n') # write the file path + the client id + client id
                f.close()  
        
        if obj.is_real(): # write into the score files for licit and spoof protocol
          f = open(list_files_forscores_real[str(obj.client.set)], 'a')
          for ids in client_ids[str(obj.client.set)]:
            f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(ids) + ' ' + str(ids) + ' ' + str(obj.client_id) + '\n') #file_path model_id claimed_id real_id 
          f.close()
          f = open(list_files_forscores_attack[str(obj.client.set)], 'a')
          f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + '\n')
          f.close()
        else: # write into the score files for attacks
          f = open(list_files_forscores_attack[str(obj.client.set)], 'a')
          f.write(os.path.join('%03d' % (frame_index+1), str(obj.path)) + ' ' + str(obj.client_id) + ' ' + str(obj.client_id) + ' attack\n') #file_path model_id claimed_id attack 
          f.close()

      sys.stdout.write('.')
      sys.stdout.flush()

    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == '__main__':
  main()


