from batchcompute import CN_QINGDAO 
# Your access_id and secret_key pair
ID = '5slyhuy4sv30bmppvgew0rps'
KEY = 'NGYL1I7hXC6SgSqkcE5DJdPgJM8='
assert ID and KEY, 'You must supply your accsess_id and secret key.'
REGION = CN_QINGDAO

OSS_HOST = 'oss-cn-qingdao.aliyuncs.com'
OSS_BUCKET = 'diku-e2e-test-qingdao'
assert OSS_HOST and OSS_BUCKET, 'You also must supply a bucket \
    created with the access_id above.'

IMAGE_ID = 'img-linux-1423801256'
assert IMAGE_ID, "You'd better specify a valid image id."

# COUNT_TASK_NUM is the total instance count
COUNT_TASK_NUM = 2
SUM_TASK_NUM = 1

# The start number and end number which
# specify the region you want to find prime
DATA_START = 1
DATA_END = 10000

PATH_TMPL = 'oss://%s/%s'

PACKAGE_PATH = 'batch_python_sdk/package/worker.tar.gz'
# FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)
FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)

DATA_PATH = 'batch_python_sdk/data/'
FULL_DATA = PATH_TMPL%(OSS_BUCKET, DATA_PATH)
LOCAL_DATA = '/home/admin/batch_python_sdk/'

OUTPUT_PATH = 'batch-python-sdk/output/find_task_result.txt'
FULL_OUTPUT = PATH_TMPL%(OSS_BUCKET, OUTPUT_PATH)

LOG_PATH = 'oss://%s/batch_python_sdk/logs/'%OSS_BUCKET

MAIL_SERVER = 'smtp-inc.alibaba-inc.com'
MAIL_FROM = 'cloud-diku@alibaba-inc.com'
MAIL_PASS = 'Caiyun123456'
MAIL_TO = 'cloud-diku@list.alibaba-inc.com'
# MAIL_TO = 'helei.hl@alibaba-inc.com'
MAIL_CC = ''
