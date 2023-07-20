import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from bs4 import BeautifulSoup as bs
from main import exportToCSV

def motleyMultiplePages(soup):
    Titles, Authors, authorClean, Dates = [], [], [], []
    for tag in soup.find_all('h5', attrs="self-center mb-6 font-medium md:text-h5 text-md md:mb-4px"):
        Titles.append(tag.get_text())
    for tags in soup.find_all('div', attrs="text-sm text-gray-800 mb-2px md:mb-8px"):
        date, author = [x for x in (tags.text.split('\n')) if x.strip() != '']
        Authors.append(author)
        Dates.append(date)
    for author in Authors:
        authorClean.append([x for x in (author.split('by ')) if x.strip() != ''][0])
    out = zip(Titles, authorClean, Dates)
    return out

def motleyFoolScrape():
    url = "https://www.fool.com/investing-news/"
    pages = 15
    Titles, authorClean, Dates = [], [], []
    for i in range(1, pages + 1):
        ss = requests.get(url + "?page=" + i.__str__())
        data = ss.text
        soup = bs(data, 'html.parser')
        resultMotley = motleyMultiplePages(soup)
        for item1, item2, item3 in resultMotley:
            Titles.append(item1)
            authorClean.append(item2)
            Dates.append(item3)
    Table = pd.DataFrame()
    Table['Titles'] = Titles
    Table['Author'] = authorClean
    Table['Date'] = pd.to_datetime(Dates)
    Table = Table.drop_duplicates(subset=['Titles'])
    Table = Table.sort_values(by=['Date'])
    print(Table.to_json())
    exportToCSV(Table)


