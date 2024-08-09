import requests
import json
import random
import re
from config.models import SmsPhoneVerify
import requests
from urllib.parse import urlencode


class oAuth2Client:
    def __init__(self, client_id, client_secret, redirect_uri, authorize_url, token_url, resource_owner_url):
        self.client_secret = client_secret
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.resource_owner_url = resource_owner_url

    def get_authorization_url(self):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
        }

        url = self.authorize_url + "?" + urlencode(payload)

        return url

    def get_access_token(self, auth_code):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post(self.token_url, data=payload)

        return response.json()

    def get_user_details(self, access_token):
        response = requests.get(self.resource_owner_url, headers={'Authorization': f'Bearer {access_token}'})
        return response.json()


def send_sms(user_code, phone_number):
    url = "http://notify.eskiz.uz/api/message/sms/send"
    payload={'mobile_phone': phone_number,
    'message': f"tutors.uzfi.uz satiga ro'yxatdan o'tish uchun tasdiqlash kodi :{user_code}",
    'from': '4546',
    'callback_url': ''}
    files=[

    ]
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjU1MTEzMjUsImlhdCI6MTcyMjkxOTMyNSwicm9sZSI6InVzZXIiLCJzaWduIjoiYTUzYzEzYzhhMzVlYzg1YWEyODAwMDJlZWNkNDZhZDdiMmU3ZmMxZTk0NWFmMjUwYjM3MjJlODQ5NTdkOWE1YiIsInN1YiI6IjI0NTkifQ.9LSG05e5c2fuZauUlpgpcFb87onH7W5adKEteXjQrOY"
    headers = {'Authorization': "Bearer {}".format(token)}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

def generateCode():
    while True:
        code = ''.join(random.choices('^[a-zA-Z0-9]', k=6))
        if re.match('^[a-zA-Z0-9]{6}$', code) and not SmsPhoneVerify.objects.filter(code=code).exists():
            return code

def download_image(url, save_as):
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)