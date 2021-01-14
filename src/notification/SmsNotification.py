
from twilio.rest import Client

class SmsNotification:
    def __init__(self, account_sid, auth_token, auth_phone):
        if account_sid is not None and auth_token is not None :
            self.client = Client(account_sid, auth_token)
        self.auth_phone = auth_phone

    def sendSms(self, body, user_phone):
        self.client.api.account.messages.create(
            to=user_phone,
            from_=self.auth_phone,
            body=body)