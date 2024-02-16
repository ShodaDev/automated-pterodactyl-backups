import datetime
import schedule
import time

import config from config

import pterodactylClient as PterodactylClient
import pterodactylApplication as PterodactylApplication


def main():
    print("--------------------")
    print("STARTING BACKUP SYSTEM JOB")
    print("--------------------")
    pterodactylClient = PterodactylClient.PterodactylClient(config.client_api_key, config.base_uri)
    pterodactylApplication = PterodactylApplication.PterodactylApplication(config.application_api_key, config.base_uri)

    allServers = pterodactylApplication.getAllServers()
    allServers = allServers["data"]

    # backup creation:
    for server in allServers:
        serverIdentifier = server["attributes"]["identifier"]
        if (server["attributes"]["suspended"] == True):
            print("Skipping server " + serverIdentifier + " because it is suspended")
            continue
        pterodactylClient.createBackup(serverIdentifier)
        print("Created backup for server " + serverIdentifier)

    print("Done creating backups for all servers")

    # backup deletion:
    for server in allServers:
        serverIdentifier = server["attributes"]["identifier"]
        if (server["attributes"]["suspended"] == True):
            print("Skipping server " + serverIdentifier + " because it is suspended")
            continue
        allBackups = pterodactylClient.getAllBackups(serverIdentifier)
        allBackups = allBackups["data"]

        for backup in allBackups:
            date = datetime.datetime.now(datetime.timezone.utc)
            backupCreatedAt = backup["attributes"]["created_at"]
            backupId = backup["attributes"]["uuid"]

            if (date - datetime.datetime.strptime(backupCreatedAt, "%Y-%m-%dT%H:%M:%S%z")) < datetime.timedelta(days=config.delete_after_days):
                print("Not deleting backup " + backupId + " for server " + serverIdentifier + " because it is not older than 5 days")

            else :
                pterodactylClient.deleteBackup(serverIdentifier, backupId)
                print("Deleted backup " + backupId + " for server " + serverIdentifier)

    print("Done deleting backups older than 5 days for all servers")
    print("--------------------")
    print("ENDING BACKUP SYSTEM JOB")
    print("--------------------")


schedule.every().day.at("00:00").do(main)
print("Scheduled backup creation and deletion for 00:00 UTC every day")

while True:
    schedule.run_pending()
    time.sleep(1)
