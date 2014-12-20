# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 20:59:57 2014

@author: quantum2015
"""

import requests
import bs4
import re
import csv

root_url = 'http://suchen.mobile.de'
index_url = root_url + '/auto/bmw-520.html?useCase=RefineSearch&damageUnrepaired=NO_DAMAGE_UNREPAIRED&__lp=100&scopeId=C&sortOption.sortBy=searchNetGrossPrice&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=17&makeModelVariant1.searchInFreetext=false&makeModelVariant2.searchInFreetext=false&makeModelVariant3.searchInFreetext=false&ambitCountry=DE&export=ALSO_EXPORT&lang=en'
def get_page_ID():
    """
    extract the last page link, and the position where the page number located
    """
    response = requests.get(index_url);
    soup = bs4.BeautifulSoup(response.text);
    end_page = soup.find('a',class_='pg-btn page-end')  # find the link for the end page,  then the number of total page is known
    end_page_url = end_page.get('href');                # find the link for the end page,  then the number of total page is known
    pageNumberString= re.findall('pageNumber=\d+',end_page_url);  #extract the page number from the link
    endPageNum = int(re.findall('\d+',pageNumberString[0])[0]);   # take the element from last extraction then transfer it to int number
    return endPageNum, end_page_url
    

#print(get_page_ID())    

def replace_url_pageNumber():
    
    """
    replace the page numbers to get all the sub page's link
    """
    temp_str1 = 'pageNumber=' + str(get_page_ID()[0]);
    for ii in range(1,get_page_ID()[0]):
        temp_str2 = 'pageNumber=' + str(ii);
        replaced_url_address = get_page_ID()[1].replace(temp_str1,temp_str2)
        print get_subUrl_pages(replaced_url_address)
    
def get_subUrl_pages(url_nextPages):
    
    """
    extract the links for the normal Advertisement only
    """
    response = requests.get(url_nextPages);
    soup = bs4.BeautifulSoup(response.text);
    with open("auto_data.csv","w") as f:
        for div_start in soup.find_all('div', class_='listEntry normalAd '): #look only the normal Advertisement
            sub = div_start.find('a',class_='infoLink detailsViewLink');  #the link in normal Advertisement
            sub_url = sub.get('href');     # get the link
            auto_data_summary = get_subUrl_pages_contents(sub_url);
            writer = csv.writer(f, dialect='excel')
            writer.writerow(auto_data_summary)
            print auto_data_summary
    return
    
def get_subUrl_pages_contents(sub_url):
    
    """
    extract all the auto parameters from a single page
    """
    response_next = requests.get(sub_url);
    soup_next = bs4.BeautifulSoup(response_next.text);
    auto_data_price = soup_next.find('p',class_='pricePrimaryCountryOfSale priceGross');
    auto_data_Maintech_data = soup_next.find('div', class_='mainTechnicalData');
    return  auto_data_price.text, auto_data_Maintech_data.text.replace('\n', '|')   
    
print replace_url_pageNumber()    
