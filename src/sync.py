import os
import logging
import boto3
from boto3.exceptions import S3UploadFailedError
from src.arguments import args
from botocore.exceptions import ClientError


log = logging.getLogger('s3sync')


class Sync(object):

    def __init__(self):
        self.s3 = boto3.client('s3')
        self._bucket = None

    @property
    def bucket(self):
        return self._bucket

    @bucket.setter
    def bucket(self, value):
        """ checking if bucket exist, if not, create it """
        buckets = self.s3.list_buckets()
        log.debug('Checking if bucket {} exist'.format(value))
        if value not in [bucket['Name'] for bucket in buckets['Buckets']]:
            log.debug('Creating bucket {}'.format(value))
            self.s3.create_bucket(Bucket=value)

        self._bucket = value

    def upload(self, **kwargs):
        """ upload to amazon s3 """
        try:
            if 'path' in kwargs and 'filename' in kwargs:
                with open(kwargs['path'], 'rb') as data:
                    log.debug('Sync file {}'.format(kwargs['path']))
                    s3_dest = self._get_s3_destination(**kwargs)

                    # upload to aws s3 and make it public
                    self.s3.upload_fileobj(data, self.bucket, s3_dest, ExtraArgs={'ACL': 'public-read'})

                    # clean local file?
                    if args.clean:
                        self._remove_local_file(s3_dest, **kwargs)
            else:
                log.debug('Path or File name not exist.')
        except IOError as ex:
            log.debug('Error to find file to upload {}'.format(kwargs['path']))
            log.debug(repr(ex))
            log.debug('Exit')
            exit(1)
        except S3UploadFailedError as ex:
            log.debug('Error upload to S3: {}'.format(kwargs['path']))
            log.debug(repr(ex))
            log.debug('Exit')
            exit(1)

    @staticmethod
    def _get_s3_destination(**kwargs):
        return '{}/{}'.format(kwargs['dirname'], kwargs['filename']) \
                        if 'dirname' in kwargs else kwargs['filename']

    def _remove_local_file(self, s3_dest, **kwargs):
        """ remove local file if it exist in S3"""
        try:
            self.s3.head_object(Bucket=self.bucket, Key=s3_dest)
            log.debug('Remove file {}'.format(kwargs['path']))
            os.remove(kwargs['path'])
        except ClientError as ex:
            log.debug('Not found "{}" in AWS S3.'.format(s3_dest))
            log.debug(repr(ex))
