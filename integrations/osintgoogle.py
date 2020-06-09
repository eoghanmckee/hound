import requests
import json
import calendar

from app.models import Events, IOCMatches
from app import create_app, db
from datetime import datetime, timedelta
from googleapiclient.discovery import build

class OSINTGoogle(object):

    def __init__(self):

        self.app = create_app()
        with self.app.app_context():
            self.google_api_key = self.app.config['CONFIG']["google_api_key"]
            self.google_cse_id = self.app.config['CONFIG']["google_cse_id"]

    def ioc_checker(self, all_iocs, caseid):

        if not self.google_api_key:
            self.app.logger.error('No Google API Key. Exiting.')
            return

        google_checklist = {
            "keyword": True,
        }

        message = ''

        for i in all_iocs:
            if i in google_checklist:
                for ioc_data in all_iocs[i]:
                    events = ''
                    ioc = ioc_data.indicator
                    service = build("customsearch", "v1", developerKey=self.google_api_key)
                    response = service.cse().list(q=ioc, cx=self.google_cse_id).execute()
                    totalResults = response['searchInformation']['totalResults']
                    if int(totalResults) != 0:
                        results = response['items']
                        for result in results:
                            link = result['link']
                            iocmatches = IOCMatches.query.filter_by(osintgoogle=link, caseid=caseid).first()
                            if not iocmatches:
                                title = result['title']
                                snippet = result['snippet']
                                message += '\nOSINT hit (via Googs) for IOC: {}\n'.format(ioc)
                                event = 'Title: {}\nLink: {}\nSnippet: {}\n'.format(
                                    title, 
                                    link, 
                                    snippet
                                    )
                                message += event
                                events += event

                                iocmatch = IOCMatches(link, caseid)
                                db.session.add(iocmatch)
                                db.session.commit()

                                # Add event to Events table
                                ioc_data = Events(datetime.now(), ioc, events, 'OSINT(Google)', caseid)
                                db.session.add(ioc_data)
                                db.session.commit()
        return(message)