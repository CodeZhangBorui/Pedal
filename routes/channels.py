"""Handler of APIs about channels (adpaters, new, overview...)."""

import json
import importlib
import sqlite3
from flask import Blueprint, request

import orion
import functions.authentication as authed

channels = Blueprint("channels", __name__)

users = orion.Users("pedal.db", ["email"])
session = orion.Sessions("pedal.db")
permissions = orion.Permissions("pedal.db")
auditlog = orion.AuditLog("pedal.db")
configuration = orion.Configuration("pedal.db")


# Read config.json for adapters
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)
    adapter_list = config["adapters"]

# Import adapters' modules
adapter_module = {}
for adapt in adapter_list:
    adapter_module[adapt] = importlib.import_module(f"adapters.{adapt}")


@channels.route("/api/adapters/list", methods=["GET"])
def list_adapters():
    """List all adapters."""
    if not authed.verify_request(request)["auth"]:
        return {"success": False, "reason": "unauthorized"}
    return {"success": True, "data": adapter_list}


@channels.route("/api/channels/create", methods=["POST"])
def create_channel():
    """Create a new channel."""
    try:
        adapter = request.json["adapter"]
        channel_name = request.json["channel_name"]
        paneladdr = request.json["paneladdr"]
        apikey = request.json["apikey"]
    except KeyError:
        return {"success": False, "message": "Invalid request"}, 400
    authen = authed.verify_request(request)
    if not authen["auth"]:
        return {"success": False, "message": "Unauthorized"}, 403
    if not permissions.has_permission(authen["username"], "group.admin"):
        return {"success": False, "message": "Permission denied"}, 403
    if adapter not in adapter_list:
        return {"success": False, "message": "Adapter not found"}
    remote_obj = adapter_module[adapter].MCSManager(paneladdr, {"apikey": apikey})
    remote_overview = remote_obj.overview()
    if remote_overview["success"]:
        conn = sqlite3.connect("pedal.db")
        c = conn.cursor()
        c.execute("SELECT id FROM channels")
        if not c.fetchone():
            max_channel_id = 0
        else:
            c.execute("SELECT MAX(id) FROM channels")
            max_channel_id = c.fetchone()[0]
        c.execute(
            "INSERT INTO channels (id, name, adapter, paneladdr, apikey, username, instances_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (max_channel_id + 1, channel_name, adapter, paneladdr, apikey, remote_overview["data"]["username"], remote_overview["data"]["instances_count"]),
        )
        conn.commit()
        return {"success": True, "data": remote_overview["data"]}
    return {"success": False, "message": remote_overview["reason"]}

@channels.route("/api/channels/list", methods=["GET"])
def list_channel():
    """List all channels."""
    authen = authed.verify_request(request)
    if not authen["auth"]:
        return {"success": False, "message": "Unauthorized"}, 403
    if not permissions.has_permission(authen["username"], "group.admin"):
        return {"success": False, "message": "Permission denied"}, 403
    conn = sqlite3.connect("pedal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM channels")
    dirty_channels = c.fetchall()
    channels_list = []
    for channel in dirty_channels:
        channels_list.append(
            {
                "id": channel[0],
                "channel_name": channel[1],
                "adapter": channel[2],
                "paneladdr": channel[3],
                "apikey": channel[4],
                "username": channel[5],
                "instances_count": channel[6]
            }
        )
    return {"success": True, "data": channels_list}

@channels.route("/api/channelss/<channel>/overview", methods=["GET"])
def overview(adapter):
    """Get the overview of the channel."""
    # if not authed.verify_request(request)['auth']:
    #     return {'success': False, 'reason': 'unauthorized'}
    # if adapter not in adapter_list:
    #     return {'success': False, 'reason': 'adapter_not_found'}
    # return adapter_module[adapter].overview()
    return {}
