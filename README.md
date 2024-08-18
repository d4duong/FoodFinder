# FoodFinder
### Video Demo:  [Watch the Demo](https://youtu.be/OpHqSqjJzCo)
### Description:

FoodFinder is a web application designed to help users search for grocery items across two of Australia's largest supermarkets: Coles and Woolworths. By leveraging web scraping and API integration, FoodFinder gathers data from these supermarkets, stores it in SQLite databases and displays the results through a user-friendly web interface built with Flask, Bootstrap, and Python.

- **Coles**: Data is scraped directly from the Coles website using BeautifulSoup, leveraging its static web page structure.
- **Woolworths**: Data is fetched from Woolworths' API, which provides JSON responses to accommodate its dynamic web page structure.

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

### Setup (Linux/Windows)

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

- **User Authentication**: Sign up, log in, and log out functionality for secure user access.
- **Price Comparison**: Compare prices for grocery items across Coles and Woolworths.
- **Shopping Cart Management**: Add, view, and remove items from a shopping cart, with quantity tracking
- **Multi-Item Search**: Search for multiple items at once and view the consolidated results on one page.
- **Sorting Options**: Sort search results by brand, price (low to high), or price (high to low).

## Project Structure

### Functions/Routes

**__init__.py**

The **__init__.py** file initializes the Flask application and defines several key functions:

- **create_app()**: Initializes the Flask application and configures its settings.
- **login_required(f)**: A decorator to ensure certain routes can only be accessed by authenticated users.
- **aud(value)**: Formats values (e.g., prices) as Australian dollars (AUD).
- **get_cookies()**: Retrieves cookies from the Woolworths website to handle sessions.
- **coles(URL)**: Scrapes grocery item data from the Coles website.
- **woolworths(searchTerm)**: Fetches JSON data from Woolworths' API for a given search term.


**auth.py**

The **auth.py** file handles user authentication, including login, logout, and sign-up functionalities. User data is stored securely in the **users.db** SQLite database.

**views.py**

The **views.py** file manages the core functionality of the FoodFinder app, defining routes and the logic for searching, displaying results, and managing the shopping cart:

- **search()**: Handles single-item searches, scrapes data from Coles and Woolworths, stores the results in scrape.db, and redirects to the /results route.
- **multi_search()**: Handles multi-item searches, retrieves the top two results for each item from Coles and Woolworths, stores them in scrape.db, and redirects to the /results-multi route.
- **results()**, **results_multi()**: Display search results by passing data from scrape.db to the appropriate HTML templates.
- **cart()**: Retrieves and displays items stored in the cart.db database.
- **add_to_cart(food_id)**: Adds an item to the cart, increasing the quantity if the item is already present.
- **remove_from_cart(food_id)**: Decreases the quantity or removes an item from the cart.
- **clear_cart()**: Empties the cart by deleting all entries from the cart.db database.


### Templates

The **templates/** directory contains the HTML files used by the application, structured using Jinja templating to allow dynamic content generation based on user interactions.

- **layout.html**: The base template extended by other HTML files
- **Various HTML files**: Specific pages for search results, the shopping cart, login, sign-up, etc.

### Databases

**users.db**

The **users.db** database stores user login information. Passwords are securely hashed before storage to protect user data.

**scrape.db**

The **scrape.db** database stores the results of grocery item searches from Coles and Woolworths, including details such as brand, title, price, image, and link.

**cart.db**

The **cart.db** database tracks the items users add to their shopping cart, including quantities.

### Styling

The *static/* directory contains the **styles.css** file which includes custom CSS used to make minor adjustments to the Bootstrap-based design.

**main.py**

The **main.py** is the file the entry point of the application, responsible for running the Flask app.

## Contributing

Contributions to FoodFinder are very much welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
