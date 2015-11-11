# Deploys a directory for lambda.
import subprocess
import os
import zipfile

class LambdaDeploy(object):
    """
    Deploys a zip to S3 that is ready for use with lambda.
    """
    def __init__(self, directory, bucket, name):
        """
        Creates a new deploy object for deploying to S3.

        Params:
        -------
        directory : str
            Location of the lambda function to zip. This should include pip files.
        bucket : str
            The S3 bucket to send the file to.
        name : str
            The name of the zipped file. Defaults to my_lambda_function
        """
        self.directory = directory
        self.bucket = bucket
        self.name = name

        self.__initialize()

    def __initialize(self):
        """
        Initializes the object and ensures data integrity.
        """
        if self.directory is None or type(self.directory) is not str or self.directory == "":
            raise ValueError("Please provide a valid directory string.")
        if self.bucket is None or type(self.bucket) is not str or self.bucket == "":
            raise ValueError("Please provide a valid S3 bucket location string.")
        if self.name is not None and (type(self.name) is not str or self.name == ""):
            raise ValueError("Please provide a valid name for the zip file.")


        # Check for valid paths for the directory and S3
        if not os.path.isdir(self.directory):
            raise IOError(self.directory + " is not a valid directory!")

        self.directory = os.path.abspath(self.directory)

        if self.bucket.find("s3://") == -1:
            raise ValueError("Invalid S3 bucket location! Should start with 's3://'")

        if self.name is None:
            self.name = "my_lambda_function"

    def deploy(self):
        """
        Deploys to AWS based on the internal state of the object.
        """
        args = ["which", "zip"]
        p = subprocess.Popen(args)
        result = p.wait()
        if result != 0:
            raise Exception("'zip' is not installed on the system!")

        args = ["which", "aws"]
        p = subprocess.Popen(args)
        result = p.wait()
        if result != 0:
            raise Exception("'aws' cli is not installed on the system!")

        self.check_pip_packages()

        # Zip the file
        args = ["zip", "-r", "/tmp/" + self.name + ".zip", ".", "-i", "*"]
        p = subprocess.Popen(args)
        result = p.wait()
        if result != 0:
            print p.stderr
            raise Exception("Unable to zip the current directory! " + self.directory)

        # Send to aws aws s3 cp ./" + info.name + ".zip " + s3
        args = ["aws", "s3", "cp", "/tmp/" + self.name + ".zip", self.bucket]
        p = subprocess.Popen(args)
        result = p.wait()
        if result != 0:
            raise Exception("Unable to upload to S3!")

    def check_pip_packages(self):
        """
        Checks if the directory uses pip packages. If so, downloads to correct folder within directory.
        """
        if not os.path.isfile(self.directory + "/requirements.txt"):
            print "WARNING: No 'requirements.txt' was found within the directory. Skipping automatic pip packaging."
        else:
            args = ["which", "pip"]
            p = subprocess.Popen(args)
            result = p.wait()
            if result != 0:
                raise Exception("'pip' is not installed on the system!")

            args = ["pip", "install", "-r", self.directory + "/requirements.txt", "-t", self.directory]
            p = subprocess.Popen(args)
            result = p.wait()
            if result != 0:
                raise Exception("Unable to pip install packages from requirements.txt!")
