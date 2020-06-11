import calendar

from polyswarm_api.api import PolyswarmAPI
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Events

class PolySwarmchecker(object):

    def __init__(self):

        self.app = create_app()
        with self.app.app_context():
            self.poly_api_key = self.app.config['CONFIG']["poly_api_key"]

        self.one_hour_ago = datetime.utcnow() - timedelta(hours = 1)
        self.one_hour_ago_epoch = calendar.timegm(self.one_hour_ago.timetuple())

    def ioc_checker(self, all_iocs, caseid):
        message = ''
        api = PolyswarmAPI(key=self.poly_api_key)
        poly_checklist = ['sha256', 'sha1', 'md5', 'keyword']

        for i in all_iocs:
            if i in poly_checklist:
                for ioc_data in all_iocs[i]:
                    events = ''
                    meta_results = ''
                    ioc = ioc_data.indicator

                    try:
                        meta_results += api.search_by_metadata(ioc)
                    except Exception as e:
                        self.app.logger.error("Polyswarm exeception occured: {}".format(e))

                    if meta_results:
                        for meta_result in meta_results:
                            results = api.search(meta_result.sha256)
                            if results:
                                for result in results:
                                    last_seen = calendar.timegm(result.last_seen.timetuple())
                                    if (last_seen >= self.one_hour_ago_epoch):
                                        message += '\nPolySwarm hit for IOC: {}\n'.format(ioc)
                                        event = 'PolyScore: {}\nsha256: {}\nsha1: {}\nmd5: {}\nFirst Seen: {}\nLast Seen: {}\nPermalink: {}\n'.format(
                                            result.polyscore, 
                                            result.sha256,
                                            result.sha1,
                                            result.md5,
                                            result.first_seen,
                                            result.last_seen,
                                            result.permalink
                                        )
                                        message += event
                                        events += event

                                        # Add event to Events table
                                        ioc_data = Events(datetime.now(), ioc, events, 'PolySwarm', caseid)
                                        db.session.add(ioc_data)
                                        db.session.commit()
        return(message)