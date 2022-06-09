#!/usr/bin/env python3

from boto3 import client
from pprint import pprint


def getAllVaults():
    return client("backup").list_backup_vaults().get("BackupVaultList")


# "DELETE_COMPLETE" status might have been a better way to approach this
statusCode = [
"CREATE_COMPLETE",
"CREATE_IN_PROGRESS",
"CREATE_FAILED",
# "DELETE_FAILED", # Let's leave these stacks alone until we know why they failed
"DELETE_IN_PROGRESS",
"REVIEW_IN_PROGRESS",
"ROLLBACK_FAILED",
"ROLLBACK_IN_PROGRESS",
"UPDATE_COMPLETE",
"UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
"UPDATE_FAILED",
"UPDATE_IN_PROGRESS",
"UPDATE_ROLLBACK_COMPLETE",
"UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
"UPDATE_ROLLBACK_FAILED",
"UPDATE_ROLLBACK_IN_PROGRESS"
]


def hasNoParent(stack):
    return stack.get("ParentId") == None


def get_stacks():
    return client("cloudformation").list_stacks(StackStatusFilter=statusCode).get("StackSummaries")


def get_stack_resources(stack):
    return (
        client("cloudformation")
        .list_stack_resources(StackName=stack.get("StackName"))
        .get("StackResourceSummaries")
    )


def is_backup_vault(resource):
    return resource.get("PhysicalResourceId") and resource.get("LogicalResourceId") == "DailyBackupVault"


def get_backup_vault(resources):
    for resource in resources:
        if is_backup_vault(resource):
            return resource
    raise Exception("Failed to find the backup fault, error!")


def get_vault_id(vault):
    return vault.get("PhysicalResourceId")

hubs_cloud_description = "Hubs Cloud: Private Social VR in your web browser. Your own self-hosted hub powered by Hubs by Mozilla. Full documentation: https://github.com/mozilla/hubs-cloud\n"
def is_hubs_cloud_stack(stack):
    return hasNoParent(stack) and stack.get("TemplateDescription") == hubs_cloud_description

def getVaultsToKeep():
    hubs_cloud_stacks = filter(is_hubs_cloud_stack, get_stacks())
    resources = map(get_stack_resources, hubs_cloud_stacks)
    backup_vaults = map(get_backup_vault, resources)
    return list(map(get_vault_id, backup_vaults))

def filterVaults(allVaults, vaultsToKeep):
    allVaultNames = []
    for vault in allVaults:
        name = vault.get("BackupVaultName")
        allVaultNames.append(name)
    choppingBlock = [x for x in allVaultNames if x not in vaultsToKeep]
    return choppingBlock

