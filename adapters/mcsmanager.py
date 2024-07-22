"""The official adapter for MCSManager on Pedal. Also used for example."""

import requests
import json


class MCSManager:
    """The official adapter for MCSManager on Pedal. Also used for example."""

    def __init__(self, paneladdr, credentials):
        """Initialize the adapter with the given credentials."""
        self.paneladdr = paneladdr
        self.apikey = credentials["apikey"]
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
        }
        self.params = {
            "apikey": self.apikey,
        }

    def overview(self):
        """Get the overview of the account."""
        res = requests.get(
            f"{self.paneladdr}/api/auth?apikey={self.apikey}", headers=self.headers
        )
        data = res.json()
        print(data)
        if data["status"] == 200:
            return {
                "success": True,
                "data": {
                    "uuid": data["data"]["uuid"],
                    "username": data["data"]["userName"],
                    "instances": data["data"]["instances"], 
                    "instances_count": len(data["data"]["instances"]),   
                },
            }
        elif data["status"] == 403:
            return {
                "success": False,
                "reason": "invaild_apikey",
            }
        elif data["status"] == 500:
            return {
                "success": False,
                "reason": "remote_unavailable",
            }
