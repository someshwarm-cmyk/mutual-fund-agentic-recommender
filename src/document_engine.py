def extract_amc(scheme_name):

    scheme_name = scheme_name.lower()

    if "sbi" in scheme_name:
        return "sbi"
    if "hdfc" in scheme_name:
        return "hdfc"
    if "axis" in scheme_name:
        return "axis"
    if "icici" in scheme_name:
        return "icici"
    if "nippon" in scheme_name:
        return "nippon"
    if "aditya" in scheme_name:
        return "aditya"
    if "kotak" in scheme_name:
        return "kotak"
    if "uti" in scheme_name:
        return "uti"
    if "tata" in scheme_name:
        return "tata"

    return None


def get_amc_document_link(amc):

    links = {
        "sbi": "https://www.sbimf.com/en-us/resources",
        "hdfc": "https://www.hdfcfund.com/statutory-disclosure",
        "axis": "https://www.axismf.com/documents",
        "icici": "https://www.icicipruamc.com/downloads",
        "nippon": "https://mf.nipponindiaim.com/downloads",
        "aditya": "https://mutualfund.adityabirlacapital.com/resources",
        "kotak": "https://www.kotakmf.com/Information",
        "uti": "https://www.utimf.com/forms-and-downloads",
        "tata": "https://www.tatamutualfund.com/downloads",
    }

    return links.get(amc)


def get_scheme_document_search_link(scheme_name):

    query = scheme_name.replace(" ", "+") + "+mutual+fund+SID+factsheet+pdf"

    return f"https://www.google.com/search?q={query}"


def get_amfi_scheme_link(code):

    if code is None:
        return None

    return f"https://www.amfiindia.com/nav-details?schemeCode={code}"