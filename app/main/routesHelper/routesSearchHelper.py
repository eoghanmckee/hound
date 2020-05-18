from app.models import Cases, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, \
    Sha256, Sha1, Md5, Filenames, Keywords

def searchHelper(form, search_term):

    search_results = []

    # Search IOC table
    search_results += Cases.query.filter_by(casename=search_term).all()
    names = Names.query.filter_by(indicator=search_term).all()
    usernames = Usernames.query.filter_by(indicator=search_term).all()
    emails = Emails.query.filter_by(indicator=search_term).all()
    keywords = Keywords.query.filter_by(indicator=search_term).all()
    ips = IPaddresses.query.filter_by(indicator=search_term).all()
    domains = Domains.query.filter_by(indicator=search_term).all()
    urls = Urls.query.filter_by(indicator=search_term).all()
    btcs = BTCAddresses.query.filter_by(indicator=search_term).all()
    sha256s = Sha256.query.filter_by(indicator=search_term).all()
    sha1s = Sha1.query.filter_by(indicator=search_term).all()
    md5s = Md5.query.filter_by(indicator=search_term).all()
    filenames = Filenames.query.filter_by(indicator=search_term).all()

    if names:
        for name in names:
            search_results += \
                Cases.query.filter_by(id=name.caseid).all()

    if usernames:
        for username in usernames:
            search_results += \
                Cases.query.filter_by(id=username.caseid).all()

    if emails:
        for email in emails:
            search_results += \
                Cases.query.filter_by(id=email.caseid).all()

    if keywords:
        for keyword in keywords:
            search_results += \
                Cases.query.filter_by(id=keyword.caseid).all()

    if ips:
        for ip in ips:
            search_results += \
                Cases.query.filter_by(id=ip.caseid).all()

    if domains:
        for domain in domains:
            search_results += \
                Cases.query.filter_by(id=domain.caseid).all()

    if urls:
        for url in urls:
            search_results += \
                Cases.query.filter_by(id=url.caseid).all()

    if btcs:
        for btc in btcs:
            search_results += \
                Cases.query.filter_by(id=btc.caseid).all()

    if sha256s:
        for sha256 in sha256s:
            search_results += \
                Cases.query.filter_by(id=sha256.caseid).all()

    if sha1s:
        for sha1 in sha1s:
            search_results += \
                Cases.query.filter_by(id=sha1.caseid).all()

    if md5s:
        for md5 in md5s:
            search_results += \
                Cases.query.filter_by(id=md5.caseid).all()

    if filenames:
        for filename in filenames:
            search_results += \
                Cases.query.filter_by(id=filename.caseid).all()

    if search_term.isdigit():
        userids = UserIDs.query.filter_by(userid=search_term).all()
        phones = Phones.query.filter_by(phones=search_term).all()

        if userids:
            for userid in userids:
                search_results += \
                    Cases.query.filter_by(id=userid.caseid).all()

        if phones:
            for phone in phones:
                search_results += \
                    Cases.query.filter_by(id=phone.caseid).all()

    # dedup any results
    search_results = set(search_results)

    return(search_results)