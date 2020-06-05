import requests
import json
import calendar

from app import create_app, db
from datetime import datetime, timedelta
from app.models import Events

class VirusTotalchecker(object):

    def __init__(self):

        self.app = create_app()
        with self.app.app_context():
            self.vt_api_key = self.app.config['CONFIG']["vt_api_key"]
        self.vt_endpoint = 'https://www.virustotal.com/api/v3/intelligence/search?query={}'
        self.vt_gui_endpoint = 'https://www.virustotal.com/gui/file/{}'
        self.one_hour_ago = datetime.utcnow() - timedelta(hours = 1)
        self.one_hour_ago_epoch = calendar.timegm(self.one_hour_ago.timetuple())
        self.two_hour_ago = datetime.utcnow() - timedelta(hours = 2)
        self.two_hour_ago_epoch = calendar.timegm(self.two_hour_ago.timetuple())

    def ioc_checker(self, all_iocs, caseid):

        if not self.vt_api_key:
            self.app.logger.error('No Virustotal API Key. Exiting.')
            return

        vt_checklist = {
            "sha256": True,
            "sha1": True,
            "md5": True,
            "filename": True,
            "keyword": True,
        }

        message = ''
        headers = {'x-apikey': '{}'.format(self.vt_api_key)}

        for i in all_iocs:
            if i in vt_checklist:
                for ioc_data in all_iocs[i]:
                    ioc = ioc_data.indicator
                    full_vt_endpoint = self.vt_endpoint.format(ioc)
                    response = requests.get(full_vt_endpoint, headers=headers)
                    status_code = response.status_code

                    if status_code != 200:
                        self.app.logger.error('Encountered Error: {}'.format(status_code))

                    if status_code == 200:
                        response_json = response.json()
                        result_count = len(response_json["data"])
                        if result_count != 0:
                            events = ''
                            for x in range(result_count):
                                first_submission = response_json['data'][x]['attributes']['first_submission_date']
                                last_modification_date = response_json['data'][x]['attributes']['last_modification_date']
                                if (first_submission >= self.two_hour_ago_epoch or last_modification_date >= self.one_hour_ago_epoch):
                                    meaningful_name = response_json['data'][x]['attributes']['meaningful_name']
                                    type_description = response_json['data'][x]['attributes']['type_description']
                                    sha256 = response_json['data'][x]['attributes']['sha256']
                                    link = self.vt_gui_endpoint.format(sha256)
                                    message += '\nVirustotal hit for IOC: {}\n'.format(ioc)
                                    event = 'Name: {}\nSubmission Date: {}\nLast Modification: {}\nType: {}\nLink: {}\n'.format(
                                        meaningful_name,
                                        datetime.fromtimestamp(first_submission),
                                        datetime.fromtimestamp(last_modification_date),
                                        type_description,
                                        link
                                    )
                                    message += event
                                    events += event

                                # Add event to Events table
                                ioc_data = Events(datetime.now(), ioc, events, 'Virustotal', caseid)
                                db.session.add(ioc_data)
                                db.session.commit()
        return(message)