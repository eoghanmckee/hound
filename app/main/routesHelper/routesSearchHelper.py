from app.models import Cases, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, \
    Sha256, Sha1, Md5, Filenames, Keywords

def searchHelper(form, search_term):

    search_results = []
    prelim_results = []
    ioc_types = ['Names', 'Usernames', 'Emails', 'Keywords', 'IPaddresses', 'Domains',\
    'Urls', 'BTCAddresses', 'Sha256', 'Sha1', 'Md5', 'Filenames']

    search_results += Cases.query.filter_by(casename=search_term).all()
    for ioc_type in ioc_types:
        ioc_type = eval(ioc_type)
        prelim_results += ioc_type.query.filter_by(indicator=search_term).all()

    if prelim_results:
        for prelim_result in prelim_results:
            search_results += \
                Cases.query.filter_by(id=prelim_result.caseid).all()

    if search_term.isdigit():
        userids = UserIDs.query.filter_by(indicator=search_term).all()
        phones = Phones.query.filter_by(indicator=search_term).all()

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