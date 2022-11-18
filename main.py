#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytimeparse.timeparse import timeparse
from string import Formatter
import os
import notify2
PATH = "/usr/bin/chromedriver"


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
series = []
lseries = []

def strfdelta(tdelta, fmt='{H:02}h {M:02}m', inputtype='timedelta'):
    if inputtype == 'timedelta':
        remainder = int(tdelta.total_seconds())
    elif inputtype in ['s', 'seconds']:
        remainder = int(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = int(tdelta) * 60
    elif inputtype in ['h', 'hours']:
        remainder = int(tdelta) * 3600

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('H', 'M')
    constants = {'H': 3600, 'M': 60}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)


def login_erp(user_name, passwd):
    driver.get("https://erp.cisin.com/todaytimesheet.asp")
    driver.find_element(By.NAME, 'uname').send_keys(user_name)
    driver.find_element(By.NAME, 'pass').send_keys(passwd)
    driver.find_element(By.CLASS_NAME, 'submit-login').send_keys(Keys.ENTER)
    return 0


def total_working_hours():
    j = 0
    for i in series:
        if i > 0:
            j += 1
        else:
            pass
    return j*8


def working_hours(user_name, passwd):
    login_erp(user_name, passwd)
    driver.get("https://erp.cisin.com/todaytimesheet.asp")
    driver.find_element(By.LINK_TEXT, 'Monthly').click()
    driver.switch_to.frame(driver.find_element(By.NAME, "_ddajaxtabsiframe-countrydivcontainer"))
    elem = driver.find_element(By.CLASS_NAME, "msrcd")
    # elem.find_element(By.XPATH, "//tbody")  #get name
    d = elem.find_element(By.XPATH, "//table[@id='product-table']")
    soup = BeautifulSoup(d.get_attribute('innerHTML'), features='lxml')
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    rdata = rows[-2]
    for hrs in rdata:
        hr = hrs.text
        if hr.endswith('min'):
            t = timeparse(hr)
            series.append(t)
            if t > 0:
                lseries.append(t)
    driver.quit()
    return series


def notify(dis):
    icon_path = os.path.expanduser('~/.remhours/war.png')
    notify2.init('ERP notification')
    n = notify2.Notification('Hello', dis, icon = icon_path)
    n.set_urgency(notify2.URGENCY_CRITICAL)
    n.set_timeout(100)
    return n.show()


if os.path.exists(os.path.expanduser('~/.remhours/config')):
    pass
else:
    os.mkdir(os.path.expanduser('~/.remhours'))
    with open(os.path.expanduser('~/.remhours/config'), 'w') as config:
        config.write("<user_name>\n<passwd>")
        notify(f"Add credentials in {os.path.expanduser('~/')}.remhours/config file.")
        exit()

def main():
    file_path = os.path.expanduser('~/.remhours/config')
    config = open(file_path, 'r')
    c = config.read().split()
    u = c[0]
    p = c[1]

    s = working_hours(u, p)
    worked_hours = timedelta(seconds=sum(s))
    total_hours = timedelta(hours=total_working_hours())
    last_day_hours = timedelta(seconds=lseries[-1])

    print(f'')
    if worked_hours <= total_hours:
        lagging_by = strfdelta(total_hours - worked_hours)
        result = f'Lagging by:  {lagging_by} \nLast day hours:  {strfdelta(last_day_hours)}'
        notify(result)
        print(result)
    else:
        ahead_by = worked_hours - total_hours
        result = f'Ahead by:  {ahead_by} \nLast day hours:  {strfdelta(last_day_hours)}'
        notify(result)
        print(result)


if __name__ == '__main__':
    main()