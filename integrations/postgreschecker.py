from app import create_app, db
from app.models import Events
from prettytable import from_db_cursor
from datetime import datetime, timedelta

class Postgreschecker(object):

	def __init__(self):

			self.app = create_app()

	def ioc_checker(self, all_iocs, connection, caseid):
		# SQL query string declarations
		# If you do not want a query executed for a given indicator type, leave it as an empty string
		sql_str_matching = {
			"name": "SELECT * FROM table WHERE LOWER(name) IN ({}) AND event_time > timestamp - interval '1' hour",
			"username": "",
			"userid": "",
			"email": "",
			"phone": "",
			"ip": "",
			"domain": "",
			"url": "",
			"btcaddress": "",
			"sha256": "",
			"sha1": "",
			"md5": "",
			"filename": "",
			"keyword": "",
		}

		if not connection:
			self.app.logger.error('No Postgres Connection. Exiting.')
			return('')

		result_slack_message = ''
		for i in all_iocs:
			sql_str = ''

			if i in sql_str_matching:
				sql_str = sql_str_matching[i]

			if sql_str:
				# Format iocs so we can just do one SQL "IN" query instead of doing individual queries
				iocs = ''.join("'{}', ".format(str(ioc.indicator)) for ioc in all_iocs[i])
				iocs = iocs.lower()
				iocs = iocs[:-2]

				if iocs:
					try:
						# first do a cursor fetchall so see if there are results
						cursor = connection.cursor()
						sql_str = sql_str.format(iocs)
						cursor.execute(sql_str)
						pg_ioc_results = cursor.fetchall()

						if pg_ioc_results:
							# Add event to Events table
							ioc_data = Events(datetime.now(), i, str(pg_ioc_results), 'Postgres', caseid)
							db.session.add(ioc_data)
							db.session.commit()

							# if there are results, prettytable the output
							cursor_pt = connection.cursor()
							cursor_pt.execute(sql_str)

							data = from_db_cursor(cursor_pt)
							result_slack_message += data.get_string()
					except Exception as e:
						self.app.logger.error("Exeception occured:{}".format(e))

		return(result_slack_message)