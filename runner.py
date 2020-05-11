import psycopg2

from config import Config
from app import create_app
from slackmessenger import Slackmessenger
from integrations.postgreschecker import Postgreschecker
from integrations.postgreschecker import Postgreschecker
from integrations.flashpointchecker import Flashpointchecker
from integrations.crowdstrikechecker import Crowdstrikechecker
from app.models import Cases, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, Sha256, Sha1, Md5, \
    Filenames, Keywords

class Runner(object):

	def __init__(self):
		self.app = create_app()

	def iocanalysis(self, config_class=Config):

		with self.app.app_context():
			self.app.logger.info('Checking IOCs...')
			cases = Cases.query.all()

			if not cases:
				return

			bearer_token = ''
			user_ro_connection = ''

			if not self.app.config['CONFIG']['postgres_host']:
				self.app.logger.warning('No Postgres Credentials.')

			# initialize postgres connections
			if self.app.config['CONFIG']['postgres_host']:
				user_ro_connection = psycopg2.connect(host = self.app.config['CONFIG']['postgres_host'],
					                                          database = self.app.config['CONFIG']['postgres_dbname'],
					                                          port = self.app.config['CONFIG']['postgres_port'],
					                                          user = self.app.config['CONFIG']['postgres_user'],
					                                          password = self.app.config['CONFIG']['postgres_pass'])

			for case in cases:
				message = ''
				currentcase = Cases.query.filter_by(id=case.id).one()

				# Get crowdstrike token if not already retrieved
				if currentcase.crowdstrike == 1:
					if not bearer_token:
						bearer_token = Crowdstrikechecker().crwd_token_generator()
				if currentcase.status == 1:

					# gather iocs
					names = Names.query.filter_by(caseid=case.id).all()
					usernames = Usernames.query.filter_by(caseid=case.id).all()
					userids = UserIDs.query.filter_by(caseid=case.id).all()
					emails = Emails.query.filter_by(caseid=case.id).all()
					phones = Phones.query.filter_by(caseid=case.id).all()
					ips = IPaddresses.query.filter_by(caseid=case.id).all()
					keywords = Keywords.query.filter_by(caseid=case.id).all()
					domains = Domains.query.filter_by(caseid=case.id).all()
					urls = Urls.query.filter_by(caseid=case.id).all()
					btcaddresses = BTCAddresses.query.filter_by(caseid=case.id).all()
					sha256s = Sha256.query.filter_by(caseid=case.id).all()
					sha1s = Sha1.query.filter_by(caseid=case.id).all()
					md5s = Md5.query.filter_by(caseid=case.id).all()
					filenames = Filenames.query.filter_by(caseid=case.id).all()

					all_iocs = {
						"name": names,
						"username": usernames,
						"userid": userids,
						"email": emails,
						"phone": phones,
						"ip": ips,
						"keyword": keywords,
						"domain": domains,
						"url": urls,
						"btcaddress": btcaddresses,
						"sha256": sha256s,
						"sha1": sha1s,
						"md5": md5s,
						"filename": filenames
					}

					# Run IOCs in Crowdstrike
					if currentcase.crowdstrike == 1 and bearer_token:
						crwd_results = Crowdstrikechecker().ioc_checker(bearer_token, all_iocs, case.id)

						if crwd_results:
								message += crwd_results

					# Run IOCs in Flashpoint
					if currentcase.flashpoint == 1:
						fp_results = Flashpointchecker().ioc_checker(all_iocs, case.id)

						if fp_results:
							message += fp_results

					# Run IOCs in Postgres
					if currentcase.postgres == 1:
						pg_results = Postgreschecker2().ioc_checker(all_iocs, user_ro_connection, case.id)

						if pg_results:
							message += pg_results

					# If there is IOC activity, send a message to slack
					if message:
						self.app.logger.info('IOC activity found for case "{}", alerting Slack channel.'.format(case.casename))
						case_link = self.app.config['CASE_BASEURL']+'{}'.format(case.id)
						final_message = 'New IOC activity for case "{}":```{}```\n<{}|View Case>'.format(case.casename, message, case_link)
						Slackmessenger().main(final_message, case.id)									

			self.app.logger.info('Finished checking IOCs.')

			if user_ro_connection:
				user_ro_connection.close()

if __name__ == "__main__":
    runner = Runner()