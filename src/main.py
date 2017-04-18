import os
import logging
from arguments import args
from sync import Sync
from botocore.exceptions import NoCredentialsError

log = logging.getLogger('s3sync')


def go():
    sync = _get_sync_object()
    base_dir = _get_path_to_sync()
    contents = os.listdir(base_dir)

    # loop contents in the base dir
    for element in contents:
        element_path = os.path.join(base_dir, element)
        if os.path.isdir(element_path):
            log.debug('Start to sync the folder {}'.format(element_path))
            # loop files to upload
            for _file in os.listdir(element_path):
                # WARNING: only one level
                if not os.path.isdir(os.path.join(element_path, _file)):
                    sync.upload(dirname=element, path=os.path.join(element_path, _file), filename=_file)
        else:
            sync.upload(path=element_path, filename=element)


def _get_path_to_sync():
    """ check if path exist """
    if not os.path.exists(args._path):
        log.debug('Path "{}" not exist'.format(args._path))
        log.debug('Exit')
        exit(1)
    return args._path


def _get_sync_object():
    """ get sync object """
    try:
        sync = Sync()
        sync.bucket = 'old-ri-images-example'
        return sync
    except NoCredentialsError as ex:
        log.debug('Error to connect to Amazon. Can not found the credentials.')
        log.debug(repr(ex))
        log.debug('Exit')
        exit(1)
