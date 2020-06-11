# Hound - Indicator Monitoring

<div align="center"><img src="app/static/img/hound.png" /></div>

## What is Hound?
**Hound** is an IOC monitoring tool. Hound allows users to monitor and alert on Indicators against intelligence service such as **VirusTotal**, **PolySwarm**, **Crowdstrike**, and **Flashpoint**
Easily integrate Hound with your user data for monitoring bad actors on your platform.

## How does Hound work?
Every hour IOCs will be check against datasources for any new activity, and every 24 hours using Google CSE. If new activity is seen in the past hour, a dedicated Slack channel can be notified with details surrounding the IOC and the activity. To use Slack, add your Slack Webhook to `config/config.json`.
Don't use Slack? No sweat. Hound will ingest any new activity it sees and store the details within a given Case.

<div align="center"><img src="app/static/screenshots/houndoverview.png" width="50%" height="50%" /></div>

## Integrations
### Current integrations and capabilities
Currently Hound supports **VirusTotal**, **PolySwarm**, **Crowdstrike**, **Flashpoint**, and is ready to be integrated with any **Postgres** data source and **Goolge CSE**.

|   | Postgres (1hr)| VirusTotal (1hr) | PolySwarm (1hr) | CrowdStrike (1hr) | Flashpoint (1hr) | Google CSE (24hr)|
| ------------- | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  |
| **Name** |  |  |  | ✔ | ✔ |  |
| **Username** | ✔ |  |  | ✔ | ✔ |  |
| **UserID** | ✔ |  |  |  |  |  |
| **Email** | ✔ |  |  | ✔ | ✔ |  |
| **Phone** | ✔ |  |  | ✔ | ✔ |  |
| **IPAddress** | ✔ |  |  | ✔ | ✔ |  |
| **AnonymousID** | ✔ |  |  |  |  |  |
| **Domain** |  |  |  | ✔ | ✔ |  |
| **URL** |  |  |  | ✔ | ✔ |  |
| **BTC Address** |  |  |  | ✔ | ✔ |  |
| **sha256** |  | ✔ | ✔ | ✔ | ✔ |  |
| **sha1** |  | ✔ | ✔ | ✔ | ✔ |  |
| **md5** |  | ✔ | ✔ | ✔ | ✔ |  |
| **Filename** |  | ✔ |  | ✔ | ✔ |  |
| **Keyword** |  | ✔ | ✔ | ✔ | ✔ | ✔ |

## Running Hound

1. First setup your `config/config.json` file with all the required usernames and passwords.
2. From the command line: `$ docker-compose up --build`
3. Navigate to [http://localhost:8080/](http://localhost:8080/)
4. Follow the steps below in **Authentication and User Management** to get the Admin and Users set up.

## Authentication and User Management
Users are managed by an Admin account whos credentials are declared in `config/config.json`. To activate the Admin account, navigate to `http://localhost:8080/auth/createadmin`. From there new users can be managed by the Admin at `http://localhost:8080/auth/users`

## Future Integrations
There are two options when adding a new integrations;
1. give the end user an option to run IOCs in your new Integration
2. no case-level integration option and have IOCs run against the new Integration without end user input.

### No Case-Level Integration Checkbox
By not having the case-level option, getting set up is pretty easy. All IOCs can be delivered to a new integration script as a Python Dictionary from `runner.py`, as shown below. You have two interval options in runner, run an integration every 1 hour, or every 24 hours.

```
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
.
.
.
if currentcase.flashpoint == 1:
	fp_results = Flashpointchecker().ioc_checker(all_iocs, case.id)
	if fp_results:
		message += fp_results
```

To access each IOC from the Dictionary:
```
for i in all_iocs:
    for ioc_data in all_iocs[i]:
        ioc = ioc_data.indicator
        print(ioc)
```

Please see `integrations/flashpointchecker.py` for a working example on how each IOC is accessed.

### Case-Level Integration Checkbox
If you decide the end user should have the option to run their IOCs against your new integration, there are a couple more steps involved in addition to the above steps.

1. You'll need to add a column in the Cases table in `app/models.py` for your new integration. e.g. `flashpoint = db.Column(db.Integer)`.
2. In `config.py`, uncomment the local DB URI, and comment out the Production DB URI. It should look like this:
```
# Use this DB for upgrading/downgrading locally:
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

# Use this DB for Prod
# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(
#   CONFIG['POSTGRES_USER'],
#   CONFIG['POSTGRES_PASSWORD'],
#   CONFIG['POSTGRES_HOST'],
#   CONFIG['POSTGRES_DB'])
```
3. Now let's upgrade the Database to reflect this change. In your terminal:
```
$ flask db migrate -m "adding new integration!"
$ flask db upgrade
```
4. You'll need to prepopulate the form for the user when they go to edit a case. This is accomplished in `app/main/routes.py` in the `edit` Definition, e.g. `form.flashpoint.data=case.flashpoint`

That's it! Revert your changes in `config.py` to use the Production DB URI, and you're all set.

## Screenshots
### All Cases
<div align="center"><img src="app/static/screenshots/allcases.png" width="50%" height="50%" /></div>

### Case View
<div align="center"><img src="app/static/screenshots/caseview.png" width="50%" height="50%" /></div>

### Ingested Events
<div align="center"><img src="app/static/screenshots/events.png" width="50%" height="50%" /></div>

### Admin View
<div align="center"><img src="app/static/screenshots/users.png" width="50%" height="50%" /></div>