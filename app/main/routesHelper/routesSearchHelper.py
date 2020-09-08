from sqlalchemy import cast
from sqlalchemy.types import String
from app.models import Cases, Names, Usernames, UserIDs, \
    Emails, Phones, IPaddresses, Domains, Urls, BTCAddresses, \
    Sha256, Sha1, Md5, Filenames, Keywords

def searchHelper(form, search_term):

    search_results = []
    prelim_results = []
    ioc_types = ['Names', 'Usernames', 'UserIDs', 'Phones', 'Emails', 'Keywords', 'IPaddresses', 'Domains',\
    'Urls', 'BTCAddresses', 'Sha256', 'Sha1', 'Md5', 'Filenames']

    # search_term_fuzzy = "%{}%".format(search_term)

    search_results += Cases.query.filter(Cases.casename.like("%" + search_term + "%")).all()
    for ioc_type in ioc_types:
        ioc_type = eval(ioc_type)
        prelim_results += ioc_type.query.filter(cast(ioc_type.indicator, String).like("%" + search_term + "%")).all()

    if prelim_results:
        for prelim_result in prelim_results:
            search_results += \
                Cases.query.filter_by(id=prelim_result.caseid).all()

    # dedup any results
    search_results = set(search_results)
    return(search_results)