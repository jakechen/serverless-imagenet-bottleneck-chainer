import os
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Set CHAINER_DATASET_ROOT environment variable so Chainer can download
# pre-trained model definitions to another filesystem
os.environ['CHAINER_DATASET_ROOT'] = '/dev/shm/.chainer/dataset'

# Download ResNet-50-model.caffemodel, which chainer needs in order to
# load pre-trained model
s3 = boto3.client('s3')
s3. download_file(
    'jakechenawstemp', 
    'ResNet-50-model.caffemodel',
    '/dev/shm/.chainer/dataset/pfnet/chainer/models/ResNet-50-model.caffemodel'
)

# Load pre-trained model
from chainer.links import ResNet50Layers
from chainer.links.model.vision.resnet import prepare
model = ResNet50Layers()


def lambda_function(event, context):
    logger.debug(event)
    
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        logger.debug(s3_bucket)
        logger.debug(s3_key)
        
        img_path = '/dev/shm/{}'.format(s3_key) # where to download image
        feat_path = '/dev/shm/{}.npy'.format(s3_key) # where to save features
        
        boto3.download_file(s3_bucket,
                            s3_key,
                            '/dev/shm/{}'.format(s3_key))
        
        print(response)