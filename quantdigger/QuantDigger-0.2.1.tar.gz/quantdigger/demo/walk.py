import os
for path, dirs, files in os.walk(os.getcwd()):
    print dirs
    for file in files:
        #print os.path.join(path, file)
        filepath = path + os.sep + file
        print path, os.sep, file
        if filepath.endswith(".asm"):
            print (filepath)
