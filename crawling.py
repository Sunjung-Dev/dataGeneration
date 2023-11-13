import requests as req
import pandas as pd
from bs4 import BeautifulSoup
from configparser import ConfigParser

config = ConfigParser()
config.read('/Users/kimsunjung/Desktop/dev/dataGeneration/config.ini')
config.sections()
AMC_URL = config['url']['amc_url']
AMC_SYM_URL = config['url']['amc_sym_url']
SYM_ALL_LISTS = list()

# return { '증상명': '세부증상1', '세부증상2', '세부증상3', '''' }
def crawling():
    res = req.get(AMC_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('ul.contList > li > a')
    sym_dict = dict()
    result_num = 0

    for i in range(len(titles)):
        res = req.get(AMC_SYM_URL + titles[i]['href'])
        title = titles[i].text
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.select("div.searchCont > ul > li > label")
        sym_list = list()
        for i in range(len(result)):
            SYM_ALL_LISTS.append(result[i].string)
            sym_list.append(result[i].string)
        result_num += len(sym_list)
        sym_dict[title] = sym_list
    return sym_dict
