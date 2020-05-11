import requests
import json
import time

from datetime import datetime, timedelta
from app import create_app, db
from app.models import Events

class Crowdstrikechecker(object):

    def __init__(self):

        self.app = create_app()
        with self.app.app_context():
            self.crwd_client_id = self.app.config['CONFIG']["crwd_client_id"]
            self.crwd_client_secret = self.app.config['CONFIG']["crwd_client_secret"]

        self.onehourago = datetime.now() - timedelta(hours = 1)
        self.unix_time_onehourago = self.onehourago.strftime("%s")

        # Crowdstrike search endpoint
        self.search_endpoint = "https://api.crowdstrike.com/intel/combined/indicators/v1?filter=indicator:'{}'%2Blast_updated:>={}"
        self.auth_url = "https://api.crowdstrike.com/oauth2/token"


    def ioc_checker(self, bearer_token, all_iocs, caseid):

        if not bearer_token:
            return

        message = ''
        payload = {}
        headers = {
          'Authorization': 'Bearer {}'.format(bearer_token)
        }

        for i in all_iocs:
            for ioc_data in all_iocs[i]:
                ioc = ioc_data.indicator

                ioc_url = self.search_endpoint.format(ioc, self.unix_time_onehourago)
                response = requests.request("GET", ioc_url, headers=headers, data = payload)
                status_code = response.status_code

                if status_code != 200:
                    self.app.logger.error('Encountered Error: {}'.format(status_code))

                if status_code == 200:
                    response_json = response.json()
                    result_count = len(response_json["resources"])
                    if result_count != 0:
                        events = ''
                        # parse through json response
                        for x in range(result_count):
                            indicator = response_json["resources"][x]["indicator"]                       
                            message += '\nCrowdstrike hit for IOC: {}\n'.format(indicator)
                            label_count = len(response_json["resources"][x]["labels"])

                            for y in range(label_count):
                                label = response_json["resources"][x]["labels"][y]["name"]
                                message += 'Label: {}\n'.format(label)
                                events += '{}, '.format(label)

                        # Add event to Events table
                        ioc_data = Events(datetime.now(), ioc, events, 'Crowdstrike', caseid)
                        db.session.add(ioc_data)
                        db.session.commit()

        return(message)


    def crwd_token_generator(self):
        
        self.app.logger.info('Generating Crowdstrike bearer token...')

        if not self.crwd_client_id:
            self.app.logger.error('No Crowdstrike Credentials. Exiting.')
            return

        headers = {'Content-Type': 'application/x-www-form-urlencoded', "accept": "application/json"}
        data = {'client_id': self.crwd_client_id, 'client_secret': self.crwd_client_secret}

        resp = requests.request("POST", self.auth_url, headers=headers, data=data)

        if resp.ok:
            response = resp.json()
            access_token = response['access_token']
            if access_token:
                self.app.logger.info('Successfully retrieved Crowstrike bearer token ')
                return(access_token)
            if "errors" in response:
                for error in response['errors']:
                    self.app.logger.error("Error Code %d: %s " % (error['code'], error['message']))
        elif resp.status_code == 429:
            self.app.logger.error('Rate Limiting encountered.')
