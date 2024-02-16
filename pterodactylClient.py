import requests


class PterodactylClient:
    def __init__(self, token, url):
        self.token = token
        self.url = url

    def createBackup(self, identifier):
        response = requests.post(self.url + "/api/client/servers/" + identifier + "/backups",
                                 headers={"Authorization": "Bearer " + self.token})
        return response.text

    def deleteBackup(self, identifier, backupId):
        response = requests.request("DELETE", self.url + "/api/client/servers/" + identifier + "/backups/" + backupId, headers={"Authorization": "Bearer " + self.token})
        return response.text

    def getAllBackups(self, identifier):
        response = requests.get(self.url + "/api/client/servers/" + identifier + "/backups", headers={"Authorization": "Bearer " + self.token})
        return response.json()
