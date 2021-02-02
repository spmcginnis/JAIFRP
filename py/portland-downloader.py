from selenium import webdriver
from selenium.webdriver.common.keys import Keys # am I using this?
from bs4 import BeautifulSoup
import requests # am I using this?
from time import sleep
import csv

destination = ['D:\\academics\\Research - Digital\\Japanese Internment\\Project Files\\images\\Port1','D:\\academics\\Research - Digital\\Japanese Internment\\Project Files\\images\\SanF1'][0]
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

driver.get(Coll_URL_root + 'search?q=*:*&f.parentNaId=' + P_ID + '&f.level=fileUnit&sort=naIdSort%20asc&rows=1000')
sleep(5)
source = driver.page_source
soup = BeautifulSoup(source, 'lxml')
# divs = soup.find_all('div', class_ = 'resultDetail')
divs = soup.find_all('div', class_ = 'descriptionResult')
FilePart_list = []
for div in divs:
    ID = div.select('div.resultDetail')[0].get_text().split(':')[1].split()[0]
    # ID = div.get_text().split(':')[1].split()[0]
    filename = div.select('.titleResult')[0].get_text()
    FilePart_list.append([filename, ID])

FilePart_list2 = []
for FilePart in FilePart_list:
    FilePartName = FilePart[0]
    FilePartID = FilePart[1]
    driver.get('https://catalog.archives.gov/id/'+ FilePartID)
    sleep(5)

    driver.find_element_by_xpath('//a[@ng-click="changeMedia(objectIndex(doc))"]').click()
    sleep(5)

    innerHTML = driver.execute_script('return document.body.innerHTML')
    URL = innerHTML.split('downloadFullImage')[1].split('ng-href="')[1].split('"')[0]
    driver.get(URL)

    FilePart_list2.append([FilePartName,FilePartID,URL])

with open('../images/portland/filename_index.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for n in FilePart_list2:
        writer.writerow(n)

exit()

# https://catalog.archives.gov/search?q=*:*&f.parentNaId=38221779&f.level=fileUnit&sort=naIdSort%20asc
# print(parsed_html.prettify().encode('utf-8'))
# div#resultsView div.row span.titleResult and div.resultDetail
# div.row points to each entry.  titleResult to the title (Reel 1A etc.)  resultDetail to the following:
# <span class="hidden-inline-xs"> <span class="bold">National Archives Identifier:</span>&nbsp;45627616</span>


# URL CONSTRUCTOR
# Navigating to the file
# item_ID = '48438801'
# URL_file = 'Reel-01A_001.pdf'
    # Replace with a data dict

###
URL_root = 'https://catalog.archives.gov/OpaAPI/media/'
URL_branch_1 = '/content/electronic-records/rg-210/'
URL_branch_2 = ['WRAFRB/','WRAFRBSF/']
    # choose 0=portland 1=SF .... check portland branch
download_arg = '?download=true'

target_url = URL_root + item_ID + URL_branch_1 + URL_branch_2[1] + URL_file + download_arg

#for target_url in target_url:
driver.get(target_url)

exit()



from bs4 import BeautifulSoup
from selenium import webdriver

url = "http://legendas.tv/busca/walking%20dead%20s03e02"
browser = webdriver.PhantomJS()
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
a = soup.find('section', 'wrapper')
###
