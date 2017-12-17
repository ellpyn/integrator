'''
    Integrator
    Account fetcher
    Selenium

    Todo:
        - PhantomJS instead of Firefox
        - Store the time when NECU info was loaded
        - Make page autorefresh data every minute
        - Use Markdown and prettify the HTML output
        - Store account data in a sqlite3 database so reloading doesn't necessarily fetch
'''

from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decimal import *
from flask import Flask
import time
import sqlite3

app = Flask(__name__)
print('Initializing Integrator... User account name: {}'.format(environ.get('USERNAME')))

accounts = []

class AccountSummarizer():
    def __init__(self, account_tuples):
        self.accounts = [Account(tpl) for tpl in account_tuples]
        self.time = time.time()

    def count(self):
        return len(self.accounts)

    def available(self):
        return sum([acc.available for acc in self.accounts])

    def total(self):
        return sum([acc.total for acc in self.accounts])

class Account():
    def __init__(self, tpl):
        self.data = tpl
        self.name = tpl[0]
        self.available = tpl[1]
        self.total = tpl[2]

    def recent_transactions():
        pass

def format_acc(tpl): 
    print('{} account: Available ${} || Total: ${}'.format(tpl.name, tpl.available, tpl.total))

def fetch_necu_accounts():
    # Login in to my necu account with selenium/firefox
    url = 'https://www.netteller.com/login2008/Authentication/Views/Login.aspx?returnUrl=%2fnecu'
    browser = webdriver.Firefox()
    browser.get(url)
    lil_box = browser.find_element_by_name('ctl00$PageContent$Login1$IdTextBox')
    lil_box.send_keys(environ.get('NECU_Account') + Keys.RETURN)
    browser.implicitly_wait(10)
    new_box = browser.find_element_by_name('ctl00$PageContent$Login1$PasswordTextBox')
    new_box.send_keys(environ.get('NECU_Password') + Keys.RETURN)
    browser.implicitly_wait(10)
    try:
        browser.find_element_by_id('ctl00_ctl26_retailSecondaryMenuAccountTransactionsMenuItemLinkButton').send_keys(Keys.RETURN)
        browser.implicitly_wait(10)
    except:
        pass
    # Scraping code,  gets the balances of my checking and savings accounts.
    melements = browser.find_elements_by_class_name('POMoneyTableData')
    money_amounts = [Decimal(melement.get_attribute('innerHTML')[1:]) for melement in melements]

    acc_details = browser.find_elements_by_class_name('List')
    acc_details[1].send_keys(Keys.RETURN)

    try:
        browser.find_element_by_id('ctl00_ctl26_retailSecondaryMenuAccountTransactionsMenuItemLinkButton').send_keys(Keys.RETURN)
        browser.implicitly_wait(10)
    except:
        pass

    browser.implicitly_wait(10)

    money_negations = browser.find_elements_by_class_name('Date AccountTransactionsDateColumn')
    print len(money_negations)
    for money_negation in money_negations:
        print money_negation

    accounts = []
    accounts.append(('Savings', money_amounts[0], money_amounts[1]))
    accounts.append(('Checking', money_amounts[2], money_amounts[3]))

    return AccountSummarizer(accounts)

print('Waiting to contact NECU...')
accounts = fetch_necu_accounts()
print('Initial fetch made.')

def cli_account_summary():
    # CLI output
    print('NECU Account Information--')
    print(str(accounts.count()) + ' accounts found')
    for account in accounts.accounts:
        format_acc(account)
    print('Available money: ${}'.format(accounts.available()))
    print('Total money: ${}'.format(accounts.total()))

''' Check when the NECU account was last updated.
    If it was over 1 minute ago, update it again. '''
def ping_necu():
    global accounts
    need_fetch = False

    if accounts.time < time.time() - 100:
        need_fetch = True

    if need_fetch:
        print('Fetching...')
        accounts = fetch_necu_accounts()
    else:
        print('No fetch needed: {} {}'.format(accounts.time, time.time()))

@app.route('/')
def integrator():
    page = ''
    ping_necu()
    for account in accounts.accounts:
        page += '{}: <b>${}</b> available, ${} present<br>\n'.format(account.name, account.available, account.total)
    page += 'Total available: <b>${}</b><br>'.format(accounts.available())
    page += 'Total present: ${}<p>'.format(accounts.total())
    return page + '<font size="144"><b>${}</b></font>'.format(accounts.available())

cli_account_summary()
app.run(debug=False, host='0.0.0.0', port=80)
