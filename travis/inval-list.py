#! /usr/bin/env python

"""
This script creates an invalidation batch for use by the AWS CLI. 

https://docs.aws.amazon.com/cli/latest/reference/cloudfront/create-invalidation.html

Files are listed from `site` and output is written to `target`. 
"""

import os
import time
import json

def pretty_time():
    return '-'.join(time.strftime('%c').split())

def list_files(site, name):
    base = site + name
    files = [name]
    for f in os.listdir(base):
        path = os.path.join(base, f)
        if os.path.isfile(path):
            files.extend([name + f])
        if os.path.isdir(path):
            files.extend(list_files(site, name + f + "/"))

    return files

def build_payload(site):
    # translations
    files = list_files(site, "/")

    return {
        "Paths": {"Quantity": len(files), "Items": list(files)},
        "CallerReference": f"travis-{pretty_time()}",
    }

def write_output(obj, target):
    with open(target, "w") as f:
        json.dump(obj, f)

def main():
    site = "_site"
    target = "payload.json"
    payload = build_payload(site)
    write_output(payload, target)

if __name__ == "__main__":
    main()
