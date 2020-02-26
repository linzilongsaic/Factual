
# python3 factual_v2.py -Q "near" -L "bloomington" -R "in"
# python3 factual_v2.py -F "combination_complete-yelp2.txt"
import os
import re
import sys
import json
import time
import platform
import random
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import quote
from util import sleepBar, prettyOutputName

# 统计总访问次数
total_visit_num = 0

# 开启Chrome浏览器
def initBrowser(headless=False):
    if "Windows" in platform.system():
        chrome_path = "driver/chromedriver.exe"
    else:
        chrome_path = "driver/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--disable-features=NetworkService")
    if headless:
        chrome_options.add_argument('headless')
    browser = webdriver.Chrome(options=chrome_options,executable_path=chrome_path)
    return browser


# Search on Google and returns the list of PAA questions in SERP.
def newSearch(browser, email, password):
    # 查找登录输入框
    browser.get("https://accounts.factual.com/login")
    inputbox1 = browser.find_element_by_xpath("//input[@placeholder='Email']")
    inputbox2 = browser.find_element_by_xpath("//input[@placeholder='Password']")
    # 向登录输入框中输入邮箱和密码
    inputbox1.send_keys(email)
    inputbox2.send_keys(password)
    sleepBar(2)
    # 登录按钮
    searchbtn1 = browser.find_elements_by_xpath("//input[@type='submit']")
    try:
        searchbtn1[-1].click()
    except:
        searchbtn1[0].click()
    sleepBar(2)
    # 查找进入搜索界面的入口, 并进入
    searchbtn2 = browser.find_elements_by_xpath("//a[@href='//places.factual.com/data/t/places']")
    searchbtn2[-1].click()
    sleepBar(2)
    return browser


# 将关键词输入框中, 完成爬取后, 删除框内内容
def searchItems(browser, query_combination, limitation=-1):
    query, region, locality = query_combination

    # 检测 region 和locality是否为空
    only_query = False
    if region == "" and locality == "":
        only_query = True

    # 查找搜索输入框
    q_inputbox = browser.find_element_by_xpath("//input[@id='search-query']")
    # 向搜索输入框中输入内容
    q_inputbox.send_keys(query)
    sleepBar(2)
    time.sleep(random.uniform(0,1))

    # 检查是否有报错
    haveError = checkError(browser)
    if haveError:
        print("WARNING: error happens")

    if not only_query:
        # 输入地区
        region_inputbox = browser.find_element_by_xpath("//div[@id='s2id_facet-selector-region']//input[@type='text']")
        if random.choice([True, False]):
            region_inputbox.click()
        region_inputbox.send_keys(region)
        region_inputbox.send_keys(Keys.ENTER)
        sleepBar(1)
        time.sleep(random.uniform(0, 1))

        # 输入城市
        locality_inputbox = browser.find_element_by_xpath("//div[@id='s2id_facet-selector-locality']//input[@type='text']")
        if random.choice([True, False]):
            locality_inputbox.click()
        locality_inputbox.send_keys(locality)
        locality_inputbox.send_keys(Keys.ENTER)
        sleepBar(1)
        time.sleep(random.uniform(0, 1))

    # 查找搜索按钮
    searchbtn3 = browser.find_elements_by_xpath("//button[@type='submit']")
    try:
        searchbtn3[-1].click()
    except:
        searchbtn3[0].click()
    sleepBar(1)
    time.sleep(random.uniform(0, 1))

    # 提取此关键词搜索出来的信息
    endsign = False
    infostore = []
    iter = 0
    while not endsign:
        info = extraction(browser)
        global total_visit_num
        total_visit_num += 1
        browser, endsign = checkEnd(browser)
        infostore += info
        # 对每个关键词所爬取的页面进行限制
        iter += 1
        if limitation > 0:
            if iter >= limitation:
                endsign = True

    # 删除输入框中的信息, 为下次输入做准备
    q_inputbox4delete = browser.find_element_by_xpath("//input[@id='search-query']")
    deleteInfo(q_inputbox4delete, True, query)
    sleepBar(1)
    time.sleep(random.uniform(0, 1))

    if not only_query:
        region_inputbox4delete = browser.find_element_by_xpath("//div[@id='s2id_facet-selector-region']//input[@type='text']")
        deleteInfo(region_inputbox4delete, False)
        sleepBar(1)
        time.sleep(random.uniform(0, 1))

        locality_inputbox4delete = browser.find_element_by_xpath("//div[@id='s2id_facet-selector-locality']//input[@type='text']")
        deleteInfo(locality_inputbox4delete, False)
        sleepBar(1)
        time.sleep(random.uniform(0, 1))

    return infostore


# 删除刚刚输入部分
def deleteInfo(inputbox, have_X=False, query=""):
    # have_X 表示是否可用"X"键删除内容
    # 若可用"X"键删除内容, 则删除方法二选一; 若不可用"X"键删除内容, 则用删除方法二.
    if have_X:
        deleteMethod = random.randint(1,2)
    else:
        deleteMethod = 2

    # 具体删除方法
    if deleteMethod == 1:
        # 删除方法1: 查找删除按钮
        searchbtn5 = browser.find_elements_by_xpath("//button[@type='submit']")
        try:
            searchbtn5[-1].click()
        except:
            searchbtn5[0].click()
        sleepBar(1)
    elif deleteMethod == 2:
        # 删除方法2: backspace删除
        for _ in range(len(query)+1):
            inputbox.send_keys(Keys.BACK_SPACE)
            time.sleep(0.1)
        sleepBar(1)


def checkError(browser):
    if browser.find_elements_by_xpath("//div[@style='display: block;']"):
        return True
    else:
        return False


def checkEnd(browser):
    end = False
    if browser.find_elements_by_xpath("//div[@class='pagination']//li[@class='disabled']/a[text()='Next']"):
        end = True
    else:
        nextbtn = browser.find_elements_by_xpath("//div[@class='pagination']//li/a[text()='Next']")
        nextbtn[0].click()
        sleepBar(2)
    return browser, end


def extraction(browser):
    page = BeautifulSoup(browser.page_source, "lxml")
    # 锁定范围
    results_grid = page.find(name="div", attrs={"class": "results-grid"})
    grid_canvas = results_grid.find(name="div", attrs={"class": "grid-canvas"})
    # 抓取此页中每个店铺的信息条
    infoLines = grid_canvas.find_all(name="div", attrs={"class": re.compile("ui-widget-content")})
    # 提取信息条中的信息
    itemsInfos = []
    for line in infoLines:
        itemInfo = []
        infospaces = line.find_all(name="div")
        for infospace in infospaces:
            itemInfo.append(infospace.get_text())
        itemsInfos.append(itemInfo)
    return itemsInfos


if __name__ == "__main__":
    # Input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-Q", "--query", help="query in search engine", type=str)
    parser.add_argument("-R", "--region", help="region in search engine", type=str, default="")
    parser.add_argument("-L", "--locality", help="locality in search engine", type=str, default="")
    parser.add_argument("-F", "--keywordFile", help="the file of inputs in search engine", type=str)
    parser.add_argument("-H", "--headless", help="If needed headless, -H is \"True\"", type=str)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    email= "xxx@yyy.com"
    password = "xxx"

    dirname = "./save"
    pageLimitation = -1
    start = 3861
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # 设置是否需要打开chrome(headless为chrome无界面状态)
    if args.query or args.keywordFile:
        if args.headless:
            browser = initBrowser(True)
        else:
            browser = initBrowser()

        if args.query:
            query = args.query
            region = args.region
            locality = args.locality
            queries = [[query, region, locality]]
            savedFilename = " ".join(queries[0])
        elif args.keywordFile:
            with open(args.keywordFile, "r") as f:
                queries = []
                for i in f.readlines():
                    one_query = []
                    elements = i.strip().split(";;")
                    one_query.append(elements[0].strip())
                    if len(elements) > 1:
                        for j in elements[-1].strip().split(","):
                            one_query.append(j.strip())
                    else:
                        one_query.append("") # region 为空
                        one_query.append("") # locality 为空
                    queries.append(one_query)

                query = queries[0]
                savedFilename = ".".join(os.path.basename(args.keywordFile).split(".")[:-1])

        filename = os.path.join(dirname, prettyOutputName(savedFilename, 'txt'))
        kg_panelFile = open(filename, "w", encoding="utf8")

        browser = newSearch(browser, email, password)
        for index, q_combination in enumerate(queries):
            # 设置爬去的起始位置
            if index < start:
                continue

            print("\n************")
            print("No. %d: %s" % (index, quote(q_combination[0])))
            print("************\n")
            infos = searchItems(browser, q_combination, pageLimitation)

            for item in infos:
                item.append(str(q_combination))
                kg_panelFile.write(str(item) + "\n")

            print("Total visiting count: %d" % total_visit_num)
            if total_visit_num % 200 == 0:
                time.sleep(120)

        browser.close()


    
