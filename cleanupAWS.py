#!/usr/bin/env python3
from tokenize import Name
from boto3 import client
from json_utils import load_json_file, write_json_file
from pprint import pprint
from functools import reduce
from time import sleep
from botocore.exceptions import ClientError

from vault_utils import deleteVault



vaultArray = [
	"jfs-beta-daily-backup-974e80c0",
	"jfs-2022-05-02-daily-backup-052e3ff0",
	"jfs-beta-daily-backup-974e80c0"
	]


#deleteVault(vaultArray)

for vault in vaultArray:
	deleteVault(vault)