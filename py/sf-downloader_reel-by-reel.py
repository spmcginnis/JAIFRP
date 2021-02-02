from selenium import webdriver
from selenium.webdriver.common.keys import Keys # am I using this?
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests # am I using this?
from time import sleep
import csv

destination = ['D:\\academics\\Research - Digital\\Japanese Internment\\Project Files\\images\\Port1','D:\\academics\\Research - Digital\\Japanese Internment\\Project Files\\images\\SanF1'][1]
    # choose 0=portland 1=SF

options = webdriver.ChromeOptions()
preferences = {"download.default_directory": destination}
options.add_experimental_option("prefs", preferences)
    # adds the stuff listed in profile
WD_path = 'D:\\academics\\Research - Digital\\Japanese Internment\\Project Files\\bin\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=WD_path, chrome_options=options)
    # Optional argument, if not specified will search path.

# series IDs for Portland and SF
P_ID = '40143322'
SF_ID= '38221779'

#building the index for the filenames
Coll_URL_root = 'https://catalog.archives.gov/'

driver.get(Coll_URL_root + 'search?q=*:*&f.parentNaId=' + SF_ID + '&f.level=fileUnit&sort=naIdSort%20asc&rows=1000')
sleep(5)
source = driver.page_source
soup = BeautifulSoup(source, 'lxml')
# divs = soup.find_all('div', class_ = 'resultDetail')
# FP_divs = soup.find_all('div', class_ = 'descriptionResult')

FilePart_list = []
item_list = []
# item_list2 = []

FPIDs = soup.select('div.resultDetail')

for FPID in FPIDs:
    FPID = FPID.get_text().split(':')[1][:9].strip()
    # ID = div.get_text().split(':')[1].split()[0]
    # filename = div.select('.titleResult')[0].get_text()
    # FilePart_list.append([filename, ID])
    FilePart_list.append(FPID)

print(FilePart_list)

# exit()

# _________________________________

ID = FilePart_list[11]
# doing this one Reel (FilePart) at a time.  There are 12 Reels.

# _________________________________

driver.get(Coll_URL_root + 'search?q=*:*&f.parentNaId=' + ID + '&f.level=item&sort=naIdSort%20asc&rows=1000')
sleep(5)
item_source = driver.page_source
item_soup = BeautifulSoup(item_source, 'lxml')
# divs = soup.find_all('div', class_ = 'resultDetail')
item_divs = item_soup.find_all('div', class_ = 'descriptionResult')

for item_div in item_divs:
    itemID = item_div.select('.resultDetail')[0].get_text().split(':')[1].split()[0]
    # ID = div.get_text().split(':')[1].split()[0]
    filename = item_div.select('.titleResult')[0].get_text()

    driver.get('https://catalog.archives.gov/id/'+ itemID)
    print('testing')
    #delay = 100
    #try:
    # myElem =
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//a[@ng-click="changeMedia(objectIndex(doc))"]')))
    WebDriverWait(driver, 100).until_not(EC.element_to_be_clickable((By.XPATH, '//div[@id="loaderDiv"]')))
    # id="loaderDiv"
        # myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(By.XPATH, '//a[@ng-click="changeMedia(objectIndex(doc))"]'))
    print("Page is ready!")
    #except TimeoutException:
        #print("Loading took too much time!")
    print('continuing....')
    driver.find_element_by_xpath('//a[@ng-click="changeMedia(objectIndex(doc))"]').click()
    sleep(5)

    innerHTML = driver.execute_script('return document.body.innerHTML')
    URL = innerHTML.split('downloadFullImage')[1].split('ng-href="')[1].split('"')[0]
    driver.get(URL)

    item_list.append([filename,itemID,URL])
    sleep(10)

with open('../images/SanFrancisco/filname_index.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(item_list)

exit()
