import wifi
import socketpool
from adafruit_requests import Session
import ssl
import binascii


class Twilio:
    def __init__(self, account_sid, auth_token, from_number, to_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.to_number = to_number
        self.from_number = from_number
        self.session = None

    def connect_to_network(self, ssid, password):
        wifi.radio.enabled = True
        print("Connecting to Wi-Fi...")
        wifi.radio.connect(ssid, password)
        print("Connected!")
        pool = socketpool.SocketPool(wifi.radio)
        self.session = Session(pool, ssl.create_default_context())

    def send_text(self, message):
        url = "https://api.twilio.com/2010-04-01/Accounts/" + self.account_sid + "/Messages.json"
        authorization = str(binascii.b2a_base64((self.account_sid + ":" + self.auth_token).encode()), "utf-8")[:-1]
        headers = {
            "Authorization": "Basic " + authorization,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = "To=" + self.to_number + '&' + \
               "From=" + self.from_number + '&' + \
               "Body=" + message

        response = self.session.post(url, headers=headers, data=data)
        if response.status_code == 201:
            print("Text sent!")
        else:
            print("Failed to send text. Response:", response.text)