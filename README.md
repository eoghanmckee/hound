# Hound - Indicator Monitoring

<div align="center"><img src="app/static/img/hound.png" /></div>

## What is Hound?
**Hound** is an IOC monitoring tool. Hound allows users to monitor and alert on Indicators against intelligence service such as **Crowdstrike** and **Flashpoint**.
Easily integrate Hound with your user data for monitoring bad actors on your platform.

![All Cases](./app/static/screenshots/allcases.png)

![Case View](./app/static/screenshots/caseview.png)

## How does Hound work?
Every hour IOCs will be check against datasources for any new activity. If new activity is seen in the past hour, a dedicated Slack channel can be notified with details surrounding the IOC and the activity. To use Slack, add your Slack Webhook to `config.json`.
Don't use Slack? No sweat. Hound will ingest any new activity it sees and store the details within a given Case. 

![Events Table](./app/static/screenshots/events.png)

## Integrations
Currently Hound supports **Crowdstrike** and **Flashpoint**, and is ready to be integrated with any Postgres data source.
To integrate other data sources, check out `runner.py` where all IOCs can be delivered to a new integration script as a Python Dictionary:

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
```

To access each IOC from the Dictionary:
```
for i in all_iocs:
    for ioc_data in all_iocs[i]:
        ioc = ioc_data.indicator
        print(ioc)
```

Please see `integrations/flashpointchecker.py` for a working example on how each IOC is accessed.

## Running Hound

1. First setup your `config.json` file with all the required usernames and passwords.
2. From the command line: `$ docker-compose up --build`
3. Navigate to [http://localhost:8080/](http://localhost:8080/)

## Authentication and User Management
Users are managed by an Admin account whos credentials are declared in `config.json`. To activate the Admin account, navigate to `http://localhost:8080/auth/createadmin`. From there new users can be managed by the Admin at `http://localhost:8080/auth/users`

![Users](./app/static/screenshots/users.png)