import key
import conf
from stupeflix import *
import time
import traceback

class StupeflixTest:
    def __init__(self):
        # Create the client to access the API
        # You can safely assume that key.stupeflixHost is None
        self.client = StupeflixClient(key.stupeflixAccessKey, key.stupeflixSecretKey, host = key.stupeflixHost)
        
        # Set the name for the resource to be created
        # These names are alphanumerical, and can be set to whatever you want
        self.user = "test"
        self.resource = "resource" + conf.dateString
        # Configuration for s3 retries
        self.s3Retries = 5
        self.s3Wait = 1
        # Set this to true if you want to see the status of videos being generated
        self.debug = True

    def uploadsCreate(self, profileName):
        """Create several upload targets. Choose the ones you want by setting the corresponding variables in conf.py, or modify directly the code."""
        user = self.user
        resource = self.resource
        
        # Array of uploads to be filled in
        uploads = []

        # Default upload creation : will store to the stupeflix s3 bucket
        # This is not mandatory, just a easy way to store temporarily the result of the video generation.
        uploads += [StupeflixDefaultUpload()]

         # YouTube upload creation, if correct information was entered in conf.py
        if conf.youtubeLogin != None:
            # Create sample youtube information
            tags = ",".join(["these","are","my","tags"])
            youtubeInfo = {"title" : "Upload test "  + conf.dateString,
                           "description": "Upload test description" + conf.dateString,
                           "tags":tags,
                           "channels":"Tech",
                           "acl":"public",
                           "location":"49,-3"}

            youtubeMeta = StupeflixMeta(youtubeInfo)
            # There is no currently notification 
            youtubeNotify = None
            uploads += [StupeflixYoutubeUpload(conf.youtubeLogin, conf.youtubePassword, meta = youtubeMeta, notify = youtubeNotify)]

        # YouTube upload creation, if correct information was entered in conf.py
        if conf.youtubeAuthSubToken != None:
            # Create sample youtube information
            tags = ",".join(["these","are","my","tags"])
            youtubeInfo = {"title" : "Upload test "  + conf.dateString,
                           "description": "Upload test description" + conf.dateString,
                           "tags":tags,
                           "channels":"Tech",
                           "acl":"public",
                           "location":"49,-3"}

            youtubeMeta = StupeflixMeta(youtubeInfo)
            # There is no currently notification 
            youtubeNotify = None
            uploads += [StupeflixYoutubeTokenUpload(conf.youtubeDeveloperKey, conf.youtubeAuthSubToken, meta = youtubeMeta, notify = youtubeNotify)]

        # Dailymotion upload creation, if correct information was entered in conf.py
        if conf.dailymotionLogin != None:
            # Create sample dailymotion information
            tags = ",".join(["these","are","my","tags"])
            dailymotionInfo = {"title" : "Upload test "  + conf.dateString,
                               "description": "Upload test description" + conf.dateString,
                               "tags":tags,
                               "channels":"Tech",
                               "acl":"public",
                               "location":"49,-3"}

            dailymotionMeta = StupeflixMeta(dailymotionInfo)
            # There is no currently notification 
            dailymotionNotify = None
            uploads += [StupeflixDailymotionUpload(conf.dailymotionLogin, conf.dailymotionPassword, meta = dailymotionMeta, notify = dailymotionNotify)]

        # Dailymotion upload creation, if correct information was entered in conf.py
        if conf.facebookApiKey != None:
            # Create sample facebook information
            facebookInfo = {"title" : "Upload test "  + conf.dateString,
                            "description": "Upload test description" + conf.dateString}

            facebookMeta = StupeflixMeta(facebookInfo)
            # There is no currently notification 
            facebookNotify = None
            uploads += [StupeflixFacebookTokenUpload(conf.facebookApiKey, conf.facebookApiSecret, conf.facebookToken, meta = facebookMeta, notify = facebookNotify)]
            
        # S3 Upload creation : upload to your own S3 bucket
        if conf.s3AccessKey != None:
            # Create an arbitrary location for the resource
            s3resource = "%s/%s/%s" % (user, resource, profileName)
            # Create s3 upload settings
            uploads += [StupeflixS3Upload(bucket=conf.s3Bucket, resourcePrefix = s3resource, accesskey = conf.s3AccessKey, secretkey = conf.s3SecretKey)]

        #  HTTP Uploads creation : POST and PUT
        if conf.httpUploadPrefix != None:
            # Create http POST upload settings
            postURL = conf.httpUploadPrefix + "post/%s/%s/%s" % (user, resource, profileName)
            uploads += [StupeflixHttpPOSTUpload(postURL)]

            # Create http PUT upload settings
            putURL = conf.httpUploadPrefix + "put/%s/%s/%s" % (user, resource, profileName)
            uploads += [StupeflixHttpPUTUpload(putURL)]

        return uploads
    
    def availableKey(self, rank, suffix = "id"):
        return  "available-" + str(rank) + "-" + suffix

    # Check that all went fine, until every uploads is finished (or went on error)
    def waitForCompletion(self, uploadCount):
        error = False
        # Then wait for the generation to complete
        available = False
        status = None
        error = False
        while not available and not error:
            # Retrieve an array of status for every profiles for user and resource
            status = self.client.getStatus(self.user, self.resource, None)            
            print status
            # Variable to test if every profile is available
            for s in status:
                if self.debug:
                    print s
                available = True
                for id in range(uploadCount):
                    availableKey = self.availableKey(id)
                    availableType = self.availableKey(id, "type")
                    if not availableKey in s["status"]:
                        if self.debug:
                            print  "upload #" + str(id)  + " '" + self.uploads[id].__class__.__name__ + "' not yet ready for profile " + s["profile"]
                        available = False
                        break
                    else:                 
                        if self.debug:
                            print  "upload #" + str(id)  + " '" + s["status"][availableType] + "' ready for profile " + s["profile"]

                if s["status"]["status"] == "error":
                    error = True
                    break
            time.sleep(5)
        # if available if False, that means that an error occurred
        return available, status

    def s3WaitLoop(self):
        """Sometimes we have to wait for s3 to make the content available (this is in the Amazon S3 spec). This function is built to do just that."""
        s3Wait = self.s3Wait
        for i in range(self.s3Retries):
            try:
                yield None
            except Exception, e:
                print traceback.format_exc(e)
                if (i + 1) == self.s3Retries:
                    raise
                else:
                    time.sleep(s3Wait)
                    s3Wait *= 2

    def run(self):
        """This is the main function for creating videos, with main calls to the Stupeflix API."""
        # The set of profiles to be created
        profileNames = ["iphone"] # You can add profiles there :  "flash-small, quicktime, dvd ..."
        profileArray = []
        for profileName in profileNames:
            # Create an array of uploads to be executed after the current profile is generated.
            # All upload types will be the same here, but of course you can specify different targets for different profiles.
            uploads = self.uploadsCreate(profileName)
            self.uploads = uploads
            # Create a new profile.
            profileArray += [StupeflixProfile(profileName, uploads = uploads)]

        # Notification is not configured there : this consists in a series of HTTP POST ping request to your own server.
        # This is much more powerful than polling the API as demonstrated in function waitForCompletion.
        notify = None
        # Uncomment this line if you want to test notification. StatusRegexp is used to filter notification sent to your server.
        # Here, only final "available message" would be sent
        # notify =  StupeflixNotify(url = "http://myserver.com/mypath", statusRegexp = "available")

        # Create the set of profiles to be created
        profiles = StupeflixProfileSet(profileArray, meta = None, notify = notify)

        # This is only used to give proper names to output files (file names are appended with a proper extension) 
        profileExtensions = ["mp4"] # flv ...

        # Calls to the API Start there

        # First send the movie definition file to the service. (see sample movie.xml in this directory)
        self.client.sendDefinition(self.user, self.resource, conf.filename)

        # Then launch the generation, using the configuration we have built earlier
        self.client.createProfiles(self.user, self.resource, profiles)
        
        # Poll the API, waiting for completion
        available, status = self.waitForCompletion(uploadCount = len(uploads))

        # Check if everything went fine
        if not available :
            # Something went bad: at least some part of the task was not complete, but some may still have or even was uploaded.
            # This may happen for example if upload to youtube failed but upload to your own server succeeded.
            # an error occured, the status will give more information
            raise Exception, str(status)

        # Download all profiles : this is only valid if a StupeflixDefaultUpload was used in the uploads array
        for i,p in enumerate(profileNames):
            # Print the profile url were the video can be found
            print self.client.getProfileUrl(self.user, self.resource, p)
            movieName = "movie%s.%s" % (p, profileExtensions[i])
            for n in self.s3WaitLoop():
                self.client.getProfile(self.user, self.resource, p, movieName)
                
            # Download the profile thumb url
            thumbName = "thumb_%s.jpg" % p
            for n in self.s3WaitLoop():
                self.client.getProfileThumb(self.user, self.resource, p, thumbName)                

        print "Test succeeded."


def main():
    # Test if the keys were set
    if key.stupeflixAccessKey == None:
        print "ERROR : Please fill in key information in key.py"
        exit(1)
    test = StupeflixTest()
    test.run()
