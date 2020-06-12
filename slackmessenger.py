import requests
import json
import sys
import os

from app.models import SlackWebhook
from app import create_app

class Slackmessenger(object):

    def __init__(self):

        self.app = create_app()
        with self.app.app_context():
            self.webhook_url = self.app.config['CONFIG']["webhook_url"]

    def main(self, message, caseid):
        webhook_url = self.getwebhook(caseid)
        data = {
            'text': '{}'.format(message)
        }
        self.posttoslack(data, webhook_url)

    def casecreated(self, casename, owner, caseid):
        webhook_url = self.getwebhook(caseid)
        data = {
            'text': 'Case created: {}, Owner: {}'.format(casename, owner)
        }
        self.posttoslack(data, webhook_url)

    def accountcreated(self, accountname, accountemail):
        data = {
            'text': 'Account created for: {}, {}'.format(accountname, accountemail)
        }
        self.posttoslack(data, self.webhook_url)

    def getwebhook(self, caseid):
        webhook_url = ''
        webhook_url_pg = SlackWebhook.query.filter_by(caseid=caseid).first()
        
        if webhook_url_pg:
            webhook_url = webhook_url_pg.slackwebhook
        else:
            webhook_url = self.webhook_url
        return webhook_url

    def insidermessenger(self, message):
        data = {
            'text': '{}'.format(message)
        }
        if self.webhook_url:
            response = requests.post(self.webhook_url, data=json.dumps(
                data), headers={'Content-Type': 'application/json'})

    def posttoslack(self, data, webhook_url):
        if not webhook_url:
            self.app.logger.error('No Slack Webhook provided!')
            return

        response = requests.post(webhook_url, data=json.dumps(
            data), headers={'Content-Type': 'application/json'})