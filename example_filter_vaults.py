#!/usr/bin/env python3

from json_utils import load_json_file, write_json_file

vaults_to_keep = load_json_file("./data/vaults_to_keep.json")


def should_delete_vault(vault):
    return vault.get("BackupVaultName") not in vaults_to_keep


vaults = load_json_file("./data/vaults.json").get("BackupVaultList")
vaults_to_delete = list(filter(should_delete_vault, vaults))

print(
    "There are",
    len(vaults),
    "backup vaults. We should delete",
    len(vaults_to_delete),
    "of them.",
)
