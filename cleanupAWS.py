#!/usr/bin/env python3
from tokenize import Name
from boto3 import client
from json_utils import load_json_file, write_json_file
from pprint import pprint
from functools import reduce
from time import sleep
from botocore.exceptions import ClientError

from stack_utils import getAllVaults, vaults_to_keep, filterVaults, backup_vaults
from vault_utils import deleteVault #, getAllActiveVaults



"""
1.  Get all backup vaults
2.  Get all backup vaults associated with active stacks - we don't want to delete these
3.  Filter backup vaults so that they don't include ones with active stacks
4.  Delete remaining vaults

"""


# 1. GET ALL BACKUP VAULTS  (STACK_UTILS.PY)

allVaults = getAllVaults()  # done

#pprint(allVaults)
#print(len(allVaults))
#print(allVaults[0])
#print(allVaults[0].get("NumberOfRecoveryPoints"))  <--- access first vault and list num recover pts


# 2. VAULTS TO KEEP (FROM STACK_UTILS.PY)

#pprint(list(vaults_to_keep))

# 3. FILTER LIST OF ALL VAULT NAMES AND REMOVE THE ONES WE WANT TO  KEEP

allVaultNames = []

for vault in allVaults:
	name = vault.get("BackupVaultName")
	allVaultNames.append(name)

# ALL VAULT NAMES
#pprint(allVaultNames)   # <---- prints all vault names
#print(len(allVaultNames))  # 95 today

#print("#####################################")

# VAULTS TO KEEP
#pprint(list(vaults_to_keep))
#print(len(list(vaults_to_keep)))  # 4... says 0 but lists 4 today, why???



def vaults_to_delete(vault):
	return vault not in vaults_to_keep

choppingBlock = filter(vaults_to_delete, "jfs-2022-06-06-daily-backup-c5758630")

print(list(choppingBlock))

#print("Number of vaults to delete:")
#print(len(list(choppingBlock)))


#pprint(list(backup_vaults))
# ^^ these 4 aren't even occurring in my list of vaults.  WHY?
# Am I comparing apples and oranges?


