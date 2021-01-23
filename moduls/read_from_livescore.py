#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs

def save_obj(obj, name):
    with open('matches_obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('matches_obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_matches():

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    #driver = webdriver.Chrome("./moduls/chromedriver", chrome_options=options)
    driver = webdriver.Chrome("./moduls/chromedriver")

    driver.get("https://www.livescore.in/ru/")
    time.sleep(2)
    tabs = driver.find_elements_by_class_name("tabs__tab")
    tabs[3].click()
    time.sleep(7)
 
    while True:
        try:
            today = driver.page_source
            save_obj(html_to_dict(today), 'today')
            calend = driver.find_elements_by_class_name("calendar__nav")
            calend[1].click()
            time.sleep(7)
            tomorrow = driver.page_source
            save_obj(html_to_dict(tomorrow), 'tomorrow')
            break
        except:
            continue

    driver.close()

def html_to_dict(html):
    try:
        matches = []
        atr_match = [
            "div", 'class_="event__match event__match--scheduled event__match--oneLine"',
            "div", 'class_="event__match event__match--scheduled event__match--last event__match--oneLine"']

        table = bs(html, 'html.parser').find("div", class_="sportName soccer")
        for row in table:
            if row.find("div", class_="event__titleBox"):
                country = row.find("div", class_="event__titleBox")
                spans = country.find_all("span")
                country = f"{spans[0].text}: {spans[1].text}"      
            elif row.find(atr_match):
                match = row.find_all(atr_match)
                if (len(match[1].text) == 5 or match[1].text[5:8] == "TKP"):
                    try:
                        if all([match[5].span != None,
                            match[6].span != None,
                            match[7].span != None]):
                            matches.append({
                                "country": country,
                                "time": match[1].text,
                                "team1": match[2].text,
                                "team2": match[3].text,
                                "kw1": float(match[5].span.text),
                                "kx": float(match[6].span.text),
                                "kw2": float(match[7].span.text)
                                })
                    except IndexError:
                        if all([match[6].span != None,
                            match[7].span != None, 
                            match[8].span != None]):
                            matches.append({
                                "country": country,
                                "time": match[1].text[:5],
                                "team1": match[3].text,
                                "team2": match[4].text,
                                "kw1": float(match[6].span.text),
                                "kx": float(match[7].span.text),
                                "kw2": float(match[8].span.text)
                                })
        return matches
    except:
        time.sleep(2)
        #print("не удалось записать")
        return html_to_dict(html) 

load_matches()