# HFAI Resume Bias Project
This package contains scraper scripts that uses Selenium to scrape user profile information from a list of LinkedIn URLs.

## Set-up
---
### Interactive:
1) Download ChromeDriver for your version of Chrome and ensure that it is executable from the `resume-bias` directory. 

2) Run `selenium_scraper.sh`.
    ```
    . selenium_scraper.sh
    ```

3) Enter username, password, filename, and search_query when prompted to in the console.

### Command Line:
1) Download ChromeDriver for your version of Chrome and ensure that it is executable from the `resume-bias` directory. 

2) Install dependencies.
    ```
    pip3 install -r requirements.txt
    ```

3) Run `selenium_scraper.py` with command-line arguments from the `resume-bias` directory. 
    ```
    python3 selenium_scraper.py -u <username> -p <password> -f <filename> -s <search_query>
    ```
    The `filename` argument is the name of a txt file containing LinkedIn URLs on separate lines (e.g. `users.txt`). The `search_query` argument is the search query for Googling LinkedIn users (e.g. site:linkedin.com/in/ AND "python developer"). If both arguments are specified, the program combines the URLs specified in the txt file and from the Google search query.