#!/usr/bin/env python3
from tokenize import Name
from boto3 import client
from json_utils import load_json_file, write_json_file
from pprint import pprint
from functools import reduce
from time import sleep
from botocore.exceptions import ClientError

from stack_utils import getAllVaults, getVaultsToKeep, filterVaults
from vault_utils import deleteVault


# 1. GET ALL BACKUP VAULTS  (STACK_UTILS.PY)

allVaults = getAllVaults()  # done

# 2. VAULTS TO KEEP (FROM STACK_UTILS.PY)

vaultsToKeep = getVaultsToKeep()

# 3. FILTER LIST OF ALL VAULT NAMES AND REMOVE THE ONES WE WANT TO  KEEP

vaultsToDelete = filterVaults(allVaults, vaultsToKeep)[0:10]
print("Vaults to delete: ")
pprint(vaultsToDelete)
print("Vaults to keep: ")
pprint(vaultsToKeep)

choice = input("Do you wish to continue with vault deletion? (yes/no): ").strip().lower()

if choice != "yes":
	print("Exiting.")
	exit()

print("Okay, continuing...")

# 4. DELETE VAULTS ON THE CHOPPING BLOCK

for vault in vaultsToDelete:
	deleteVault(vault)

