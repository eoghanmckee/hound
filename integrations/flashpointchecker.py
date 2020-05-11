import requests
import json

from app import create_app, db
from datetime import datetime, timedelta
from app.models import Events

class Flashpointchecker(object):

    def __init__(self):
        
        self.app = create_app()
        with self.app.app_context():
            self.fp_bearer = self.app.config['CONFIG']["fp_bearer"]

        self.fp_endpoint = "https://fp.tools/api/v4/indicators/simple?limit=10&query=\"{}\"&updated_since=1h"


    def ioc_checker(self, all_iocs, caseid):

        if not self.fp_bearer:
            self.app.logger.error('No Flashpoint Credentials. Exiting.')
            return

        message = ''
        headers = {'Authorization': 'Bearer ' + self.fp_bearer}

        for i in all_iocs:
            for ioc_data in all_iocs[i]:
                ioc = ioc_data.indicator

                full_fp_endpoint = self.fp_endpoint.format(ioc)
                response = requests.get(full_fp_endpoint, headers=headers)
                status_code = response.status_code

                if status_code != 200:
                    self.app.logger.error('Encountered Error: {}'.format(status_code))

                response_json = response.json()
                total_hits = len(response_json)

                if status_code == 200:
                    if total_hits != 0:
                        events = ''
                        for i in range(total_hits):
                            attribute_type = response_json[i]["Attribute"]["type"]
                            attribute_info = response_json[i]["Attribute"]["Event"]["info"]
                            attribute_category = response_json[i]["Attribute"]["category"]
                            attribute_value = response_json[i]["Attribute"]["value"]
                            message += 'Flashpoint hit for IOC: {}\n'.format(ioc)

                            event = 'Type: {}\nInfo: {}\nCategory: {}\nValue: {}\n'.format(
                                attribute_type,
                                attribute_info,
                                attribute_category,
                                json.dumps(attribute_value)
                            )
                            message += event
                            message += 'Link: {}\n\n'.format(response_json[i]["Attribute"]["Event"]["href"])

                            events += event

                        # Add event to Events table
                        ioc_data = Events(datetime.now(), ioc, events, 'Flashpoint', caseid)
                        db.session.add(ioc_data)
                        db.session.commit()

        return(message)