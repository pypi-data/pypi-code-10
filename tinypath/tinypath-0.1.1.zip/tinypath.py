"""
# tinypath

Tinypath is a tiny file path module that provides only the most crucial and
commonly needed functionality, including turning files and folders into classes.
Designed as a companion module for projects that require handling arbitrary paths
from users without breaking, and easy navigation of local file systems. 

By staying tiny in both size and functionality, the API is easy to learn so
you can start using it right away. Essentially, it provides object-oriented access
to files and folders with several convenient attributes such as checking file or
folder size, handling a lot of the intricacies of os.path behind
the scene so you do not have to. 


## Platforms

Tested on Python version 2.x. 


## Dependencies

Pure Python, no dependencies. 


## Installing it

Tinypath is installed with pip from the commandline:

    pip install tinypath


## More Information:

- [Home Page](http://github.com/karimbahgat/tinypath)
- [API Documentation](http://pythonhosted.org/tinypath)


## License:

This code is free to share, use, reuse,
and modify according to the MIT license, see license.txt


## Credits:

Karim Bahgat (2015)

"""

__version__ = "0.1.1"


# Imports
import sys,os,time


# Classes

class Size:
    """
    The file size object, as returned by File.size.

    Attributes:

    - **bytes**: The actual size in bytes, to be used for calculations.
    - **string**: The size as a more sensible human-readable string depending on size. 
    """
    def __init__(self, bytes):
        self.bytes = bytes
        # parse
        size = bytes
        kb,mb,gb = 1000, 1000*1000, 1000*1000*1000
        if size < mb:
            size = size/float(kb)
            sizeunit = "kb"
        elif size < gb:
            size = size/float(mb)
            sizeunit = "mb"
        else:
            size = size/float(gb)
            sizeunit = "gb"
        self.string = "%.3f %s" %(size, sizeunit)

    def __str__(self):
        return "Size: %s" %self.string







class Folder:
    """
    A class that holds info about a folder, which can be accessed via attributes

    Attributes:

    - **path**: Full proper path of the folder.
    - **name**: Just the name of the folder. 
    - **exists**: True or False if exists.
    - **read_ok**: Read permission or not.
    - **write_ok**: Write permission or not. 
    - **location**: The parent folder where the folder is located.
    - **content**: A list of all child files and folders.
    - **files**: A list of all child files.
    - **folders**: A list of all child folders.
    - **size**: A Size instance of the total size of the entire folder.
        This is done by looping and sizign all nested child files, so can take a while
        for a high level folder. The size is cached after the first time to ease
        repeat calling.
    - **total_files**: Total number of files within the entire folder.
    
    """
    def __init__(self, *folderpath, **kwargs):
        """
        Arguments:
        
        - **folderpath**: can be a relative path, a full path incl drive letter and filetype extension, or a list of path name elements to be joined together
        """
        #concatenate path elements if multiple given
        folderpath = os.path.join(*folderpath)
        #full normalized path (make into absolute path if relative)
        folderpath = os.path.abspath(folderpath)
        folderpath = os.path.normpath(folderpath)
        self.path = folderpath
        #access
        self.exists = os.access(self.path, os.F_OK)
        self.read_ok = os.access(self.path, os.R_OK)
        self.write_ok = os.access(self.path, os.W_OK)
        #split entire path into components
        pathsplit = []
        head,tail = os.path.split(self.path)
        while head != "":
            pathsplit.insert(0,tail)
            if os.path.ismount(head):
                drive = head
                break
            head,tail = os.path.split(head)
        #parent folder path
        if len(pathsplit) > 1:
            oneup = os.path.join(*pathsplit[:-1])
        else:
            oneup = ""
        if drive:
            self._oneup = drive+oneup
        else:
            self._oneup = oneup
        self.name = pathsplit[-1]

    def __str__(self):
        string = "Folder:\n"
        for each in (self.location.name,self.name,self.size,self.total_files):
            string += "\t%s\n" % each
        return string

    def __repr__(self):
        return "Folder( %s )" % self.path

    # Properties

    @property
    def location(self):
        return Folder(self._oneup)
    
    @property
    def content(self):
        content = []
        content.extend(self.files)
        content.extend(self.folders)
        return content

    @property
    def files(self):
        if not hasattr(self, "_files"):
            self._files = []
            try:
                children = os.listdir(self.path)
                for child in children:
                    childpath = os.path.join(self.path, child)
                    if os.path.isfile(childpath) or os.path.islink(childpath):
                        self._files.append( File(childpath) )
            
            except OSError:
                pass

        return self._files

    @property
    def folders(self):
        if not hasattr(self, "_folders"):
            self._folders = []
            try:
                children = os.listdir(self.path)
                for child in children:
                    childpath = os.path.join(self.path, child)
                    if os.path.isdir(childpath):
                        self._folders.append( Folder(childpath) )
            
            except OSError:
                pass
            
        return self._folders

    @property
    def size(self):
        # collect
        if not hasattr(self, "_size"):
            foldersize = 0
            for file in self.loop():
                if file.read_ok:
                    foldersize += file.size.bytes
            self._size = Size(foldersize)
            
        return self._size

    @property
    def total_files(self):
        # collect
        if not hasattr(self, "_filecount"):
            self._filecount = 0
            for file in self.loop():
                self._filecount += 1
                
        return self._filecount

    # Methods
    
    def up(self):
        """Changes this object's path up one level"""
        newpath = self._oneup
        self.__init__(newpath)
        
    def down(self, foldername):
        """Changes this object's path down into the given subfolder name"""
        for folder in self.folders:
            if foldername == folder.name:
                newpath = folder.path
                self.__init__(newpath)
                break
        else: raise Exception("No such folder found")
        
    def loop(self, filetypes=[], maxdepth=None):
        """
        Loops files only

        Arguments:

        - **filetypes** (optional): If filetype is a sequence then grabs all filetypes listed within it, otherwise grabs everything.
            Each file type is specified as the file extension including the dot, eg ".py".
        - **maxdepth** (optional): Max depth to look before continuing. 
        """
        return loop_folder(self, filetypes, maxdepth)
    
    def overview(self, filetypes=[], maxdepth=None):
        """
        Return a string representation of the folder structure and file members, as a snapshot of the folder's content.

        Arguments:

        - **filetypes** (optional): If filetypes is a sequence then grabs all filetypes listed within it, otherwise grabs everything.
            Each file type is specified as the file extension including the dot, eg ".py".
        - **maxdepth** (optional): Max depth to look before continuing. 
        """

        if not filetypes: filetypes = []
        if not isinstance(filetypes, (list,tuple)): filetypes = [filetypes]
        
        # setup
        topfolder = self
        depth = 0
        spaces = "  "
        structstring = self.path+"\n"
        def recurloop(parentfolder, structstring, depth, spaces):
            depth += 1
            if not maxdepth or depth <= maxdepth:
                if not filetypes:
                    for file in parentfolder.files:
                        structstring += spaces*depth + file.name + file.type + "\n"
                else:
                    for file in parentfolder.files:
                        if file.type in filetypes:
                            structstring += spaces*depth + file.name + file.type + "\n"
                for folder in parentfolder.folders:
                    structstring += spaces*depth + folder.name + "\n"
                    folder, structstring, depth, spaces = recurloop(folder, structstring, depth, spaces)
            depth -= 1
            return parentfolder, structstring, depth, spaces
        # begin
        finalfolder, structstring, depth, spaces = recurloop(topfolder, structstring, depth, spaces)
        return structstring

    def overview_table(self, filetypes=[], maxdepth=None):
        """
        Return a tab-delimited table string of the folder structure and file members, as a snapshot of the folder's content.

        Arguments:

        - **filetypes** (optional): If filetypes is a sequence then grabs all filetypes listed within it, otherwise grabs everything.
            Each file type is specified as the file extension including the dot, eg ".py".
        - **maxdepth** (optional): Max depth to look before continuing. 

        Warning: Not fully tested...
        """
        # setup
        topfolder = self
        depth = 0
        delimit = "\t"
        structstring = delimit.join(["path","name","type","depth","size"])+"\n"
        structstring += delimit.join([self.path,self.name,"",str(depth),str(self.size.bytes)])+"\n"
        def recurloop(parentfolder, structstring, depth):
            depth += 1
            if not maxdepth or depth <= maxdepth:
                if not filetypes:
                    for file in parentfolder.files:
                        structstring += delimit.join([file.path,file.name,file.type,str(depth),str(file.size.bytes)])+"\n"
                else:
                    for file in parentfolder.files:
                        if file.type in filetypes:
                            structstring += delimit.join([file.path,file.name,file.type,str(depth),str(file.size.bytes)])+"\n"
                for folder in parentfolder.folders:
                    structstring += delimit.join([folder.path,folder.name,"",str(depth),str(folder.size.bytes)])+"\n"
                    folder, structstring, depth = recurloop(folder, structstring, depth)
            depth -= 1
            return parentfolder, structstring, depth
        # begin
        finalfolder, structstring, depth = recurloop(topfolder, structstring, depth)
        return structstring







class File:
    """
    A class that holds info about a file, which can be accessed via attributes.

    Attributes:

    - **path**: Full proper path of the folder.
    - **name**: Just the name of the folder.
    - **type**: Type extension of the file.
    - **filename**: Name with type extension. 
    - **exists**: True or False if exists.
    - **read_ok**: Read permission or not.
    - **write_ok**: Write permission or not.
    - **size**: Size instance of the size of the file.
    - **lastchanged**: The last time the file was modified as a timestamp object. 
    """
    def __init__(self, *filepath, **kwargs):
        """
        Arguments:
        
        - **filepath**: can be a relative path, a full path incl drive letter and filetype extension, or a list of path name elements to be joined together
        """
        #concatenate path elements if multiple given
        filepath = os.path.join(*filepath)
        #full normalized path (make into absolute path if relative)
        filepath = os.path.abspath(filepath)
        filepath = os.path.normpath(filepath)
        self.path = filepath
        #access
        self.exists = os.access(self.path, os.F_OK)
        self.read_ok = os.access(self.path, os.R_OK)
        self.write_ok = os.access(self.path, os.W_OK)
        #split entire path into components
        pathsplit = []
        head,tail = os.path.split(filepath)
        while head != "":
            pathsplit.insert(0,tail)
            if os.path.ismount(head):
                drive = head
                break
            head,tail = os.path.split(head)
        #folder path
        if len(pathsplit) > 1:
            oneup = os.path.join(*pathsplit[:-1])
        else:
            oneup = ""
        if drive:
            self.folder = Folder(drive+oneup)
        else:
            self.folder = Folder(oneup)
        #filename and type
        fullfilename = pathsplit[-1]
        filename,filetype = os.path.splitext(fullfilename)
        self.name = filename #".".join(fullfilename.split(".")[:-1])
        self.type = filetype #"." + fullfilename.split(".")[-1]
        self.filename = filename + filetype

    def __str__(self):
        string = "File:\n"
        for each in (self.folder.name,self.name,self.type):
            string += "\t%s\n" % each
        if self.read_ok:
            string += "\t%s\n" % self.size
            string += "\t%s\n" % self.lastchanged
        return string

    def __repr__(self):
        return "File( %s )" % self.path

    @property
    def size(self):
        #filesize
        if not hasattr(self, "_size"):
            self._size = Size( os.path.getsize(self.path) )
        return self._size

    @property
    def lastchanged(self):
        #last changed
        if not hasattr(self, "_lastchanged"):
            self._lastchanged = time.ctime(os.path.getmtime(self.path))
        return self._lastchanged







# User Functions

def current_script():
    """
    Returns the file object of the currently running script
    """
    return File(__file__)

def current_folder():
    """
    Returns the folder object of the currently running script
    """
    curfile = current_script()
    return curfile.folder

def path2obj(path):
    """
    Returns a File or Folder object from the given path.
    """
    if os.path.isfile(path) or os.path.islink(path):
        return File(path)
    elif os.path.isdir(path):
        return Folder(path)

def loop_folder(folder, filetypes=[], maxdepth=None):
    """
    A generator that iterates through all files in a folder tree, either in a for loop or by using next() on it.

    Arguments:

    - **folder**: The folder path to loop. Can be a folder instance, or any string path accepted by Folder. 
    - **filetypes** (optional): If filetypes is a sequence then grabs all filetypes listed within it, otherwise grabs everything.
        Each file type is specified as the file extension including the dot, eg ".py".
    - **maxdepth** (optional): Max depth to look before continuing. 
    """
    if not filetypes: filetypes = []
    if not isinstance(filetypes, (list,tuple)): filetypes = [filetypes]
    
    # setup
    if not isinstance(folder, Folder): 
        topfolder = Folder(folder)
    else:
        topfolder = folder
    depth = 0
    def recurloop(parentfolder, depth):           
        depth += 1
        if not maxdepth or depth <= maxdepth:
            if not filetypes:
                for file in parentfolder.files:
                    yield file
            else:
                for file in parentfolder.files:
                    if file.type in filetypes:
                        yield file
            for folder in parentfolder.folders:
                for file in recurloop(folder, depth):
                    yield file
    # begin
    return recurloop(topfolder, depth)





    
