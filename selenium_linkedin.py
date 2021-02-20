from selenium import webdriver
from time import sleep
import argparse
import logging
import os
import sys
import getpass
import stdiomask

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class SeleniumLinkedin():
    
    def __init__(self, args=None, **kwargs):
        if isinstance(args, argparse.Namespace):
            self.username = args.username
            self.password = args.password
            self.filename = args.filename
            self.search_query = args.search_query
        else:
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            self.filename = kwargs.get('filename')
            self.search_query = kwargs.get('search_query')

        self.set_chrome_options()
        self.login()
        self.generate_data()

    def set_chrome_options(self):
        """
        Sets Chrome driver options, such as configuring Chrome to download files to the current directory.
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()+"/profiles"})
        path = '{}/chromedriver'.format(os.getcwd())
        self.driver = webdriver.Chrome(executable_path=path, options=options)

    def login(self):
        """
        Automates logging in to a LinkedIn account in a Chrome guest browser.
        """
        logging.info("Logging into your LinkedIn account...")

        self.driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

        username = self.driver.find_element_by_id('username')
        username.send_keys(self.username)
        sleep(2)

        password = self.driver.find_element_by_id('password')
        password.send_keys(self.password)
        sleep(2)

        password.submit()

    def read_user_list(self, filename):
        """
        Given the name of a txt file with a LinkedIn URL on each line, reads in the users.
        Returns a list of the URLs in the txt files.
        """
        logging.info("Reading in users from {}...".format(filename))
        users = []

        if os.path.isfile(filename):
            with open(filename, 'r') as in_file:
                users = [line.strip() for line in in_file]
        else:
            logging.error("{} file doesn't exist.".format(filename))
        
        return users

    def google_search_users(self, search_query):
        """
        Given a search query, automates searching on Google for a user associated with specific keywords.
        Returns a list of LinkedIn URLs.
        """
        logging.info("Google searching LinkedIn profiles with query {}...".format(search_query))
        users = []

        self.driver.get('https://www.google.com')
        sleep(3)

        search = self.driver.find_element_by_name('q')
        search.send_keys('site:linkedin.com/in/ AND ' + search_query)
        sleep(0.5)

        search.submit()
        sleep(3)

        linkedin_urls = self.driver.find_elements_by_class_name('iUh30')
        users = [url.text for url in linkedin_urls]
        sleep(0.5)

        return users

    def get_user(self, linkedin_url):
        """
        Given a LinkedIn URL for a user, scrapes data on that user.
        Returns a pandas DataFrame for each user.
        """
        logging.info("Scraping data from {}...".format(linkedin_url))

        self.driver.get(linkedin_url)
        split_url = linkedin_url.split("/")
        user_path = split_url[-2] if split_url[-1] == "" else split_url[-1]

        self.driver.find_element_by_class_name('msg-overlay-bubble-header').click()
        
        self.driver.find_element_by_xpath("//div[contains(@class, 'pv-s-profile-actions__overflow ember-view')]").click()
        sleep(2)

        # saves profile to pdf 
        self.driver.find_element_by_xpath("//div[contains(@class, 'save-to-pdf')]").click()
        sleep(5)

        pdf_file = user_path + '.pdf'
        os.rename('profiles/Profile.pdf', 'profiles/' + pdf_file)
        
    def generate_data(self):
        """
        Driver function for the program.
        """
        users = []

        if self.filename and self.search_query:
            users = self.read_user_list(self.filename) + self.google_search_users(self.search_query)
        elif self.filename:
            users = self.read_user_list(self.filename)
        elif self.search_query:
            users = self.google_search_users(self.search_query)
        else:
            logging.warning("No users to scrape...")
        
        os.mkdir("profiles")

        for user in users:
            sleep(4)
            self.get_user(user) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help="Enter LinkedIn username")
    parser.add_argument('-p', '--password', help="Enter LinkedIn password")
    parser.add_argument('-f', '--filename', help="Enter name of txt file containing LinkedIn URLs")
    parser.add_argument('-s', '--search_query', help="Enter search query for Googling LinkedIn users")
    args = parser.parse_args()

    if args.username and args.password:
        obj = SeleniumLinkedin(args)
    else: 
        kwargs = {}
        kwargs['username'] = input("Enter your username: ")
        kwargs['password'] = stdiomask.getpass("Enter your password: ")
        answer = input("How will you be providing your LinkedIn URLs? Type 'file' for txt file or 'search' for Google search query: ")
        if answer.strip().lower() == 'file':
            kwargs['filename'] = input("Enter the name of your txt file (e.g. users.txt) containing LinkedIn URLs: ")
        else: 
            kwargs['search_query'] = input("Enter your search query for Googling LinkedIn users: ")
        obj = SeleniumLinkedin(**kwargs)