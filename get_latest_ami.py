from operator import itemgetter
from unittest import TestCase

import boto3

from constants import OWNER, AMI_NAME

client = boto3.client('ec2')


def get_latest_ami_list(name=AMI_NAME, owner=OWNER):
    list_of_images = client.describe_images(Filters=[{'Name': 'name', 'Values':
        [name, ]}, {'Name': 'owner-id', 'Values': [owner, ]}])
    image_details = sorted(list_of_images['Images'], key=itemgetter(
        'CreationDate'), reverse=True)
    return image_details[0]


def copy_latest_ami():
    latest_ami_info = get_latest_ami_list()
    ami_name = latest_ami_info['Name']
    source_image_id = latest_ami_info['ImageId']
    client.copy_image(Name=ami_name, SourceImageId=source_image_id,
                      SourceRegion='eu-west-1', Encrypted=True)
