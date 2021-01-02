# HFAI Resume Bias Project
This package contains scraper scripts that uses Selenium to scrape user profile information from a list of LinkedIn URLs.

## Set-up
---
### Interactive:
1) Run `selenium_scraper.sh`.
    ```
    . selenium_scraper.sh
    ```

2) Enter username and password when prompted to in the console.

### Specify virtual environment and arguments in the command line:
1) Install dependencies.
    ```
    pip3 install -r requirements.txt
    ```

2) There are three options (a, b, c) to run `selenium_scraper.py` from the `resume-bias` directory.

    a) Export credentials, then run `selenium_scraper.py`.
    ```
    export USERNAME=<username> 
    export PASSWORD=<password>
    python3 selenium_scraper.py
    ```

    b) Run `selenium_scraper.py` with command-line arguments.
    ```
    python3 selenium_scraper.py -u <username> -p <password>
    ```

    c) Run `selenium_scraper.py`, then enter username and password when prompted to in the console.
    ```
    python3 selenium_scraper.py
    ```
