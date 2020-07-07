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
from app.main.forms import SearchForm, CreateForm, NotesForm
from app.models import Users, Cases, SlackWebhook, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, Sha256, Sha1, Md5, \
    Filenames, Keywords, Notes, Events, IOCMatches

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

        integrations_list = []
        for field in form:
            if field.type == "BooleanField":
                integrations_list.append(field.name)
        integrations_tuple = tuple(integrations_list)
        data = {field:int(field in request.form) for field in integrations_tuple}
        data['casename'] = casename
        data['creator'] = creator
        data['createdate'] = datetime.today().strftime('%Y-%m-%d')
        data['status'] = 1
        data['user_id'] = user_id.id
        db.session.add(Cases(**data))
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
    notes = Notes.query.filter_by(caseid=id).all()
    events = Events.query.filter_by(caseid=id).all()

    # Get form data
    form = CreateForm()
    notesform = NotesForm()

    # prepopulate the form if GET request
    if request.method == 'GET':
        form.slackwebhook.data = ''
        slackwebhook = SlackWebhook.query.filter_by(caseid=id).first()

        if slackwebhook:
            form.slackwebhook.data = str(slackwebhook.slackwebhook)

        names_string, usernames_string, userids_string, emails_string, phones_string, \
        ips_string, domains_string, urls_string, btcaddresses_string, sha256s_string, \
        sha1s_string, md5s_string, filenames_string, keywords_string = ('' for i in range(14))

        # get names
        names = Names.query.filter_by(caseid=id).all()
        for name in names:
            names_string += str(name.indicator) + ', '
        form.names.data = names_string[:-2] # removing the last comma and trailing space

        # get usernames
        usernames = Usernames.query.filter_by(caseid=id).all()
        for username in usernames:
            usernames_string += str(username.indicator) + ', '
        form.usernames.data = usernames_string[:-2]

        # get userids
        userids = UserIDs.query.filter_by(caseid=id).all()
        for userid in userids:
            userids_string += str(userid.indicator) + ', '
        form.userids.data = userids_string[:-2]

        # get emails
        emails = Emails.query.filter_by(caseid=id).all()
        for email in emails:
            emails_string += str(email.indicator) + ', '
        form.emails.data = emails_string[:-2]

        # get phones
        phones = Phones.query.filter_by(caseid=id).all()
        for phone in phones:
            phones_string += str(phone.indicator) + ', '
        form.phones.data = phones_string[:-2]

        # get ips
        ips = IPaddresses.query.filter_by(caseid=id).all()
        for ip in ips:
            ips_string += str(ip.indicator) + ', '
        form.ips.data = ips_string[:-2]

        # get domains
        domains = Domains.query.filter_by(caseid=id).all()
        for domain in domains:
            domains_string += unquote(domain.indicator) + ', '
        form.domains.data = domains_string[:-2]

        # get urls
        urls = Urls.query.filter_by(caseid=id).all()
        for url in urls:
            urls_string += unquote(url.indicator) + ', '
        form.urls.data = urls_string[:-2]

        # get btcaddresses
        btcaddresses = BTCAddresses.query.filter_by(caseid=id).all()
        for btcaddress in btcaddresses:
            btcaddresses_string += str(btcaddress.indicator) + ', '
        form.btcaddresses.data = btcaddresses_string[:-2]

        # get sha256
        sha256s = Sha256.query.filter_by(caseid=id).all()
        for sha256 in sha256s:
            sha256s_string += str(sha256.indicator) + ', '
        form.sha256.data = sha256s_string[:-2]

        # get sha1
        sha1s = Sha1.query.filter_by(caseid=id).all()
        for sha1 in sha1s:
            sha1s_string += str(sha1.indicator) + ', '
        form.sha1.data = sha1s_string[:-2]

        # get md5
        md5s = Md5.query.filter_by(caseid=id).all()
        for md5 in md5s:
            md5s_string += str(md5.indicator) + ', '
        form.md5.data = md5s_string[:-2]

        # get filenames
        filenames = Filenames.query.filter_by(caseid=id).all()
        for filename in filenames:
            filenames_string += str(filename.indicator) + ', '
        form.filenames.data = filenames_string[:-2]

        # get keywords
        keywords = Keywords.query.filter_by(caseid=id).all()
        for keyword in keywords:
            keywords_string += str(keyword.indicator) + ', '
        form.keywords.data = keywords_string[:-2]
    
        form.flashpoint.data=case.flashpoint
        form.crowdstrike.data=case.crowdstrike
        form.postgres.data=case.postgres
        form.virustotal.data=case.virustotal
        form.polyswarm.data=case.polyswarm
        form.googlecse.data=case.googlecse     

    # if updating IOCs:
    if form.update.data:

        # Warn if Slack Webhook changed by someone other than the case owner
        existing_slackwebhook = SlackWebhook.query.filter_by(caseid=id).first()
        if existing_slackwebhook is None:
            existing_slackwebhook = ''

        new_slackwebhook = request.form['slackwebhook']
        current_userid = Users.query.filter_by(username=current_user.username).first()
        case_owner = Users.query.filter_by(id=case.user_id).first()

        if new_slackwebhook != existing_slackwebhook and current_userid.id != case.user_id:
           slack_message = 'WARNING: Slack Webhook changed for {}\'s case, \'{}\', by user {}'.format(case_owner.email, case.casename, current_user.email)
           Slackmessenger().insidermessenger(slack_message)

        # # makes update changes without deleting the whole case...
        # # 1. get array/list of current IOCs
        # name_list, username_list, userid_list, email_list, phone_list, \
        # ipaddress_list, domain_list, url_list, btcaddress_list, sha256_list, \
        # sha1_list, md5_list, filename_list, keyword_list = ([] for i in range(14))

        # # get names
        # names = Names.query.filter_by(caseid=id).all()
        # for name in names:
        #     name_list.append(name.indicator)

        # # 2. get array/list of new IOCs
        # name_indicators = request.form['names']
        # name_indicators = name_indicators.split(",")
        # name_indicators = [x.strip(' ') for x in name_indicators]

        # # 3. if new list ioc not in old ioc list, add
        # for i in name_indicators:
        #     if i not in name_list:
        #         new_name = Names(i, id)
        #         db.session.add(new_name)
        #         db.session.commit()

        # # 4. if iocs in old list not in new list, delete
        # for k in name_list:
        #     if k not in name_indicators:
        #         present = Names.query.filter_by(caseid=id, indicator=k)
        #         if present:
        #             Names.query.filter_by(caseid=id, indicator=k).delete()
        #             db.session.commit()

        # delete all case iocs prior to updating the case - yep, i know
        deleteiocsHelper(id)

        integrations_list = []
        for field in form:
            if field.type == "BooleanField":
                integrations_list.append(field.name)
        integrations_tuple = tuple(integrations_list)
        integrations = {field:int(field in request.form) for field in integrations_tuple}
        Cases.query.filter_by(id=id).update(integrations)
        db.session.commit()

        # Insert SlackWebhook
        slackwebhook = request.form['slackwebhook']
        insertslackwebhookHelper(slackwebhook, id)

        # Send form data to formHelper
        insertformHelper(form, id)

        flashmessage = \
                'Case "{}" updated'.format(case.casename)
        flash(flashmessage)
        return redirect(url_for('main.edit', id=id))

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

        Events.query.filter_by(id=id).delete()
        db.session.commit()

        IOCMatches.query.filter_by(id=id).delete()
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
        return redirect(url_for('main.edit', id=id))

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
        form=form,
        notesform=notesform,
        notes=notes,
        events=events
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