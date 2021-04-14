# usual selenium imports
# Automation software
import os
import time

from selenium import webdriver
# hiding chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from webdriver_manager.chrome import ChromeDriverManager


def Check(dopuser, doppass, lists, debates):

    lists = lists

    debates = debates.split(",")
    l = []
    leng = lists.split(",")
# hider opt
    #driver_exe = 'chromedriver'
    options = Options()

    options.add_argument("--headless")

    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-sh-usage")
    options.add_argument("--no-sandbox")
# include options  options=options  executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=options)
    driver.get("https://dopagent.indiapost.gov.in/")
    driver.find_element_by_name(
        "AuthenticationFG.USER_PRINCIPAL").send_keys(dopuser)
    driver.find_element_by_name(
        "AuthenticationFG.ACCESS_CODE").send_keys(doppass)

    driver.find_element_by_name(
        "Action.VALIDATE_RM_PLUS_CREDENTIALS_CATCHA_DISABLED").click()
    # check password
    # driver.find_element_by_id("PasswordChangeFG.SIGNON_PWD")
    try:
        driver.find_element_by_id("PasswordChangeFG.SIGNON_PWD")
        return 'Change password in website'
    except:
        print("continue")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Accounts")))

    element.click()
    element2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Agent Enquire & Update Screen")))
    element2.click()
    driver.find_element_by_name(
        "CustomAgentRDAccountFG.PAY_MODE_SELECTED_FOR_TRN").click()
    driver.find_element_by_name(
        "CustomAgentRDAccountFG.ACCOUNT_NUMBER_FOR_SEARCH").send_keys(lists)

    driver.find_element_by_name("Action.FETCH_INPUT_ACCOUNT").click()

    if(len(leng) <= 10):
        for i in range(len(leng)):
            driver.find_element_by_name(
                "CustomAgentRDAccountFG.SELECT_INDEX_ARRAY["+str(i)+"]").click()

    elif(len(leng) > 10):
        s = len(leng)
        for _ in range(s//10):
            l.append(10)
        if(s % 10 != 0):
            l.append(s % 10)
    # print(l)
    for i in range(len(l)):
        # print(i)
        for j in range(l[i]):
            # print(j)
            driver.find_element_by_name(
                "CustomAgentRDAccountFG.SELECT_INDEX_ARRAY["+str(i*10+j)+"]").click()
            if((j+1) % 10 == 0):
                driver.find_element_by_name(
                    "Action.AgentRDActSummaryAllListing.GOTO_NEXT__").click()


# Next page integration tick
# After save
    driver.find_element_by_name("Action.SAVE_ACCOUNTS").click()
# wait until load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "PAY_ALL_SAVED_INSTALLMENTS")))

# Finding Radiobutton in range of debts,iterate next page then perform 3 steps

    if(len(leng) <= 10):
        for i in range(len(leng)):
            if(int(debates[i]) > 1):
                print(i)
                driver.find_element_by_xpath(
                    "//input[@value="+str(i)+"]").click()
                driver.find_element_by_name(
                    "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").clear()
                driver.find_element_by_name(
                    "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").send_keys(str(debates[i]))
            # click on save
                driver.find_element_by_name("Action.ADD_TO_LIST").click()
                time.sleep(2)

            # driver.find_element_by_name("CustomAgentRDAccountFG.SELECT_INDEX_ARRAY["+str(i)+"]").click()
    elif(len(leng) > 10):
        for i in range(len(debates)):
            if(int(debates[i]) > 1):
                # print(i)
                if(i//10 == 0):
                    driver.find_element_by_xpath(
                        "//input[@value="+str(i)+"]").click()
                    driver.find_element_by_name(
                        "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").clear()
                    driver.find_element_by_name(
                        "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").send_keys(str(debates[i]))
            # click on save
                    driver.find_element_by_name("Action.ADD_TO_LIST").click()
                    time.sleep(2)
                #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Accounts")))
                else:
                    #pg = i//10
                    driver.find_element_by_name(
                        "CustomAgentRDAccountFG.SelectedAgentRDActSummaryListing_REQUESTED_PAGE_NUMBER").send_keys(str((i//10)+1))
                    driver.find_element_by_name(
                        "Action.SelectedAgentRDActSummaryListing.GOTO_PAGE__").click()
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        "//input[@value="+str(i)+"]").click()
                    driver.find_element_by_name(
                        "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").clear()
                    driver.find_element_by_name(
                        "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").send_keys(str(debates[i]))
            # click on save
                    driver.find_element_by_name("Action.ADD_TO_LIST").click()
                #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Accounts")))


# ------------------
# driver.find_element_by_xpath("//input[@value='2']").click()
# driver.find_element_by_name("CustomAgentRDAccountFG.RD_INSTALLMENT_NO").clear()
# driver.find_element_by_name(
#     "CustomAgentRDAccountFG.RD_INSTALLMENT_NO").send_keys("2")
# # click on save34910
# driver.find_element_by_name("Action.ADD_TO_LIST").click()
    driver.find_element_by_name("Action.PAY_ALL_SAVED_INSTALLMENTS").click()
    driver.implicitly_wait(2)

    content = driver.find_element_by_css_selector('div.greenbg')

# print(content)
    st = content.text
    p = st.split(" ")
    print(content.text)
    bn = p[7:8][0][:10]
    print(p[7:8][0][:10])

    driver.quit()
    return bn


if __name__ == "__main__":
    try:
        l = []
        k = ''
        j = ''
        h = int(input('Range : '))
#p = []
        for _ in range(h):
            y = input('Accnum : ')
            g = input('Debate : ')
            l.append([y, g])
        new_list = sorted(l, key=lambda x: x[0])
        print(new_list)
        for n in range(len(new_list)):
            k = k+str(new_list[n][0])+','
            j = j+str(new_list[n][1])+','

        print(k[:-1])
        print(j[:-1])
        # listnumbers =
    #listnumbers = input('Enter Account numbers : ')
    #debateslist = input('Enter Debates  : ')
        print(Check("DOP.MI5152310100002", "siripost@123", k[: -1], j[: -1]))
    except:
        print("Something Error occured")


# printpreview
# HREF_CustomAgentRDAccountFG.ACCOUNT_NUMBER_ALL_ARRAY[1]
