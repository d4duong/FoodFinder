# FoodFinder
### Video Demo:  [Watch the Demo](https://youtu.be/OpHqSqjJzCo)
### Description:

FoodFinder is a web application that allows users to search for one or more grocery items and receive results from two of the biggest supermarkets in Australia: Coles and Woolworths. The application uses web scraping and API integration to gather data from these supermarkets, store it in SQLite databases, and display the results on a web interface built with Flask, Bootstrap, and Python.

- **Coles**: Data is scraped directly from the Coles website using BeautifulSoup, as it has a static web page structure.
- **Woolworths**: Data is fetched from Woolworths' API, which provides JSON responses due to its dynamic web page structure.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- Flask
- SQLite
- pip (Python package installer)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/foodfinder.git
   cd foodfinder

2. **Create and activate a virtual environment:**
    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install the dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Set up the SQLite databases:**

    Initialize the databases by running the following commands:
    ```
    sqlite3 scrape.db < init_scrape.sql
    sqlite3 cart.db < init_cart.sql
    sqlite3 users.db < init_users.sql
    ```

5. **Run the application**
    ```
    python main.py
    ```
6. **Access the application:**

    Open your browser and go to http://127.0.0.1:5000.

## Usage
### Search for Items

- **Single Search**: Enter an item name in the search bar and press "Search". The application will display the results from both Coles and Woolworths.
- **Multi-Search**: Enter multiple items (one per line) and press "Multi-Search". The application will display results for all items from both supermarkets.

### Manage Cart

- **Add to Cart**: Click on the "Add to Cart" button next to any search result to add the item to your shopping cart.
- **View Cart**: Go to the Cart page to view all items added to your cart and the total price.
- **Remove from Cart**: Click the "Remove" button to decrease the quantity or remove an item from your cart.
- **Clear Cart**: Click the "Clear Cart" button to remove all items from your cart.

### Features

- **User Authentication**: Sign up, log in, and log out functionality.
- **Price Comparison**: Search for grocery items across Coles and Woolworths and compare prices.
- **Shopping Cart Management**: Add, view, and remove items from a shopping cart.
- **Multi-Item Search**: Search for multiple items at once and view the results on one page.
- **Sorting Options**: Sort search results by brand, price (low to high), or price (high to low).


### website/

**__init__.py**

The __init.py__ file is used to notify the Python interpreter that the directory containing the file (*website/*) is a Python package. Additionally, it contains initialised code and several function definitions. These include:

- *create_app()*: creates a Flask application object so that its functions, methods and attributes can be used.
- *login_required(f)*: a decorated function that only allows the user to access certain routes if they have been authenticated by providing valid credentials via the */login* page.
- *aud(value)*: formats values/item prices in Australian dollars (AUD).
- *get_cookies()*: retrieves cookies from the Woolworths website.
- *coles(URL)*: scrapes information of each grocery item from a single query on the Coles website.
- *woolworths(searchTerm)*: collects all the JSON data from a “products” API endpoint on the Woolworths website


**auth.py**

The **auth.py** file ensures only authorised users can access certain features of FoodFinder. It stores the user’s session over a period of time and allows them to log in, log out and sign up. The user’s data is then stored in a SQL database named “users.db”.

**views.py**

The **views.py** file handles the majority of the routes in the FoodFinder website. Each route then calls a specific function. Among them are:

- *search()*: takes a single grocery item as a user input, scrapes the results of that query from the Coles and Woolworths website, stores them in the “scrape.db” database and then redirects the - user to the */results* route
- *multi_search()*: takes multiple grocery items i.e. a shopping list, retrieves the top two results of each item from Coles and Woolworths,  stores them in the “scrape.db” database and then redirects the user to the */results-multi* route
- *results()*, *results_multi()* and all their respective variations passes the scraped data from “scrape.db” into a .html file so that they can be displayed to the user later on.
- *cart()*: retrieves the data of all the items added to the “cart.db” database
- *add_to_cart(food_id)*: allows for the “Add to Cart” button to be clicked under a particular search result and for its data to be added to the “cart.db” database. If the same item is added to the cart again, it’s quantity will increase by one each time the button is clicked.
- *remove_from_cart(food_id)*: does the opposite of the *add_to_cart()* function.
- *clear_cart()*: removes all items from the cart by truncating the “cart” table in “cart.db”.


### /website/templates/

The **templates/** directory stores all of the HTML files. They each extend upon a base template, namely “layout.html”, and use Jinja to allow for more of a dynamic display.


**users.db**

The **users.db** file is a database that stores the login data of all users. When a user signs up, their login data is added to the “users” table under three columns: "id", "username" and "password". The password stored is the hash of the actual password so that it is more secure. When the user logs in, the details they entered is cross checked with that stored in the database to authorise their access.

**scrape.db**

The **scrape.db** file is another database that stores the data of the grocery items scraped from the Coles and Woolworths website. It is utilised in the *search()* and *multi_search()* function to display data such as the brand, title, price, image and URL of every grocery item displayed.

**cart.db**

The **cart.db** file stores the data of all the items that the user have chosen to add to their cart. If a particular item already exists it the cart but is added again, only its quantity is updated in the table “cart”. It contains almost the exact same columns as scrape.db, but has an extra column “qty”.

**/static/styles.css**

The *static/* directory stores the **styles.css** file which contains some extra CSS. This was used to make minor adjustments to the already pre-existing CSS included in Boostrap.

**main.py**

The **main.py** is the file that runs the entire program.
