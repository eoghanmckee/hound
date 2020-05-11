# Hound - Indicator Monitoring

<div align="center"><img src="app/static/img/hound.png" /></div>

## What is Hound?
**Hound** is an IOC monitoring tool. Hound allows users to monitor and alert on Indicators against intelligence service such as Crowdstrike and Flashpoint.
Easily integrate Hound with your user data for monitoring bad actors.

Every hour IOCs will be check against datasources for any new activity. If new activity is seen in the past 1 hour, a dedicated Slack channel will be notified with details surrounding the IOC and the activity.

## Running Hound
First setup your **config.json** file with all the required usernames and passwords.
`docker-compose up --build`
Navigate to [http://localhost:8080/](http://localhost:8080/)