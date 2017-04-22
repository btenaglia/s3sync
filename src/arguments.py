""" parse arguments """

import argparse

args = argparse.ArgumentParser(description="Script so sync files with AWS S3")
# path to sync
args.add_argument('-p', '--path', dest='path', required=True)
# bucket name
args.add_argument('-b', '--bucket', dest='bucket', required=True)
# remove file for local storage
args.add_argument('-c', '--clean', dest='clean', action='store_true')
# verbose
args.add_argument('-v', '--verbose', action='store_true')

args = args.parse_args()
