import urllib.parse
from urllib.parse import unquote, quote

from app import db
from app.main import bp
from datetime import datetime
from slackmessenger import Slackmessenger
from flask_login import current_user, login_required
from app.main.routesHelper.routesDbHelper import insertslackwebhookHelper, insertformHelper, \
    deleteiocsHelper
from app.main.routesHelper.routesSearchHelper import searchHelper
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from app.main.forms import SearchForm, CreateForm, UpdateForm, NotesForm
from app.models import Users, Cases, SlackWebhook, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, Sha256, Sha1, Md5, \
    Filenames, Keywords, Notes, Events


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    cases = Cases.query.all()
    yourcases = \
        Cases.query.filter_by(creator=current_user.username).all() 
    return render_template('index.html', title='Home', cases=cases,
                           yourcases=yourcases)

@bp.route('/allcases')
@login_required
def allcases():
    cases = Cases.query.all()
    return render_template('allcases.html', title='All Cases',
                           cases=cases)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        
        # Insert Cases
        user_id = Users.query.filter_by(username=current_user.username).first()
        casename = request.form['casename']
        creator = current_user.username
        createdate = datetime.today().strftime('%Y-%m-%d')
        status = 1

        flashpoint = ''
        if 'flashpoint' not in request.form:
            flashpoint = 0
        else:
            flashpoint = 1

        crowdstrike = ''
        if 'crowdstrike' not in request.form:
            crowdstrike = 0
        else:
            crowdstrike = 1

        postgres = ''
        if 'postgres' not in request.form:
            postgres = 0
        else:
            postgres = 1

        data = Cases(casename, creator, createdate, status, flashpoint, crowdstrike, postgres, user_id.id)
        db.session.add(data)
        db.session.commit()

        case = Cases.query.filter_by(casename=casename).first()
        caseid = case.id

        # Insert SlackWebhook & Çase Details
        slackwebhook = request.form['slackwebhook']
        insertslackwebhookHelper(slackwebhook, caseid)
        insertformHelper(form, caseid)

        Slackmessenger().casecreated(casename, creator, caseid)

        flash('Case Created - Release the Hounds!')
        return redirect('index')
    return render_template('create.html', title='Create Case',
                           form=form)


@bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    
    case = Cases.query.filter_by(id=id).first()
    flashpoint = case.flashpoint
    crowdstrike = case.crowdstrike
    postgres = case.postgres
    notes = Notes.query.filter_by(caseid=id).all()
    events = Events.query.filter_by(caseid=id).all()

    slackwebhook_string = ''
    slackwebhook = SlackWebhook.query.filter_by(caseid=id).first()

    if slackwebhook:
        slackwebhook_string = str(slackwebhook.slackwebhook)

    # get names

    names_string = ''
    names = Names.query.filter_by(caseid=id).all()
    for name in names:
        names_string += str(name.indicator) + ', '
    names_string = names_string[:-2] # removing the last comma and trailing space

    # get usernames

    usernames_string = ''
    usernames = Usernames.query.filter_by(caseid=id).all()
    for username in usernames:
        usernames_string += str(username.indicator) + ', '
    usernames_string = usernames_string[:-2]

    # get userids

    userids_string = ''
    userids = UserIDs.query.filter_by(caseid=id).all()
    for userid in userids:
        userids_string += str(userid.indicator) + ', '
    userids_string = userids_string[:-2]

    # get emails

    emails_string = ''
    emails = Emails.query.filter_by(caseid=id).all()
    for email in emails:
        emails_string += str(email.indicator) + ', '
    emails_string = emails_string[:-2]

    # get phones

    phones_string = ''
    phones = Phones.query.filter_by(caseid=id).all()
    for phone in phones:
        phones_string += str(phone.indicator) + ', '
    phones_string = phones_string[:-2]

    # get ips

    ips_string = ''
    ips = IPaddresses.query.filter_by(caseid=id).all()
    for ip in ips:
        ips_string += str(ip.indicator) + ', '
    ips_string = ips_string[:-2]

    # get domains

    domains_string = ''
    domains = Domains.query.filter_by(caseid=id).all()
    for domain in domains:
        domains_string += unquote(domain.indicator) + ', '
    domains_string = domains_string[:-2]

    # get urls

    urls_string = ''
    urls = Urls.query.filter_by(caseid=id).all()
    for url in urls:
        urls_string += unquote(url.indicator) + ', '
    urls_string = urls_string[:-2]

    # get btcaddresses

    btcaddresses_string = ''
    btcaddresses = BTCAddresses.query.filter_by(caseid=id).all()
    for btcaddress in btcaddresses:
        btcaddresses_string += str(btcaddress.indicator) + ', '
    btcaddresses_string = btcaddresses_string[:-2]

    # get sha256

    sha256s_string = ''
    sha256s = Sha256.query.filter_by(caseid=id).all()
    for sha256 in sha256s:
        sha256s_string += str(sha256.indicator) + ', '
    sha256s_string = sha256s_string[:-2]

    # get sha1

    sha1s_string = ''
    sha1s = Sha1.query.filter_by(caseid=id).all()
    for sha1 in sha1s:
        sha1s_string += str(sha1.indicator) + ', '
    sha1s_string = sha1s_string[:-2]

    # get md5

    md5s_string = ''
    md5s = Md5.query.filter_by(caseid=id).all()
    for md5 in md5s:
        md5s_string += str(md5.indicator) + ', '
    md5s_string = md5s_string[:-2]

    # get filenames

    filenames_string = ''
    filenames = Filenames.query.filter_by(caseid=id).all()
    for filename in filenames:
        filenames_string += str(filename.indicator) + ', '
    filenames_string = filenames_string[:-2]

    # get keywords

    keywords_string = ''
    keywords = Keywords.query.filter_by(caseid=id).all()
    for keyword in keywords:
        keywords_string += str(keyword.indicator) + ', '
    keywords_string = keywords_string[:-2]

    # Get form data

    form = UpdateForm()
    notesform = NotesForm()

    # load page content if GET request

    if request.method == 'GET':
    
        # prepopulate the form with existing iocs
        form.slackwebhook.data=slackwebhook_string
        form.names.data=names_string
        form.usernames.data=usernames_string
        form.userids.data=userids_string
        form.emails.data=emails_string
        form.phones.data=phones_string
        form.ips.data=ips_string
        form.domains.data=domains_string
        form.urls.data=urls_string
        form.btcaddresses.data=btcaddresses_string
        form.sha256.data=sha256s_string
        form.sha1.data=sha1s_string
        form.md5.data=md5s_string
        form.filenames.data=filenames_string
        form.keywords.data=keywords_string
        form.flashpoint.data=flashpoint
        form.crowdstrike.data=crowdstrike
        form.postgres.data=postgres


    # if updating IOCs:

    if form.update.data:

        # delete all case iocs prior to updating the case - yep, i know
        deleteiocsHelper(id)

        # Insert Flashpoint
        flashpoint = ''
        if 'flashpoint' not in request.form:
            flashpoint = 0
        else:
            flashpoint = 1

        Cases.query.filter_by(id=id).update(dict(flashpoint=flashpoint))

        # Insert Crowdstrike
        crowdstrike = ''
        if 'crowdstrike' not in request.form:
            crowdstrike = 0
        else:
            crowdstrike = 1

        Cases.query.filter_by(id=id).update(dict(crowdstrike=crowdstrike))

        # Insert Postgres
        postgres = ''
        if 'postgres' not in request.form:
            postgres = 0
        else:
            postgres = 1

        Cases.query.filter_by(id=id).update(dict(postgres=postgres))
        db.session.commit()
        
       # Insert SlackWebhook
        slackwebhook = request.form['slackwebhook']
        insertslackwebhookHelper(slackwebhook, id)

        # Send form data to formHelper
        insertformHelper(form, id)

        flashmessage = \
                'Case "{}" updated'.format(case.casename)
        flash(flashmessage)
        return redirect(url_for('main.index'))

    if notesform.submit.data:
        text = request.form['text']
        author = current_user.username
        createdate = datetime.today().strftime('%Y-%m-%d')

        note = Notes(text, author, createdate, id)
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('main.edit', id=id))

    if form.delete.data:

        # delete iocs
        deleteiocsHelper(id)

        notes = Notes.query.filter_by(caseid=id).delete()
        db.session.commit()

        # get flash message first prior to deleting the case
        flashmessage = \
                'Case "{}" deleted'.format(case.casename)

        Cases.query.filter_by(id=id).delete()
        db.session.commit()

        flash(flashmessage)
        return redirect(url_for('main.index'))

    if form.deactivate.data:
        case = Cases.query.filter_by(id=id).one()
        case.status = 0
        db.session.commit()

        flashmessage = \
                'Case "{}" deactivated'.format(case.casename)

        flash(flashmessage)
        return redirect(url_for('main.index'))

    if form.activate.data:
        case = Cases.query.filter_by(id=id).one()
        case.status = 1
        db.session.commit()

        flashmessage = \
                'Case "{}" activated'.format(case.casename)

        flash(flashmessage)
        return redirect(url_for('main.index'))

    return render_template(
        'edit.html',
        title='Edit Case',
        case=case,
        slackwebhook=slackwebhook_string,
        names_string=names_string,
        usernames_string=usernames_string,
        userids_string=userids_string,
        emails_string=emails_string,
        phones_string=phones_string,
        ips_string=ips_string,
        domains_string=domains_string,
        urls_string=urls_string,
        btcaddresses=btcaddresses,
        sha256s_string=sha256s_string,
        sha1s_string=sha1s_string,
        md5s_string=md5s_string,
        filenames_string=filenames_string,
        keywords_string=keywords_string,
        form=form,
        notesform=notesform,
        notes=notes,
        events=events,
        names=names,
        usernames=usernames,
        userids=userids
        )


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    form = SearchForm()
    search_term = request.form.get("searchterm")

    if not search_term:
        return redirect(url_for('main.index'))

    search_results = searchHelper(form, search_term)

    return render_template(
    'search.html',
    title='Search',
    search_results=search_results,
    search_term=search_term
    )