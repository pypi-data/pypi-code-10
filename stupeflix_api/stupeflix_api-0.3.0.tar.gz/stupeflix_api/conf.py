import os
import time

# These are optional variables, by default read from the environement variables, but you can too override them with your own credentials directly.
youtubeLogin = os.getenv("YOUTUBE_LOGIN")
youtubePassword = os.getenv("YOUTUBE_PASSWORD")
youtubeDeveloperKey = os.getenv("YOUTUBE_DEVELOPER_KEY")
youtubeAuthSubToken= os.getenv("YOUTUBE_AUTH_SUB_TOKEN")
dailymotionLogin = os.getenv("DAILYMOTION_LOGIN")
dailymotionPassword = os.getenv("DAILYMOTION_PASSWORD")
s3AccessKey = os.getenv("S3_ACCESS_KEY")
s3SecretKey = os.getenv("S3_SECRET_KEY")
s3Bucket = os.getenv("S3_BUCKET")
httpUploadPrefix = os.getenv("HTTP_UPLOAD_PREFIX")

if os.getenv("STUPEFLIX_TEST_TIME") == None:
    t = time.time()
    dateString = time.strftime("%Ya%ma%da%Ha%Ma%S", time.gmtime(int(t)))
else:
    dateString = os.getenv("STUPEFLIX_TEST_TIME")

filename = os.getenv("STUPEFLIX_MOVIE")
if filename == None:
    filename = "movie.xml"

facebookApiKey = os.getenv("FACEBOOK_API_KEY")
facebookApiSecret = os.getenv("FACEBOOK_API_SECRET")
facebookToken = os.getenv("FACEBOOK_TOKEN")
