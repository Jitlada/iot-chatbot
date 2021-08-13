import requests
from flask import request
from database import Database
from module import Module
from flask_restful import Resource
from datetime import datetime
import urllib3
import json
import threading
import string
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Webhook(Resource):
    onechat_url = "https://chat-api.one.th"
    onechatbot_id = "B0e42aac13b8d547ba303b00f8b225aa2"
    onechat_dev_token = "Bearer A4665996d217651cd9a100f35203b3f6d7f4581c412fa4430a77a6f4851fa74e341b7e45b691a485a88c8f17cf3674e44"

    sendmessage_url = "https://chat-api.one.th/message/api/v1/push_message"
    sendmessage_headers = {"Authorization": onechat_dev_token}

    onechat_url1 = onechat_url + '/message/api/v1/push_quickreply'

    def send_msg(self, one_id, reply_msg):
        TAG = "send_msg:"

        payload = {
            "to": one_id,
            "bot_id": self.onechatbot_id,
            "type": "text",
            "message": reply_msg,
            "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
        }

        print(TAG, "payload=", payload)
        r = requests.post(self.sendmessage_url, json=payload,
                          headers=self.sendmessage_headers, verify=False)
        return r

    # def send_quick_reply(self, one_id, msg, payload):
    def send_quick_reply(self, one_id, received_msg):
        TAG = "send_quick_reply:"
        # "to": "804228822528",
        # "bot_id": "B0e42aac13b8d547ba303b00f8b225aa2",
        # "message": "เลือกบริการ",
        # "quick_reply": [
        #     {
        #         "label": "หลอดไฟ",
        #         "type": "text",
        #         "message": "หลอดไฟ",
        #         "payload": {
        #             "keyword": "Register",
        #             "service": "001"
        #         }
        #     },
        #     {
        #         "label": "จัดการอุปกรณ์",
        #         "type": "text",
        #         "message": "จัดการอุปกรณ์",
        #         "payload": {
        #             "keyword": "Register",
        #             "service": "001"
        #         }
        #     }
        # ]

        if((received_msg != 'จัดการอุปกรณ์') and (received_msg != 'อุปกรณ์ทั้งหมด') and (received_msg != 'เพิ่มอุปกรณ์') and (received_msg != 'ลบอุปกรณ์')):
            # recv_msg = received_msg
            # devices = self.get_device(one_id)
            devices = self.get_devices_user(one_id)
            payload = []
            for item in devices[0]['result']:
                payload.append(
                    {
                        "label": item['device_name'],
                        "type": "text",
                        "message": item['device_name'],
                        "payload": "my_devices"
                    }
                )

            payload.append({
                "label": "จัดการอุปกรณ์",
                "type": "text",
                "message": "จัดการอุปกรณ์",
                "payload": "my_devices"
            })

            req_body = {
                "to": one_id,
                "bot_id": self.onechatbot_id,
                "message": "เลือกบริการ",
                "quick_reply": payload
            }
            print(TAG, "payload=", payload)
            print(TAG, "received_msg=", received_msg)
            r = requests.post(self.onechat_url1, json=req_body,
                              headers=self.sendmessage_headers, verify=False)
            return r

        else:
            if(received_msg == 'อุปกรณ์ทั้งหมด'):
                all_devices = self.get_devices_user(one_id)
                print("all deviceeeeeeeeeeeeeeeeeeeeeeee : " + str(all_devices))
                return_device = all_devices[0]['result']
                print("return_device deviceeeeeeeeeeeeeeeeeeeeeeee : " +
                      str(return_device))
                sendmessage_body = {
                    "to": one_id,
                    "bot_id": self.onechatbot_id,
                    "type": "text",
                    "message": str(return_device),
                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                }
                sendmessage = requests.post(
                    self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                return sendmessage

            elif (received_msg == 'เพิ่มอุปกรณ์'):
                letters = string.ascii_letters
                device_id = ''.join(random.choice(letters) for i in range(10))
                secret_key = ''.join(random.choice(letters) for i in range(30))
                print(
                    device_id + " : device_iddevice_iddevice_iddevice_iddevice_iddevice_iddevice_iddevice_id")
                print(
                    secret_key + " : secret_keysecret_keysecret_keysecret_keysecret_keysecret_keysecret_keysecret_key")
                sendmessage_body = {
                    "to": one_id,
                    "bot_id": self.onechatbot_id,
                    "type": "text",
                    "message": "กรุณาพิมพ์ชื่ออุปกรณ์",
                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                }
                sendmessage = requests.post(
                    self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                return sendmessage

            elif (received_msg == 'ลบอุปกรณ์'):
                devices = self.get_devices_user(one_id)
                payload = []
                for item in devices[0]['result']:
                    payload.append(
                        {
                            "label": item['device_name'],
                            "type": "text",
                            "message": item['device_name'],
                            "payload": "my_devices"
                        }
                    )

                payload.append({
                    "label": "ยกเลิก",
                    "type": "text",
                    "message": "ยกเลิก",
                    "payload": "my_devices"
                })
                req_body = {
                    "to": one_id,
                    "bot_id": self.onechatbot_id,
                    "message": "กรุณาเลือกอุปกรณ์ที่ต้องการลบ",
                    "quick_reply": payload
                }
                print(TAG, "payload=", payload)
                print(TAG, "received_msg=", received_msg)
                r = requests.post(self.onechat_url1, json=req_body,
                                  headers=self.sendmessage_headers, verify=False)
                return r
                # sendmessage_body = {
                #     "to": one_id,
                #     "bot_id": self.onechatbot_id,
                #     "type": "text",
                #     "message": "กรุณาเลือกอุปกรณ์ที่ต้องการลบ",
                #     "custom_notification": "ตอบกลับข้อความคุณครับ"
                # }
                # sendmessage = requests.post(
                #     self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                # return sendmessage

            else:
                payload = [
                    {
                        "label": "อุปกรณ์ทั้งหมด",
                        "type": "text",
                        "message": "อุปกรณ์ทั้งหมด",
                        "payload": "manage_my_device"
                    },
                    {
                        "label": "เพิ่มอุปกรณ์",
                        "type": "text",
                        "message": "เพิ่มอุปกรณ์",
                        "payload": "manage_my_device"
                    },
                    {
                        "label": "ลบอุปกรณ์",
                        "type": "text",
                        "message": "ลบอุปกรณ์",
                        "payload": "manage_my_device"
                    }
                ]
                req_body = {
                    "to": one_id,
                    "bot_id": self.onechatbot_id,
                    "message": "เลือกจัดการอุปกรณ์",
                    "quick_reply": payload
                }
                print(TAG, "payload=", payload)
                print(TAG, "received_msg=", received_msg)
                r = requests.post(self.onechat_url1, json=req_body,
                                  headers=self.sendmessage_headers, verify=False)
                return r

    # def add_new_device(self, email, name, one_id):
    #     TAG = "add_new_user:"
    #     database = Database()
    #     print(TAG, "add user to our system")
    #     sql = """INSERT INTO `users` (`one_email`, `name`, `one_id`) VALUES ('%s', '%s', '%s')""" \
    #           % (email, name, one_id)
    #     insert = database.insertData(sql)
    #     return insert

    def get_onechat_token(self, auth):
        TAG = "get_onechat_token:"
        module = Module()
        onechat_token = auth.split()

        print(TAG, "auth=", auth)

        if(len(onechat_token) < 2):
            return module.wrongAPImsg()
        if(onechat_token[0] != "Bearer"):
            return module.wrongAPImsg()

        return {
            'type': True,
            'message': "success",
            'error_message': None,
            'result': [{'onechat_token': onechat_token[1]}]
        }, 200

    def menu_send(self, one_id, recv_msg):
        TAG = "menu_send:"
        # database = Database()
        # cmd = """SELECT devices.device_name FROM `devices` """
        # covid_res = database.getData(cmd)
        # print(str(covid_res) + "covid_ressssssss")
        # print(type(covid_res) + "covid_res typeeeeeeeeee")

        # devices = self.get_device(one_id)

        # print(type(devices) + "typeeeeeeeeee")

        # print(str(devices) + "devices")
        # print(str(devices[0]['result'][0]['device_name']))

        # received_msg = recv_msg

        # payload = []
        # for item in devices[0]['result']:

        #     # print(str(item) + "item in devicesssssssssssss")
        #     # print(item['device_name'])

        #     # web_vue_url1 = "http://onesmartaccess.ddns.net:8081"
        #     # web_vue_url1 = "http://203.151.164.229:8081"
        #     # msg = "ให้ช่วยอะไรดี"
        #     payload.append(
        #         {
        #             "label": item['device_name'],
        #             "type": "text",
        #             "message": item['device_name'],
        #             "payload": "my_devices"
        #         }
        #     )
        #     # if(self.is_admin(one_id)):
        #     #     payload.append({
        #     #         "label": "Admin",
        #     #         "type": "link",
        #     #                 "url": web_vue_url1,
        #     #                 "sign": "false",
        #     #                 "onechat_token": "true"
        #     #     })

        # payload.append({
        #     "label": "จัดการอุปกรณ์",
        #     "type": "text",
        #     "message": "จัดการอุปกรณ์",
        #     "payload": "my_devices"
        # })

        # res = self.send_quick_reply(one_id, received_msg, payload)

        res = self.send_quick_reply(one_id, recv_msg)
        print(TAG, "res=", res)

    def get_device(self, one_id):
        TAG = "get_device:"
        database = Database()
        cmd = """SELECT devices.device_name FROM `devices` """
        covid_res = database.getData(cmd)
        # WHERE timeattendance.employee_code='%s' AND timeattendance.date=CURRENT_DATE""" %(one_id)
        return covid_res

    def is_admin(self, one_id):
        TAG = "is_admin:"
        dataabaase = Database()
        module = Module()

        if(not self.is_oneid_exist(one_id)):
            return module.userNotFound()

        cmd = """SELECT users.role FROM `users` WHERE users.one_id='%s'""" % (
            one_id)
        res = dataabaase.getData(cmd)

        role = res[0]['result'][0]['role']

        print(TAG, "role=", role)

        if(role is None):
            return False
        elif(role == "admin"):
            return True
        else:
            return False

    def package_forward(self, package, uri):
        TAG = "package_forward:"
        print(TAG, "forward to dev")
        try:
            r = requests.post(uri, json=package, verify=False)
            print(TAG, "forward status=", r.status_code)
        except:
            print(TAG), "no connection found!"

    def is_user_exist(self, one_email):
        TAG = "is_user_exist:"
        cmd = """SELECT users.one_email FROM users WHERE users.one_email='%s' """ % (
            one_email)
        print(TAG, "cmd=", cmd)
        database = Database()
        res = database.getData(cmd)
        print(TAG, "res=", res)
        if(res[0]['len'] > 0):
            return True
        else:
            return False

    def is_oneid_exist(self, one_id):
        TAG = "is_oneid_exist:"
        cmd = """SELECT users.one_id FROM users WHERE users.one_id='%s' """ % (
            one_id)
        database = Database()
        res = database.getData(cmd)
        print(TAG, "res=", res)
        if(res[0]['len'] > 0):
            return True
        else:
            return False

    def add_new_user(self, email, name, one_id):
        TAG = "add_new_user:"
        database = Database()
        print(TAG, "add user to our system")
        sql = """INSERT INTO `users` (`one_email`, `name`, `one_id`) VALUES ('%s', '%s', '%s')""" \
            % (email, name, one_id)
        insert = database.insertData(sql)
        return insert

    def check_permission(self, one_id):
        TAG = "check_permission:"
        database = Database()
        cmd = """SELECT permissions.one_id FROM `permissions` WHERE permissions.one_id='%s' """ % (
            one_id)
        res = database.getData(cmd)
        print(TAG, "res check_permission=", res)
        if(res[0]['len'] > 0):
            return True
        else:
            return False

    def get_devices_user(self, one_id):
        TAG = "get_devices_user:"
        database = Database()
        cmd = """SELECT devices.device_id, devices.device_name,devices.secret_key  FROM `permissions` 
        LEFT JOIN devices ON permissions.device_id=devices.device_id
        WHERE permissions.one_id='%s' """ % (one_id)
        print(TAG, "cmd of get device all" + cmd)
        devices_of_user = database.getData(cmd)
        # WHERE timeattendance.employee_code='%s' AND timeattendance.date=CURRENT_DATE""" %(one_id)
        return devices_of_user

    def get_message(self, key):
        print("this is KEY" + str(key))
        database = Database()
        sql = """SELECT device_name FROM devices"""
        message = database.getData(sql)
        print("message: " + str(message))
        return message

    # def check_action(self, one_id):
    #     TAG = "check_action:"
    #     database = Database()
    #     cmd = """SELECT permissions.one_id FROM `permissions` WHERE permissions.one_id='%s' """ % (
    #         one_id)
    #     res = database.getData(cmd)
    #     print(TAG, "res check_permission=", res)
    #     if(res[0]['len'] > 0):
    #         return True
    #     else:
    #         return False

    def post(self):
        TAG = "Webhook:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, "headers=", request.headers)
        database = Database()
        module = Module()

        print(TAG, "message: 111111111111111111111111111111111111111111111111111111111111")

        # dev_uri = "http://localhost:5008/api/v1/webhook"
        # t = threading.Thread(target=self.package_forward, args=(data, dev_uri))
        # t.start()

        if ('event' in data):
            if(data["event"] == 'greeting'):
                sendmessage_body = {
                    "to": data['source']['one_id'],
                    "bot_id": self.onechatbot_id,
                    "type": "text",
                    "message": "Hello IoT ChatBot Welcome",
                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                }

                print(TAG, "message: 22222222222222222222222222222222222222222222222")
                print(type(sendmessage_body))
                print(str(sendmessage_body) + "Bodyy")
                sendmessage = requests.post(
                    self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                print("debug onechat response :" +
                      json.dumps(sendmessage.json()))
                print(TAG, "message: 33333333333333333333333333333333333333333333333333" +
                      str(sendmessage_body))
                return module.success()

            elif(data["event"] == 'message'):
                # message_db = self.get_message(1)
                one_id = data['source']['one_id']
                # one_id = 804228822528

                recv_msg = data['message']['text']
                print(TAG, "recv_msg=", recv_msg)

                dissplay_name = data['source']['display_name']

                one_email = data['source']['email']
                print(TAG, "one_email=", one_email)
                if(not self.is_user_exist(one_email)):
                    add_user = self.add_new_user(
                        one_email, dissplay_name, one_id)
                    print(TAG, "add=new_user=", add_user)
                    self.send_msg(one_id, "ยินดีให้บริการค่ะ")
                    return module.success()

                # print(TAG, "message: " +
                #       str(message_db[0]['result'][0]['device_name']))

                # "to": "804228822528"
                # "message": message_db[0]['result'][0]['device_name']

                # self.menu_send(one_id, recv_msg)
                # return module.success()
                if(self.check_permission(one_id)):
                    print(TAG, "check permission before send menu")
                    self.menu_send(one_id, recv_msg)
                    return module.success()

            elif(data["event"] == 'add_friend'):
                one_id = data['source']['one_id']
                dissplay_name = data['source']['display_name']
                one_email = data['source']['email']
                if(not self.is_user_exist(one_email)):
                    add_user = self.add_new_user(
                        one_email, dissplay_name, one_id)
                    print(TAG, "add=new_user=", add_user)
                    self.send_msg(one_id, "ขอบคุณที่เพิ่มเพื่อนค่ะ")
                return module.success()

            return module.success()

    # def get(self):
    #     args = request.args
    #     get_device = self.get_device(args)
    #     return get_device

    # def get(self):
    #     # args = request.args
    #     one_id = request.args['one_id']
    #     get_device_all = self.get_devices_user(one_id)
    #     return get_device_all
