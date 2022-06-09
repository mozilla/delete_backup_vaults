#!/usr/bin/env python3
from tokenize import Name
from boto3 import client
from json_utils import load_json_file, write_json_file
from pprint import pprint
from functools import reduce
from time import sleep
from botocore.exceptions import ClientError
from termcolor import cprint

from stack_utils import getAllVaults, getVaultsToKeep, filterVaults
from vault_utils import deleteVault

def name_has_daily_backup(name):
    return str.find(name, "daily-backup") >= 0

allVaults = getAllVaults()
vaultsToKeep = getVaultsToKeep()
vaultsToDelete = list(filter(name_has_daily_backup, filterVaults(allVaults, vaultsToKeep)))

for vault in vaultsToDelete:
    cprint("Here are the vaults we want to keep:", "green")
    pprint(vaultsToKeep)
    print()
    cprint(f"Vault to delete:       {vault}  ", "red")
    choice = input(f"Delete this vault? (Type \"confirm\"): ").strip().lower()
    if choice == "confirm":
        print("Okay, deleting...")
        deleteVault(vault)
    else:
    	print("Skipping this vault.")
    print()
    print()
