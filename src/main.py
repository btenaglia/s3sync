import os
import logging
from arguments import args
from sync import Sync

log = logging.getLogger('s3sync')


def go():
    sync = Sync()
    sync.bucket = 'old-ri-images-example'
    base_dir = _get_path_to_sync()
    contents = os.listdir(base_dir)

    # loop contents in the base dir
    for element in contents:
        element_path = os.path.join(base_dir, element)
        if os.path.isdir(element_path):
            log.debug('Start to sync the folder {}'.format(element_path))
            # loop files to upload
            for _file in os.listdir(element_path):
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