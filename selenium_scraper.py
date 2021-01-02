from selenium import webdriver
from time import sleep
import pandas as pd
import argparse
import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class SeleniumScraper():
    def __init__(self, args=None, **kwargs):
        if isinstance(args, argparse.Namespace):
            self.username = args.username
            self.password = args.password
        else:
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')

        self.driver = webdriver.Chrome('{}/chromedriver'.format(os.getcwd()))
        self.login()
        self.generate_data('users.txt')
                
    def login(self):
        logging.info("Logging into your LinkedIn account...")

        self.driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

        username = self.driver.find_element_by_id('username')
        username.send_keys(self.username)
        sleep(0.5)

        password = self.driver.find_element_by_id('password')
        password.send_keys(self.password)
        sleep(0.5)

        password.submit()

    def read_user_list(self, filename):
        logging.info("Reading in users from {}...".format(filename))
        users = []
        
        if os.path.isfile(filename):
            with open(filename, 'r') as in_file:
                users = [line.strip() for line in in_file]
        else:
            logging.error("users.txt file doesn't exist.")
        
        return users

    def google_search_users(self, search_query):
        logging.info("Google searching LinkedIn profiles with query {}...".format(search_query))
        users = []

        self.driver.get('https://www.google.com')
        sleep(3)

        search = self.driver.find_element_by_name('q')
        search.send_keys(search_query)
        sleep(0.5)

        search.submit()
        sleep(3)

        linkedin_urls = self.driver.find_elements_by_class_name('iUh30')
        users = [url.text for url in linkedin_urls]
        sleep(0.5)

        return users

    def scrape(self, linkedin_url):
        logging.info("Scraping data from {}...".format(linkedin_url))
        self.driver.get(linkedin_url)
        df = pd.DataFrame()
        
    def generate_data(self, users_txt_file=None):
        users = []

        if users_txt_file:
            users = self.read_user_list(users_txt_file)
        else:
            users = self.google_search_users('site:linkedin.com/in/ AND "python developer" AND "London"')
            
        for user in users:
            self.scrape(user) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help="Enter LinkedIn username")
    parser.add_argument('-p', '--password', help="Enter LinkedIn password")
    args = parser.parse_args()
    kwargs = {}

    USERNAME = os.getenv('USERNAME')  # $export USERNAME=<username>
    PASSWORD = os.getenv('PASSWORD')  # $export PASSWORD=<password>
    
    if USERNAME and PASSWORD:
        kwargs['username'] = USERNAME
        kwargs['password'] = PASSWORD
        obj = SeleniumScraper(**kwargs)
    elif args.username and args.password:
        obj = SeleniumScraper(args)
    else: 
        kwargs['username'] = input("Enter your username: ")
        kwargs['password'] = input("Enter your password: ")
        obj = SeleniumScraper(**kwargs)
