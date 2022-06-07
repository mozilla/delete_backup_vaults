#!/usr/bin/env python3

from boto3 import client

#from json_utils import write_json_file

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
#write_json_file("data/stacks.json", list(root_stacks))
#print("Wrote ./data/stacks.json")




def getAllVaults():
    return client("backup").list_backup_vaults().get("BackupVaultList")






#def activeVaults(backup_vaults):
    #vaults_to_keep = map(get_vault_id, backup_vaults)
    #return vaults_to_keep




#######

# FROM EXAMPLE LIST STACKS



def hasNoParent(stack):
    return stack.get("ParentId") == None





# FROM EXAMPLE_LIST_STACKS.PY
def get_stacks():
    return client("cloudformation").list_stacks(StackStatusFilter=["CREATE_COMPLETE",]).get("StackSummaries")



# FROM EXAMPLE LIST OWNED STACKS

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


stacks = get_stacks()
root_stacks = filter(hasNoParent, stacks)
resources = map(get_stack_resources, root_stacks) # PASSING root_stacks HERE
backup_vaults = map(get_backup_vault, resources)
vaults_to_keep = map(get_vault_id, backup_vaults)



def filterVaults(vaults):
    for vault in vaults:
        if vault not in vaults_to_keep:
            return vault
        else:
            break



"""
# ALL VAULT NAMES ONLY

allVaultNames = []

for vault in allVaults:
    name = vault.get("BackupVaultName")
    allVaultNames.append(name)
"""