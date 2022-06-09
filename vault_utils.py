#!/usr/bin/env python3
from tokenize import Name
from boto3 import client
from json_utils import load_json_file, write_json_file
from pprint import pprint
from functools import reduce
from time import sleep
from botocore.exceptions import ClientError


def getAllRecoveryPoints(vaultName):
	data =  client("backup").list_recovery_points_by_backup_vault(BackupVaultName = vaultName)
	recoveryPointsList = data.get("RecoveryPoints")
	return recoveryPointsList


def deleteRecoveryPoint(recoveryPoint):
    name = recoveryPoint.get("BackupVaultName")
    arn = recoveryPoint.get("RecoveryPointArn")
    client('backup').delete_recovery_point(
        BackupVaultName = name,
        RecoveryPointArn = arn
		)


def emptyVault(vaultName):
	points = getAllRecoveryPoints(vaultName)
	if not points:
		print("This vault has no recovery points.")
		return True

	print("Okay, deleting", len(points), "recovery points.")
	for point in points:
		deleteRecoveryPoint(point)
	sleep(3)
	resultingPoints = getAllRecoveryPoints(vaultName)
	if len(resultingPoints) == 0:
		return True
	else:
		return False


# make sure vault exists
def backupVaultExists(vaultName):
	try:
		response = client('backup').describe_backup_vault(BackupVaultName = vaultName)
		#print("The response was: ", response)
		return True
	except ClientError as error:
		#print("The error was: ", error)
		return False


defaultAttempts = 50
def deleteVault(vaultName, attempts=defaultAttempts):
	if (attempts == defaultAttempts):
		print(f"Deleting vault: {vaultName}")
	else:
		print(f"Number of attempts remaining #{attempts}")

	if (attempts == 0):
		print(f"Failed to delete vault: {vaultName}")
		return false

	if backupVaultExists(vaultName) == False:
		# raise error
		print("Vault", vaultName, "does not exist!")
		return


	vaultIsEmpty = emptyVault(vaultName)
	if vaultIsEmpty == True:
		client('backup').delete_backup_vault(BackupVaultName= vaultName)
		sleep(3)
		if backupVaultExists(vaultName) == False:
			print("Vault", vaultName,  "was successfully deleted.")
		else:
			deleteVault(vaultName, attempts-1)
	else:
		deleteVault(vaultName, attempts-1)
