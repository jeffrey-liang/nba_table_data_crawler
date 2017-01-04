#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict, deque
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def scrape_table(html):
    '''
    Scrape the data off any stats.nba.com data table.

    Parameters:
    -----------
    html: str
        The page source.

    Returns:
    --------
    data: pandas.core.DataFrame
        The data table of the html page.
    '''

    bs_obj = BeautifulSoup(html, 'lxml')
    # Target table on html
    table = bs_obj.find_all(
        'div', {'class': 'nba-stat-table'})[0].find('tbody')

    # Store data into dictionary
    data = OrderedDict()

    for row in table.find_all('tr'):
        # Store row data.
        row_data = deque()

        for td in row.find_all('td'):

            try:
                # Convert str numbers into floats
                row_data.append(float(td.get_text()))

            except ValueError:
                row_data.append(td.get_text())

        # Use first value of row_data list as key for the dictionary
        data[row_data[0]] = row_data

    # Convert dict to dataframe
    data = pd.DataFrame.from_dict(data, orient='index')

    # Get table headers
    headers = get_header(bs_obj)

    # If headers length is equal to columns, correctly scraped headers
    # off table.
    if len(headers) == len(data.columns):
        data.columns = headers

    # Some tables on nba.com have indexes (numerical), if index was also
    # scraped off the html table, delete the index column, then set headers
    elif data[0].values.dtype is not object:
        if np.array_equal(data.index.values, data[0].values):
            del data[0]
            data.columns = headers
    else:
        print('Failed to get headers')

    return data


def get_header(bs_obj):
    '''
    Gets the header of the BeautifulSoup object that contains the table.

    Parameters
    ----------
    bs_obj: bs4.BeautifulSoup
        BeautifulSoup object that contains the table.

    Returns:
    --------
    columns: list
        List of headers.
    '''

    headers = bs_obj.find_all(
        'div', {'class': 'nba-stat-table'})[0].find('thead')

    columns = deque()

    for header in headers.find_all('th'):
        attributes = header.attrs.keys()

        # Target header values are in 'class' or 'data-field' attributes
        # of each table row. Ignore 'hidden' attributes in table row.
        if 'class' in attributes or 'data-field' in attributes:
            if 'hidden' not in attributes:
                try:
                    columns.append(header.attrs['data-field'])

                except KeyError:
                    # 'TEAM' header is not in 'data-field' attribute, in
                    # 'class' attribute.
                    columns.append(header.get_text())

    return columns


def fetch(url):
    '''
    Fetch the url, then return the page source.

    Parameters:
    -----------
    url: str
        The link of page to fetch.

    Returns:
    --------
    The page source of the url.
    '''
    driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
    print('Fetching: {}'.format(url))
    driver.get(url)
    page_source = driver.page_source
    driver.close()

    return page_source


def crawler(links):
    '''
    Crawls the links and return the tables in the url. 

    Parameters:
    -----------
    links: dict
        Contains the links to be crawled. Key should be name of table,
        value should be url.

    Returns:
    --------
    tables: collections.OrderedDict
        Tables crawled from the links.
        e.g. {'2015-16 Team Total Shooting': pandas.core.DataFrame of table}
    '''

    tables = OrderedDict()

    for table_name, url in links.items():

        tables[table_name] = scrape_table(fetch(url))

    return tables
