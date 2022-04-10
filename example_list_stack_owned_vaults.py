#!/usr/bin/env python3

from boto3 import client
from json_utils import load_json_file, write_json_file


def get_resources(stack):
    return (
        client("cloudformation")
        .list_stack_resources(StackName=stack.get("StackName"))
        .get("StackResourceSummaries")
    )


def is_backup_vault(resource):
    return resource.get("LogicalResourceId") == "DailyBackupVault"


def get_backup_vault(resources):
    return list(filter(is_backup_vault, resources))[0]


def get_vault_id(vault):
    return vault.get("PhysicalResourceId")


stacks = load_json_file("data/stacks.json")
resources = map(get_resources, stacks)
backup_vaults = map(get_backup_vault, resources)
vaults_to_keep = map(get_vault_id, backup_vaults)

write_json_file("data/vaults_to_keep.json", list(vaults_to_keep))
