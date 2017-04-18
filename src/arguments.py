""" parse arguments """

import argparse

args = argparse.ArgumentParser(description="Script so sync files with AWS S3")
args.add_argument('-p', '--path', dest='_path', required=True)
args.add_argument('-c', '--clean', dest='_clean', action='store_true')
args.add_argument('-v', '--verbose', action='store_true')

args = args.parse_args()
