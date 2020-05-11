from app import create_app, db
from app.models import Events
from prettytable import from_db_cursor
from datetime import datetime, timedelta

class Postgreschecker(object):

	def __init__(self):

			self.app = create_app()

	def ioc_checker(self, all_iocs, connection, caseid):

		# SQL query string declarations
		# If you do not want a query executed for a given indicator type, leave it as an empty string, e.g. sql_str_name
		sql_str_sample = "SELECT * FROM table WHERE LOWER(username) IN ({}) AND event_time > timestamp - interval '1' hour"
		sql_str_name = ""
		sql_str_username = ""
		sql_str_userid = ""
		sql_str_email_src = ""
		sql_str_phone_number = ""
		sql_str_ip_src = ""
		sql_str_domain = ""
		sql_str_url = ""
		sql_str_btc = ""
		sql_str_sha256 = ""
		sql_str_sha1 = ""
		sql_str_md5 = ""
		sql_str_filenmame = ""
		sql_str_keyword = ""
		
		sql_str_matching = {
			"name": sql_str_name,
			"username": sql_str_username,
			"userid": sql_str_userid,
			"email": sql_str_email_src,
			"phone": sql_str_phone_number,
			"ip": sql_str_ip_src,
			"domain": sql_str_domain,
			"url": sql_str_url,
			"btcaddress": sql_str_btc,
			"sha256": sql_str_sha256,
			"sha1": sql_str_sha1,
			"md5": sql_str_md5,
			"filename": sql_str_filenmame,
			"keyword": sql_str_keyword,
		}

		if not connection:
			self.app.logger.error('No Postgres Connection. Exiting.')
			return

		result_slack_message = ''
		for i in all_iocs:
			sql_str = ''

			if i in sql_str_matching:
				sql_str = sql_str_matching[i]

			if sql_str:
				# Format iocs so we can just do one SQL "IN" query instead of doing individual queries
				iocs = ','.join(str(ioc.indicator) for ioc in all_iocs[i])
				iocs = iocs.lower()

				if iocs:
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

		return(result_slack_message)
