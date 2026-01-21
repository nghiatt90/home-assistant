#!/usr/bin/env python
# -*- coding: utf-8 -*-

# home_assistant.api
# Date: 2023/06/12
# Filename: api

__author__ = "Yoshi Truong"
__date__ = "2023/06/12"


import base64
from datetime import datetime
import hashlib
import hmac
import requests
import uuid

TOKEN = "c91***2cc"
SECRET_KEY = "717***7be"

API_ENDPOINT = "https://api.switch-bot.com"
API_VERSION = "v1.0"


def signed_headers(request_type="GET"):
    nonce = uuid.uuid4()
    t = int(datetime.now().timestamp())
    string_to_sign = f"{TOKEN}{t}{nonce}"

    string_to_sign = bytes(string_to_sign, "utf-8")
    secret = bytes(SECRET_KEY, "utf-8")

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    header = {
        "Authorization": TOKEN,
        "t": str(t),
        "sign": str(sign, "utf-8"),
        "nonce": str(nonce),
    }
    if request_type == "POST":
        header["Content-Type"] = "application/json"
        header["charset"] = "utf8"
    return header


def get_all_devices():
    url = f"{API_ENDPOINT}/{API_VERSION}/devices"
    headers = signed_headers()
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


if __name__ == '__main__':
    print(get_all_devices())
