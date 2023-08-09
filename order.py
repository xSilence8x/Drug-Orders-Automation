from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import csv, json
import time
import logging

logging.basicConfig(filename='script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')


class SeleniumOrder:
    def __init__(self, webpage, login, password):
        """
        It initializes a webdriver with specific options. 
        Then it signs in a given distribution e-shop using
        Selenium.
        """
        self.options = Options()
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(webpage)

        # find username and password fields
        username_field = self.driver.find_element(
            by=By.XPATH, value='//*[@id="Login1_UserName"]')
        password_field = self.driver.find_element(
            by=By.XPATH, value='//*[@id="Login1_Password"]')
        submit_button = self.driver.find_element(
            by=By.XPATH, value='//*[@id="Login1_LoginButton"]')

        username_field.send_keys(login)
        password_field.send_keys(password)
        submit_button.click()
        self.driver.implicitly_wait(0.5)
        
        logging.info("Logging to website was succesful.")
    

    def search_drugs(self, drugs: list):
        """
        This method uses Selenium and BeautifulSoup. It searches for 
        given drug names on a website, scrapes the returned table of 
        results, and saves all the found drug variants to a CSV file.
        E. g. for drug "amoksiklav" it returns Amoksiklav 1G, Amoksiklav 625mg 
        and so on with specific unique drug code (SUKL code).
        """
        results = list()
        for drug in drugs:
            search_field = self.driver.find_element(
                by=By.XPATH, value='//*[@id="cnt1_cnt1_txtSearch"]')
            search_field.clear()
            search_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="cnt1_cnt1_btnSearch"]')

            search_field.send_keys(drug)
            search_button.click()
            self.driver.implicitly_wait(3)

            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            table = soup.find("table", {"class": "gridview"})
            table_body = table.find("tbody")

            if table_body:
                table_rows = table_body.find_all("tr")
                for row in table_rows:
                    cells = row.find_all("td")
                    row_data = [cell.text.strip().split("\n")[0] for cell in cells]
                    results.append(row_data)
            else:
                logging.warning("No element <tbody> found.")

        with open("leky.csv", "w", newline="") as f:
            wr = csv.writer(f)
            wr.writerows(results)
        
        self.driver.quit()
    

    def order_drugs(self, drugs):
        """
        This method parses a JSON file and checks which 
        drugs should be ordered based on the given key: 'objenat.' 
        If its value is 'True,' it then checks for availability 
        on the e-shop using Selenium. If the drug is available, 
        Selenium adds it to the cart in the specified amount.
        """
        for drug in drugs:
            is_in_cart = False
            if drug["objednat"]:
                print(drug["nazev"])
                search_field = self.driver.find_element(
                    by=By.XPATH, value='//*[@id="cnt1_cnt1_txtSearch"]')
                search_field.clear()
                search_button = self.driver.find_element(
                    by=By.XPATH, value='//*[@id="cnt1_cnt1_btnSearch"]')

                search_field.send_keys(drug["kod"])
                search_button.click()
                self.driver.implicitly_wait(3)

                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                res = soup.find(
                    "span", {"id": "ctl00_ctl00_cnt1_cnt1_listProducts_gridView_ctl02_ResultPanel"})

                if res.text == "":
                    logging.info(f"{drug['nazev']} lze objednat!")

                    input_pieces = self.driver.find_element(
                        by=By.XPATH, value='//*[@id="ctl00_ctl00_cnt1_cnt1_listProducts_gridView_ctl02_TextBoxAddN"]')
                    input_pieces.send_keys(drug["pocet"])
                    input_pieces.send_keys(Keys.ENTER)
                    is_in_cart = True

                    drug["objednat"] = False

                    logging.info(
                        f"{drug['nazev']} was added to cart succesfully in amount: {drug['pocet']} pcs.")
                # else:
                #     logging.info(f"{drug['nazev']} - {res.text}")
        if is_in_cart:
            go_to_cart = self.driver.find_element(
                by=By.XPATH, value='//*[@id="btnShowCart"]')
            go_to_cart.click()
            submit = self.driver.find_element(by=By.XPATH, value='//*[@id="cnt1_cnt1_lnkTryCommitCart"]')
            submit.click()
            logging.info("Products were ordered.")

            with open("objednat.json", "w") as f:
                leky = json.dumps(drugs, indent=4)
                f.write(leky)
            logging.info("UPDATED Objednat.json file was saved.")

            time.sleep(2.0)
        else:
            logging.info("No orders were done.")
        self.driver.quit()
