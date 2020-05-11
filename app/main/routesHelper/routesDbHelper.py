import logging
import urllib.parse

from app import db
from flask import request
from urllib.parse import quote
from app.models import SlackWebhook, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, Sha256, Sha1, Md5, \
    Filenames, Keywords

def insertslackwebhookHelper(slackwebhook, caseid):

    if slackwebhook:
        slackwebhook_data = SlackWebhook(slackwebhook, caseid)
        db.session.add(slackwebhook_data)
        db.session.commit()


def insertformHelper(form, caseid):

    # Insert Names
    names = request.form['names']
    insertiocsHelper(names, caseid, 'Names')

    # Insert Usernames
    usernames = request.form['usernames']
    insertiocsHelper(usernames, caseid, 'Usernames')

    # Insert UserIDs
    userids = request.form['userids']
    insertiocsHelper(userids, caseid, 'UserIDs')

    # Insert Emails
    emails = request.form['emails']
    insertiocsHelper(emails, caseid, 'Emails')

    # Insert Phones
    phones = request.form['phones']
    insertiocsHelper(phones, caseid, 'Phones')

    # Insert IPaddresses
    ipaddresses = request.form['ips']
    insertiocsHelper(ipaddresses, caseid, 'IPaddresses')

    # Insert Domains
    domains = request.form['domains']
    # insertiocsHelper(domains, caseid, 'Domains')
    inserturlsdomainsHelper(domains, caseid, 'Domains')

    # Insert Urls
    urls = request.form['urls']
    inserturlsdomainsHelper(urls, caseid, 'Urls')

    # Insert btcaddresses
    btcaddresses = request.form['btcaddresses']
    insertiocsHelper(btcaddresses, caseid, 'BTCAddresses')

    # Insert sha256
    sha256 = request.form['sha256']
    insertiocsHelper(sha256, caseid, 'Sha256')

    # Insert sha1
    sha1 = request.form['sha1']
    insertiocsHelper(sha1, caseid, 'Sha1')

    # Insert md5
    md5 = request.form['md5']
    insertiocsHelper(md5, caseid, 'Md5')

    # Insert filenames
    filenames = request.form['filenames']
    insertiocsHelper(filenames, caseid, 'Filenames')

    # Insert Keywords
    keywords = request.form['keywords']
    insertiocsHelper(keywords, caseid, 'Keywords')

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

def insertiocsHelper(iocs, caseid, ioctype):

    ioctype = eval(ioctype)

    if iocs:
        iocs_list = iocs.split(',')
        for ioc in iocs_list:
            ioc = ioc.strip()
            ioc_data = ioctype(ioc, caseid)
            db.session.add(ioc_data)
            db.session.commit()

def deleteiocsHelper(id):

    SlackWebhook.query.filter_by(caseid=id).delete()
    Names.query.filter_by(caseid=id).delete()
    Usernames.query.filter_by(caseid=id).delete()
    UserIDs.query.filter_by(caseid=id).delete()
    Emails.query.filter_by(caseid=id).delete()
    Phones.query.filter_by(caseid=id).delete()
    IPaddresses.query.filter_by(caseid=id).delete()
    Domains.query.filter_by(caseid=id).delete()
    Urls.query.filter_by(caseid=id).delete()
    BTCAddresses.query.filter_by(caseid=id).delete()
    Sha256.query.filter_by(caseid=id).delete()
    Sha1.query.filter_by(caseid=id).delete()
    Md5.query.filter_by(caseid=id).delete()
    Filenames.query.filter_by(caseid=id).delete()
    Keywords.query.filter_by(caseid=id).delete()
    db.session.commit()
