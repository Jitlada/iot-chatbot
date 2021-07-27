import requests
from flask import request
from database import Database
from module import Module
from flask_restful import Resource
from datetime import datetime
import urllib3
import json
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Webhook(Resource):
    onechat_url = "https://chat-api.one.th"
    onechatbot_id = "B0e42aac13b8d547ba303b00f8b225aa2"
    onechat_dev_token = "Bearer Bearer A4665996d217651cd9a100f35203b3f6d7f4581c412fa4430a77a6f4851fa74e341b7e45b691a485a88c8f17cf3674e44"

    sendmessage_url = "https://chat-api.one.th/message/api/v1/push_message"
    sendmessage_headers = {"Authorization": onechat_dev_token}

    # def send_msg(self, one_id, reply_msg):
    #     TAG = "send_msg:"

    #     payload = {
    #         "to": one_id,
    #         "bot_id": self.beaconbot_id,
    #         "type": "text",
    #         "message": reply_msg,
    #         "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
    #     }

    #     print(TAG, "payload=", payload)
    #     r = requests.post(self.sendmessage_url, json=payload,
    #                       headers=self.sendmessage_headers, verify=False)
    #     return r

    def send_quick_reply(self, one_id, msg, payload):
        TAG = "send_quick_reply:"
        req_body = {
            "to": one_id,
            "bot_id": self.onechatbot_id,
            "message": "เลือกบริการ",
            "quick_reply": payload
        }
        print(TAG, "payload=", payload)
        r = requests.post(self.sendmessage_url, json=payload,
                          headers=self.sendmessage_headers, verify=False)
        return r

    # def get_onechat_token(self, auth):
    #     TAG = "get_onechat_token:"
    #     module = Module()
    #     onechat_token = auth.split()

    #     print(TAG, "auth=", auth)

    #     if(len(onechat_token) < 2):
    #         return module.wrongAPImsg()
    #     if(onechat_token[0] != "Bearer"):
    #         return module.wrongAPImsg()

    #     return {
    #         'type': True,
    #         'message': "success",
    #         'error_message': None,
    #         'result': [{'onechat_token': onechat_token[1]}]
    #     }, 200

    def menu_send(self, one_id):
        TAG = "menu_send:"
        web_vue_url1 = "http://onesmartaccess.ddns.net:8081"
        msg = "ให้ช่วยอะไรดี"
        payload = [
            {
                "label": "การเข้าพื้นที่ของคุณ",
                "type": "text",
                        "message": "ดูการเข้างานของฉัน",
                        "payload": "my_rec"
            }
        ]
        if(self.is_admin(one_id)):
            payload.append({
                "label": "Admin",
                "type": "link",
                        "url": web_vue_url1,
                        "sign": "false",
                        "onechat_token": "true"
            })
        res = self.send_quick_reply(one_id, msg, payload)
        print(TAG, "res=", res)

    def get_device(self, one_id):
        TAG = "get_device:"
        database = Database()
        cmd = """SELECT devices.device_name FROM `devices` """
        covid_res = database.getData(cmd)
        # WHERE timeattendance.employee_code='%s' AND timeattendance.date=CURRENT_DATE""" %(one_id)
        return covid_res

    def post(self):
        TAG = "Webhook:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)
        database = Database()
        module = Module()

        dev_uri = "http://localhost:5008/api/v1/webhook"
        t = threading.Thread(target=self.package_forward, args=(data, dev_uri))
        t.start()

        if ('event' in data):
            if(data["event"] == 'message'):
                message_db = self.get_message(1)
                one_id = data['source']['one_id']
                dissplay_name = data['source']['display_name']

                recv_msg = data['message']['text']
                print(TAG, "recv_msg=", recv_msg)

                one_email = data['source']['email']
                if(not self.is_user_exist(one_email)):
                    add_user = self.add_new_user(
                        one_email, dissplay_name, one_id)
                    print(TAG, "add=new_user=", add_user)
                    self.send_msg(one_id, "ยินดีให้บริการค่ะ")
                    return module.success()

                sendmessage_body = {
                    "to": data['source']['one_id'],
                    "bot_id": self.onechatbot_id,
                    "type": "text",
                    "message": message_db[0]['result'][0]['message'],
                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                }
                sendmessage = requests.post(
                    self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                self.menu_send(one_id)
                return module.success()

    def get(self):
        args = request.args
        get_device = self.get_device(args)
        return get_device
