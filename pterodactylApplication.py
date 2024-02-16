import requests

class PterodactylApplication:
    def __init__(self, token, url):
        self.token = token
        self.url = url

    def getAllServers(self):
        response = requests.get(self.url + "/api/application/servers", headers={"Authorization": "Bearer " + self.token})
        return response.json()