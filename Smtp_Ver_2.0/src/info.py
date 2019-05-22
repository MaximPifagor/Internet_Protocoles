import argparse
import json


class Info:
    def __init__(self):
        self.mail = None
        self.server = None
        self.server_port = None
        self.attachments = None
        self.sender = None
        self.password = None
        self.rcpt = None
        self.subject = None


def read_info_json_file(path):
    info = Info()
    with open(path, "r", encoding="utf-8") as  info_file:
        json_data = json.load(info_file)
    if "server_host_name" in json_data:
        info.server = json_data["server_host_name"]
    if "server_port" in json_data:
        info.server_port = json_data["server_port"]
    if "e-mail" in json_data:
        info.mail = json_data["e-mail"]
    if "attachments_dir" in json_data:
        info.attachments = json_data["attachments_dir"]
    if "sender" in json_data:
        info.sender = json_data["sender"]
    if "rcpt" in json_data:
        info.rcpt = json_data["rcpt"]
    if "password" in json_data:
        info.password = json_data["password"]
    if "subject" in json_data:
        info.subject = json_data["subject"]
    return info
