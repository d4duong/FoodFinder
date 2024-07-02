from flask import Blueprint, render_template, request, redirect, session, flash
from . import login_required, coles, woolworths, get_cookies
from cs50 import SQL


views = Blueprint('views', __name__)

db = SQL("sqlite:///scrape.db")
cdb = SQL("sqlite:///cart.db")

@views.route('/')
@login_required
def index():
    return redirect("/search")


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
      
        db.execute("DROP TABLE data")
        db.execute(
            "CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, brand TEXT, title TEXT, price INTEGER NOT NULL, image TEXT, link TEXT)"
            )

        search = request.form.get('item')
        search = search.lower().rstrip()
        session['search'] = search
        COLS_URL = f'https://www.coles.com.au/search?q={search}'
        s = search.split(' ', maxsplit=1)
        s[0] = s[0].rstrip()

        sections1 = coles(COLS_URL)
        try:
            for section in sections1:
                brand = "Coles"
                title = section.find("h2", attrs={"class":'LinesEllipsis product__title'})
                t = title.text.strip()
                price = section.find("span", attrs={"class":'price__value'})
                if price:
                    price = price.text.strip().removeprefix('$')
                    l = section.find("a", attrs={"class":'product__link'})
                    link = 'https://www.coles.com.au' + l.get('href')
                    images = section.find_all("img", attrs={"data-testid":'product-image'})
                    for i in images:
                        if 'productimages' in i['src']:
                            image = 'https://www.coles.com.au' + i['src']
                            db.execute("INSERT INTO data (brand, title, price, image, link) VALUES(?, ?, ?, ?, ?)",
                            brand, t, price, image, link)
                        else:
                            continue
                else:
                    continue

            sections2 = woolworths(search)
            for section2 in sections2['Products']:
                sec2 = section2['Products'][0]
                brand2 = "Woolworths"
                title2 = sec2['DisplayName']
                price2 = sec2['Price']
                image2 = sec2['LargeImageFile']
                stockcode = sec2['Stockcode']
                urlName = sec2['UrlFriendlyName']
                link2 = "https://www.woolworths.com.au/shop/productdetails/" + f"{stockcode}/" + urlName

                if price2:
                    db.execute("INSERT INTO data (brand, title, price, image, link) VALUES(?, ?, ?, ?, ?)",
                    brand2, title2, price2, image2, link2)
                else:
                    continue
        except TypeError:
            flash('No results. Please enter a valid item.', category='error')
        else:
            return redirect("/results")
    get_cookies()
    return render_template("index.html")

@views.route('/multi-search', methods=['GET', 'POST'])
@login_required
def multi_search():
    if request.method == 'POST':

        db.execute("DROP TABLE data")
        db.execute(
            "CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, search TEXT, brand TEXT, title TEXT, price INTEGER NOT NULL, image TEXT, link TEXT)"
            )
            
        items = request.form.get('items')
        items = items.lower().rstrip()
        shopping_list = items.split('\n')
        try:
            for item in shopping_list:

                    COLS_URL = f'https://www.coles.com.au/search?q={item}'
                    s = item.split(' ', maxsplit=1)
                    s[0] = s[0].rstrip()
                    item = item.rstrip()
                    sections1 = coles(COLS_URL)
                    try:
                        for i in range(2):
                            brand = "Coles"
                            title = sections1[i].find("h2", attrs={"class":'LinesEllipsis product__title'})
                            t = title.text.strip()
                            item = item.capitalize()
                            price = sections1[i].find("span", attrs={"class":'price__value'})
                            if price and (s[0] in t.lower()):
                                price = price.text.strip().removeprefix('$')
                                l = sections1[i].find("a", attrs={"class":'product__link'})
                                link = 'https://www.coles.com.au' + l.get('href')
                                images = sections1[i].find_all("img", attrs={"data-testid":'product-image'})
                                for j in images:
                                    if 'productimages' in j['src']:
                                        image = 'https://www.coles.com.au' + j['src']
                                        db.execute("INSERT INTO data (search, brand, title, price, image, link) VALUES(?, ?, ?, ?, ?, ?)",
                                        item, brand, t, price, image, link)
                                    else:
                                        continue
                            else:
                                continue

                        sections2 = woolworths(item)
                        for k in range(2):
                            sec2 = sections2['Products'][k]['Products'][0]
                            brand2 = "Woolworths"
                            title2 = sec2['DisplayName']
                            price2 = sec2['Price']
                            image2 = sec2['LargeImageFile']
                            stockcode = sec2['Stockcode']
                            urlName = sec2['UrlFriendlyName']
                            link2 = "https://www.woolworths.com.au/shop/productdetails/" + f"{stockcode}/" + urlName

                            if price2:
                                db.execute("INSERT INTO data (search, brand, title, price, image, link) VALUES(?, ?, ?, ?, ?, ?)",
                                item, brand2, title2, price2, image2, link2)
                                
                        else:
                            continue
                    except IndexError:
                        flash('One or more items are invalid. Unable to retrieve its results. ', category='error')
        except TypeError:
            flash('One or more items are invalid. Unable to retrieve its results.', category='error')
        else:
            return redirect("/results-multi")
    return render_template("multi_search.html")

@views.route('/results-multi')
@login_required
def results_multi():
    rows = db.execute("SELECT * FROM data")
    return render_template("multiresults.html", rows=rows)

@views.route('/results-multi-brand')
@login_required
def multi_brand():
    rows = db.execute("SELECT * FROM data ORDER BY brand")
    return render_template("multiresults.html", rows=rows)

@views.route('/results-multi-pricelth')
@login_required
def multi_pricelth():
    rows = db.execute("SELECT * FROM data ORDER BY search, price")
    return render_template("multiresults.html", rows=rows)

@views.route('/results-multi-pricehtl')
@login_required
def multi_pricehtl():
    rows = db.execute("SELECT * FROM data ORDER BY search, price DESC")
    return render_template("multiresults.html", rows=rows)


@views.route('/results')
@login_required
def results():
    result = session.get('search', None)
    rows = db.execute("SELECT * FROM data ORDER BY RANDOM()")
    return render_template("results.html", rows=rows, result=result)

@views.route('/results-brand')
@login_required
def brand():
    result = session.get('search', None)
    rows = db.execute("SELECT * FROM data ORDER BY brand")
    return render_template("results.html", rows=rows, result=result)

@views.route('/results-price-lth')
@login_required
def price_lth():
    result = session.get('search', None)
    rows = db.execute("SELECT * FROM data ORDER BY price")
    return render_template("results.html", rows=rows, result=result)

@views.route('/results-price-htl')
@login_required
def price_htl():
    result = session.get('search', None)
    rows = db.execute("SELECT * FROM data ORDER BY price DESC")
    return render_template("results.html", rows=rows, result=result)

@views.route('/<int:food_id>/add_to_cart')
@login_required
def add_to_cart(food_id):
    food = db.execute("SELECT brand, title, price, image, link FROM data WHERE id = ?", food_id)
    cart_item = cdb.execute("SELECT * FROM cart WHERE title = ?", food[0]["title"])
    if len(cart_item) == 0:
        qty = 1
        cdb.execute("INSERT INTO cart (brand, title, price, image, link, qty) VALUES(?, ?, ?, ?, ?, ?)", food[0]["brand"], food[0]["title"], food[0]["price"], food[0]["image"], food[0]["link"], qty)
    else:
        qty = cart_item[0]["qty"] + 1
        cdb.execute("UPDATE cart SET qty = ? WHERE title = ?", qty, food[0]["title"])

    return redirect("/cart")

@views.route('/cart/<int:food_id>/remove')
@login_required
def remove_from_cart(food_id):
    cart_item = cdb.execute("SELECT * FROM cart WHERE cart_id = ?", food_id)
    if cart_item[0]["qty"] > 1:
        qty = cart_item[0]["qty"] - 1
        cdb.execute("UPDATE cart SET qty = ? WHERE cart_id = ?", qty, food_id)
    else:
        cdb.execute("DELETE FROM cart WHERE cart_id = ?", food_id)
    return redirect("/cart")

@views.route('/cart')
@login_required
def cart():
    rows = cdb.execute("SELECT * FROM cart")
    total = cdb.execute("SELECT SUM(price) FROM cart")
    if total[0]["SUM(price)"] is None:
        total[0]["SUM(price)"] = 0
    return render_template("cart.html", rows=rows, total=total[0]["SUM(price)"])

@views.route('/cart/clear')
@login_required
def clear_cart():
    cdb.execute("DELETE FROM cart")
    rows = cdb.execute("SELECT * FROM cart")
    total = 0
    return render_template("cart.html", rows=rows, total=total)