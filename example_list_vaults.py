#!/usr/bin/env python3

from boto3 import client
from json_utils import write_json_file

vaults_data = client("backup").list_backup_vaults()
write_json_file("data/vaults.json", vaults_data)
