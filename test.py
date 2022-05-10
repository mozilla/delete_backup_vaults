#!/usr/bin/env python3
from tokenize import Name
from boto3 import client
from json_utils import load_json_file, write_json_file
from pprint import pprint
from functools import reduce

#vaults = load_json_file("data/vaults.json")
#stacks = load_json_file("data/stacks.json")
#vaults_to_keep = load_json_file("data/vaults_to_keep.json")

#print("vaults")
#pprint(vaults) # PRETTY PRINT ALL VAULTS AND THEIR DATA

#print("stacks")
#pprint(stacks)

#print("Vaults To Keep")
#pprint(vaults_to_keep)

#print(valuts_data.get("BackupVaultList")[9]) # gets 10th backup vault and prints the info


"""
### QUERY TOTAL RECOVERY POINTS AND PRINT THE TOTAL TO THE COMMAND LINE ###

index = 0
total_recovery_points = 0

total_vaults = len(vaults.get("BackupVaultList"))


while index in range(0, total_vaults):
	recovery_points = vaults.get("BackupVaultList")[index].get("NumberOfRecoveryPoints")
	total_recovery_points = total_recovery_points + recovery_points
	index = index + 1
	

#print(total_recovery_points)  # 84,138 recovery points

def get_number_of_recovery_points_per_vault(vault):
	#vault_recovery_points = vaults.get("BackupVaultList")[vault].get("NumberOfRecoveryPoints")
	return vault.get("NumberOfRecoveryPoints")



print(list(map(get_number_of_recovery_points_per_vault, vaults.get("BackupVaultList"))))

"""


# 1)  Get list of all vaults.

#vaults = load_json_file("data/vaults.json")


# 2)  Filter out the ones we want to keep.

vaults_to_keep = load_json_file("./data/vaults_to_keep.json")

def should_delete_vault(vault):
    return vault.get("BackupVaultName") not in vaults_to_keep

vaults = load_json_file("./data/vaults.json").get("BackupVaultList")
vaults_to_delete = list(filter(should_delete_vault, vaults))

#pprint(vaults_to_delete)

vaultNames = []

def getVaultNames(vault):
	return vault.get("BackupVaultName")


vaultNames = list(map(getVaultNames, vaults_to_delete))[0:4]   # only the first 4

# Prints a list of all vault names to delete.  63 in total.
#pprint(vaultNames)


# 3)  Query recovery points for each vault to delete.




def getAllRecoveryPoints(vaultName):
	data =  client("backup").list_recovery_points_by_backup_vault(BackupVaultName = vaultName)
	#print ("Data is:")
	#pprint(data)
	recoveryPointsList = data.get("RecoveryPoints")
	#print("Recovery Point are: ") 
	#pprint(recoveryPointsList)
	return recoveryPointsList
listOfRecoveryPointLists = list(map(getAllRecoveryPoints, vaultNames))


def concat(listA, listB):
    return listA + listB


def flatten(listOfLists):
    return reduce(concat, listOfLists)


flattenedListOfRecoveryPoints = flatten(listOfRecoveryPointLists)


# pprint(recoveryPointsList)
# print(len(recoveryPointsList))
# NEED TO GET REOVERY POINT ARN FOR EACH


def getNameAndARN(recoveryPoint):
    name = recoveryPoint.get("BackupVaultName")
    arn = recoveryPoint.get("RecoveryPointArn")
    myDict = {"BackupVaultName": name, "RecoveryPointArn": arn}
    return myDict


stuffToDelete = list(map(getNameAndARN, flattenedListOfRecoveryPoints))
# pprint(stuffToDelete)


"""
def getBackupVaultArn(BackupVaultName):
	return BackupVaultName.get("RecoveryPointArn")

RecoveryPointArnList = list(map(getBackupVaultArn, recoveryPointNames))

pprint(RecoveryPointArnList)  # I get "None" 63 times.  Something isn't right... 
"""


# 4)  Delete recovery points.


def deleteRecoveryPoint(nameAndArn):
    name = nameAndArn.get("BackupVaultName")
    arn = nameAndArn.get("RecoveryPointArn")
    client('backup').delete_recovery_point(
        BackupVaultName = name,
        RecoveryPointArn = arn
		)
    print("Ok, time to delete ", name, arn)
list(map(deleteRecoveryPoint, stuffToDelete))

# 5)  Delete vault.


def deleteVault(name):
     print("OK, time to delete a vault... ", name)
     client('backup').delete_backup_vault(
		 BackupVaultName= name
	 )


list(map(deleteVault, vaultNames))
