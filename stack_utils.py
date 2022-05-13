#!/usr/bin/env python3

from boto3 import client
from json_utils import write_json_file

stacks = (
    client("cloudformation")
    .list_stacks(
        StackStatusFilter=[
            "CREATE_COMPLETE",
        ]
    )
    .get("StackSummaries")
)


def hasNoParent(stack):
    return stack.get("ParentId") == None


root_stacks = filter(hasNoParent, stacks)
write_json_file("data/stacks.json", list(root_stacks))
print("Wrote ./data/stacks.json")


def getAllVaults():
    return client("backup").list_backup_vaults().get("BackupVaultList")



# FROM EXAMPLE_LIST_STACK_OWNED_VAULTS.PY
# ========================================

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


#stacks = load_json_file("data/stacks.json")
resources = map(get_stack_resources, stacks)
backup_vaults = map(get_backup_vault, resources)
#vaults_to_keep = map(get_vault_id, backup_vaults)

# ========================================




def activeVaults(backup_vaults):
    vaults_to_keep = map(get_vault_id, backup_vaults)
    return vaults_to_keep




