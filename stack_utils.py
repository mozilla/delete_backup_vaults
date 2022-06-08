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
"DELETE_FAILED",
"DELETE_IN_PROGRESS",
"REVIEW_IN_PROGRESS",
"ROLLBACK_COMPLETE",
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
    return resource.get("LogicalResourceId") == "DailyBackupVault"


def get_backup_vault(resources):
    return list(filter(is_backup_vault, resources))[0]


def get_vault_id(vault):
    return vault.get("PhysicalResourceId")


def getVaultsToKeep():
    stacks = get_stacks()
    root_stacks = filter(hasNoParent, stacks)
    resources = map(get_stack_resources, root_stacks) # PASSING root_stacks HERE
    backup_vaults = list(map(get_backup_vault, resources))
    vaults_to_keep = list(map(get_vault_id, backup_vaults))  # had to make this a list
    return vaults_to_keep


def filterVaults(allVaults, vaultsToKeep):
    allVaultNames = []
    for vault in allVaults:
        name = vault.get("BackupVaultName")
        allVaultNames.append(name)
    choppingBlock = [x for x in allVaultNames if x not in vaultsToKeep]
    return choppingBlock

