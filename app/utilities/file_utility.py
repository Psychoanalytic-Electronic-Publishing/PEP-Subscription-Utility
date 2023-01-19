import boto3
import uuid
import os
import glob
from zipfile import ZipFile
from xml.etree import ElementTree
s3_client = boto3.client('s3')


def download_subscription_file(record):
    download_path = None
    try:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = f'/tmp/{uuid.uuid4()}_{key}'

        print(f'downloading {bucket}/{key} to {download_path}')
        s3_client.download_file(bucket, key, download_path)
    except Exception as err:
        print(f'Error downloading s3 file: {err}')
        raise
    return download_path


def unzip(file_path):
    extraction_path = os.path.splitext(file_path)[0]
    try:
        print(f'Unzipping to {extraction_path}')
        with ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.splitext(file_path)[0])
    except Exception as err:
        print(f'Error unzipping file: {err}')
        raise
    return extraction_path


def parse_subscription_files(dir_path):
    try:
        files = glob.glob(f'{dir_path}/*.xml', recursive=True)
        xml_data = None
        for f in files:
            print(f'Parsing {f}')
            data = ElementTree.parse(f).getroot()
            if xml_data is None:
                xml_data = data
            else:
                xml_data.extend(data)
        return xml_data
    except Exception as err:
        print(f'Error parsing subscription file: {err}')
        raise
