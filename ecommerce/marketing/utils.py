import requests
import json
import hashlib
import re
from django.conf import settings


MAILCHIMP_API_KEY = getattr(settings,"MAILCHIMP_API_KEY",None)
MAILCHIMP_DATA_CENTER = getattr(settings,"MAILCHIMP_DATA_CENTER",None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings,"MAILCHIMP_EMAIL_LIST_ID",None)

def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email

def get_subscriber_hash(member_email):
    # check email
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()

class MailChimp(object):
    def __init__(self):
        super(MailChimp,self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(
                        dc = MAILCHIMP_DATA_CENTER
                        )
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
                            api_url = self.api_url,
                            list_id=self.list_id
                            )
    def get_members_endpoint(self):
        return self.list_endpoint+"/members"

    def change_subscription_status(self, email, status='unsubscribed'):
        # endpoint
        #method
        #data
        #auth
        hashed_email = get_subscriber_hash(email)


        endpoint = self.get_members_endpoint()+"/"+hashed_email
        data = {
            "status": self.check_valid_status(status),
        }

        r = requests.put(endpoint,auth=("",self.key),data = json.dumps(data))

        return r.status_code, r.json()

    def check_subscription_status(self, email):
        # endpoint
        #method
        #data
        #auth
        hashed_email = get_subscriber_hash(email)

        endpoint = self.get_members_endpoint()+"/"+hashed_email
        r = requests.get(endpoint,auth=("",self.key))

        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ['subscribed','unsubscribed','cleaned','pending']
        if status not in choices:
            raise ValueError("Not a valid choice for email status")
        return status

    def add_email(self, email):
        # endpoint
        #method
        #data
        #auth
        status = "subscribed"
        self.check_valid_status(status)
        data = {
            "email_address" : email,
            "status" : status,
        }
        endpoint = self.get_members_endpoint()
        r = requests.post(endpoint,auth=("",self.key), data = json.dumps(data))
        return r.status_code, r.json()

    def unsubscribed(self,email):
        return self.change_subscription_status(email)
    def subscribed(self,email):
        return self.change_subscription_status(email,status="subscribed")
    def pending(self,email):
        return self.change_subscription_status(email,status="pending")
