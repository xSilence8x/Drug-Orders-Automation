from order import SeleniumOrder
from json_jobs import Data

# Modify list according to your preference.
SEARCH_DRUGS = ["amoksiklav", "xorimax", "zinnat", "ospen", "penbene",
              "augmentin", "ospamox", "duomox", "betaserc", "betahistin"]

FILE_CSV = "leky.csv"
TO_ORDER_JSON = "objednat.json"

# Fill in your login and password.
PAGE = "https://*secret*.cz"
USERNAME = "abcd"
PASSWORD = "1234"

if __name__ == "__main__":
    my_data = Data()
    my_order = SeleniumOrder(webpage=PAGE, login=USERNAME, password=PASSWORD)

    # 1) Search drug names and save CSV with all registered drug variants.
    # my_order.search_drugs(drugs=SEARCH_DRUGS)

    # 2) Convert CSV data to JSON data file.
    # my_data.create_json(csv_file=FILE_CSV)

    # 3) Inspect JSON file, delete drugs you don't want to get ordered.
    # Change amount of packages to be ordered according to your needs.

    # 4) Create list from JSON file data.
    my_order_list = my_data.open_json(file=TO_ORDER_JSON)

    # 5) Run this method to scan e-shop site and order drugs if in stock.
    my_order.order_drugs(drugs=my_order_list)
