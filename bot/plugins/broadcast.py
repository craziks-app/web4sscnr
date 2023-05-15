#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Prince Mendiratta
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundatier version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import sys
import os
import os.path
import requests
import threading
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import AUTH_CHANNEL, REQUEST_INTERVAL, TG_BOT_TOKEN, MONGO_URL, MY_CHANNEL
from os import path
from bot.hf.request import request_time
from bot.mongodb.users import user_list, remove_client_from_db
from datetime import datetime
from pyrogram.errors.exceptions import UserIsBlocked, ChatWriteForbidden
from bot import logging
import subprocess


def get_mod(client: Client):
    req_result = request_time(Client)
    if req_result[0] == 404:
        mes2 = "[{}]: SSCNR Website has not been Updated.\nLast Notice - \n{}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), req_result[1]
        )
        logging.info("[*] SSCNR Website has not been Updated.")
        with open("bot/plugins/check.txt", "w+") as f:
            f.write(mes2)
            f.close()
    elif req_result[0] == 403:
        sendtelegram(2, AUTH_CHANNEL, "_", "<code>Request Timed Out,sscnr server down or too busy...</code>")
        mes2 = "[{}]: SSCNR Website has not been Updated.".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif req_result[0] == 200:
        mes2 = "[{}]: SSCNR Website has not been Updated.\nLast Notice - \n{}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), req_result[1]
        )
        t1 = threading.Thread(target=broadcast, args=(req_result,))
        t1.start()
    with open("bot/plugins/check.txt", "w+") as f:
        f.write(mes2)
        f.close()
    try:
        looped = threading.Timer(
            int(REQUEST_INTERVAL), lambda: get_mod(Client))
        looped.daemon = True
        looped.start()
    except Exception as e:
        logging.critical(e)
        sendtelegram(2, AUTH_CHANNEL, "_", e)
    return mes2


def getDocId(notice):
    try:
        print("getting doc id for - " + notice)
        token = TG_BOT_TOKEN
        
        r = requests.get(
            "https://api.telegram.org/bot{}/sendDocument".format(token),
            params={
                "chat_id": AUTH_CHANNEL,
                "document": notice,
                "caption": "[Logs]<code> New Notice from official website of sscnr.</code>",
                "parse_mode": "html",
            },
        )
        if r.status_code == 200 and r.json()["ok"]:
            doc_file_id = r.json()["result"]["document"]["file_id"]
            return doc_file_id
        else:
            logging.error(str(r.json()))
            raise Exception
    except Exception as e:
        logging.error(e)
        logging.info(
            "[*] [{}]: Error Sending Logs File!!. - {}".format(datetime.now(), e))
        doc_file_id = 0
        sendtelegram(2, AUTH_CHANNEL, "_", e)
        sys.exit()
        return doc_file_id


def sendtelegram(tipe, user_id, notice, caption):
    if tipe == 1:
        handler = "Document"
        html = "html"
        pramas = {"chat_id": user_id, "document": notice, "caption": caption, "parse_mode": html}
    elif tipe == 2:
        handler = "Message"
        pramas = {
            "chat_id": user_id,
            "text": caption,
            "parse_mode": "html",
        }
    elif tipe == 3:
        handler = "Animation"
        pramas = {"chat_id": user_id, "animation": notice, "caption": caption, "parse_mode": "html"}
    try:
        token = TG_BOT_TOKEN
        r = requests.get(
            "https://api.telegram.org/bot{}/send{}".format(token, handler),
            params=pramas,
        )
        logging.info(r.status_code)
        if r.status_code == 200 and r.json()["ok"]:
            return 200
        elif r.status_code == 403:
            logging.info(
                "[*] Alert was not sent to {} due to being blocked. ".format(user_id))
            return 403
        else:
            logging.info(
                "[*] Alert was not sent to {}. Request - {} ".format(user_id, r.json()))
            raise Exception
    except Exception as e:
        logging.error(e)
        logging.info("[*] Could not send telegram message.")
        return 69


def check_status(user_id, usname):
    print("Checking status")
    sendtelegram(
        2,
        user_id,
        "_",
        "Sending an alert in 5 seconds!\nPlease minimize the app if you want to check notification settings.",
    )
    req_result = request_time(Client)
    time.sleep(4)
    sendtelegram(
        2,
        user_id,
        "_",
        "Last Check- [{}]\n<b>Last Notice:</b> <code>{}</code>\n{}".format(
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"), req_result[1], req_result[2]
        ),
    )
    logging.info("[*] {} requested for a status update!".format(usname))


def broadcast(req_result):
    os.remove("bot/hf/recorded_status.json")
    file_id = getDocId(req_result[2])
    broadcast_list = user_list()
    total = len(broadcast_list)
    failed = 0
    failed_users = []
    for i in range(0, (total)):
        try:
            pp = "[{}]:<b>Latest update from SSCNR website</b><code>{}</code>\n{}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                req_result[1],
                req_result[2],
            )
            send_status = sendtelegram(1, MY_CHANNEL, file_id, pp)
            if send_status == 200:
                i += 1
                logging.info(
                    "[*] Alert Sent to {}/{} people.".format(i, total))
                time.sleep(0.3)
            elif send_status == 403:
                failed += 1
                i += 1
                failed_users.append(broadcast_list[i])
                time.sleep(0.18)
            else:
                continue
        except Exception as e:
            logging.error("[*] {}".format(e))

    time.sleep(4)
    done = "[*] <code>Notice Alert Sent to {}/{} people.\n {} user(s) were not sent the message.</code>".format(
        (int(total - failed)), total, failed
    )
    logging.critical(done)
    sendtelegram(
        3, AUTH_CHANNEL, "https://telegra.ph/file/89f8d77a42135acd60f48.mp4", done
    )
