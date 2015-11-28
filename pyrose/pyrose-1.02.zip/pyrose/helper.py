import os

def create_dir(dir_path):

	if not os.path.exists(dir_path):
		try:
			os.makedirs(dir_path)
		except:
			sys.exit( "Output directory (%s) could not be created." % dir_path )
 
    
