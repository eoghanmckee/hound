import logging
import urllib.parse

from app import db
from flask import request
from urllib.parse import quote
from app.models import SlackWebhook, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, Sha256, Sha1, Md5, \
    Filenames, Keywords, Events, IOCMatches

def insertslackwebhookHelper(slackwebhook, caseid):

    if slackwebhook:
        slackwebhook_data = SlackWebhook(slackwebhook, caseid)
        db.session.add(slackwebhook_data)
        db.session.commit()


def insertformHelper(form, caseid):

    ioc_types = {
        "names": 'Names',
        "usernames": 'Usernames',
        "userids": 'UserIDs',
        "emails": 'Emails',
        "phones": 'Phones',
        "ips": 'IPaddresses',
        "keywords": 'Keywords',
        "btcaddresses": 'BTCAddresses',
        "sha256": 'Sha256',
        "sha1": 'Sha1',
        "md5": 'Md5',
        "filenames": 'Filenames'
    }

    for i in ioc_types:
        indicators = request.form[i]
        ioc_type = eval(ioc_types[i])
        if indicators:
            indicators_list = indicators.split(',')
            for ioc in indicators_list:
                ioc = ioc.strip()
                ioc_data = ioc_type(ioc, caseid)
                db.session.add(ioc_data)
                db.session.commit()

    domains = request.form['domains']
    inserturlsdomainsHelper(domains, caseid, 'Domains')
    urls = request.form['urls']
    inserturlsdomainsHelper(urls, caseid, 'Urls')


# Custom Insertion for Urls & Domains - we must url encode
def inserturlsdomainsHelper(iocs, caseid, ioctype):

    ioctype = eval(ioctype)
    if iocs:
        iocs_list = iocs.split(',')
        for ioc in iocs_list:
            ioc = ioc.strip()
            ioc_decode = urllib.parse.quote(ioc)
            ioc_data = ioctype(ioc_decode, caseid)
            db.session.add(ioc_data)
            db.session.commit()


def deleteiocsHelper(id):

    tables = ['SlackWebhook', 'Names', 'Usernames', 'UserIDs', 'Emails', 'Phones', \
    'IPaddresses', 'Domains', 'Urls', 'BTCAddresses', 'Sha256', 'Sha1', \
    'Md5', 'Filenames', 'Keywords']

    for table in tables:
        table = eval(table)
        table.query.filter_by(caseid=id).delete()
        db.session.commit()