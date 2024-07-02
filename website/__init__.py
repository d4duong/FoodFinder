from bs4 import BeautifulSoup
from flask import Flask, redirect, session
from flask_session import Session
from functools import wraps

import requests


cookies = {}


def create_app():
    app = Flask(__name__)
    app.jinja_env.filters["aud"] = aud
    app.config['SECRET_KEY'] = 'ajflkfsaj asklqwriuc'  
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)  

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def aud(value):
    """Format value as AUD."""
    return f"${value:,.2f}"

def get_cookies():
    cookies.clear()
    r = requests.post('https://www.woolworths.com.au/apis/ui/Search/products')
    for cookie in r.cookies:
        cookies[cookie.name] = cookie.value
    
def coles(URL):
    COLS_URL = URL
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate, br", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Upgrade-Insecure-Requests": "1"
        }

    page1 = requests.get(COLS_URL, headers=headers)

    soup = BeautifulSoup(page1.content, "lxml")

    sections = soup.find_all("section", attrs={"data-testid":'product-tile'})

    return sections

def woolworths(searchTerm):

    url = "https://www.woolworths.com.au/apis/ui/Search/products"
    
    if len(cookies) == 0:
        get_cookies()

    payload = {
        "Filters": [],
        "IsSpecial": False,
        "Location": f"/shop/search/products?searchTerm{searchTerm}",
        "PageNumber": 1,
        "PageSize": 36,
        "SearchTerm": searchTerm,
        "SortType": "TraderRelevance",
        "IsRegisteredRewardCardPromotion": None,
        "ExcludeSearchTypes": ["UntraceableVendors"],
        "GpBoost": 0,
        "GroupEdmVariants": True,
        "EnableAdReRanking": False
    }
    headers = {
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.woolworths.com.au",
        "pragma": "no-cache",
        "referer": f"https://www.woolworths.com.au/shop/search/products?searchTerm={searchTerm}",
        "request-id": "|31cee3cb54ce40d696954543340c705e.eba7906a76084910",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-31cee3cb54ce40d696954543340c705e-eba7906a76084910-01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.request("POST", url, cookies=cookies, json=payload, headers=headers)

    return response.json()


