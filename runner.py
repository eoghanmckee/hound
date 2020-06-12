import psycopg2

from config import Config
from app import create_app
from slackmessenger import Slackmessenger
from integrations.postgreschecker import Postgreschecker
from integrations.flashpointchecker import Flashpointchecker
from integrations.crowdstrikechecker import Crowdstrikechecker
from integrations.virustotalchecker import VirusTotalchecker
from integrations.polyswarmchecker import PolySwarmchecker
from integrations.osintgoogle import OSINTGoogle
from app.models import Cases, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, Sha256, Sha1, Md5, \
    Filenames, Keywords

class Runner(object):

	def __init__(self):
		self.app = create_app()

	def iocanalysis(self, interval, config_class=Config):

		with self.app.app_context():
			self.app.logger.info(interval)
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
				try:
					user_ro_connection = psycopg2.connect(host = self.app.config['CONFIG']['postgres_host'],
						                                          database = self.app.config['CONFIG']['postgres_dbname'],
						                                          port = self.app.config['CONFIG']['postgres_port'],
						                                          user = self.app.config['CONFIG']['postgres_user'],
						                                          password = self.app.config['CONFIG']['postgres_pass'])
					self.app.logger.info('Postgres connection established.')
				except Exception as e:
					self.app.logger.error("Postgres exeception occured: {}".format(e))

			for case in cases:
				message = ''
				currentcase = Cases.query.filter_by(id=case.id).one()

				# Get crowdstrike token if not already retrieved
				if currentcase.crowdstrike == 1:
					if not bearer_token:
						bearer_token = Crowdstrikechecker().crwd_token_generator()
				if currentcase.status == 1:
					self.app.logger.info('Checking CaseID: {}'.format(case.id))

					# gather iocs
					all_iocs = {
						"name": Names.query.filter_by(caseid=case.id).all(),
						"username": Usernames.query.filter_by(caseid=case.id).all(),
						"userid": Emails.query.filter_by(caseid=case.id).all(),
						"email": Emails.query.filter_by(caseid=case.id).all(),
						"phone": Phones.query.filter_by(caseid=case.id).all(),
						"ip": IPaddresses.query.filter_by(caseid=case.id).all(),
						"keyword": Keywords.query.filter_by(caseid=case.id).all(),
						"domain": Domains.query.filter_by(caseid=case.id).all(),
						"url": Urls.query.filter_by(caseid=case.id).all(),
						"btcaddress": BTCAddresses.query.filter_by(caseid=case.id).all(),
						"sha256": Sha256.query.filter_by(caseid=case.id).all(),
						"sha1": Sha1.query.filter_by(caseid=case.id).all(),
						"md5": Md5.query.filter_by(caseid=case.id).all(),
						"filename": Filenames.query.filter_by(caseid=case.id).all()
					}

					if interval == 1:
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
							pg_results = Postgreschecker().ioc_checker(all_iocs, user_ro_connection, case.id)

							if pg_results:
								message += pg_results

						# Run IOCs in Virustotal
						if currentcase.virustotal == 1:
							vt_results = VirusTotalchecker().ioc_checker(all_iocs, case.id)

							if vt_results:
								message += vt_results

						# Run IOCs in PolySwarm
						if currentcase.polyswarm == 1:
							poly_results = PolySwarmchecker().ioc_checker(all_iocs, case.id)

							if poly_results:
								message += poly_results

					if interval == 24:
						# Run IOCs in GoogleCSE
						if currentcase.googlecse == 1:
							osintgoogle_results = OSINTGoogle().ioc_checker(all_iocs, case.id)

							if osintgoogle_results:
								message += osintgoogle_results

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