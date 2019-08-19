import os
import pandas as pd
import math
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

header = ["page", "claim", "claim_label", "tags", "claim_source_domain", "claim_source_url", "date_check", "source_body", "date_fake"]
header2 = ["page", "claim", "claim_label", "tags", "claim_source_domain", "claim_source_url", "date_check", "source_body", "date_fake", "label"]

cwd = os.getcwd()

results = pd.read_csv(cwd+"/results.csv", sep="\t")
dataset = pd.read_csv(cwd+"/dataset.csv", sep="\t")

# snopes = pd.DataFrame(columns=header2)
# emergent = pd.DataFrame(columns=header2)
# politifact = pd.DataFrame(columns=header2)
# factcheck = pd.DataFrame(columns=header2)

# for e in dataset.iterrows():
# 	if "snopes" in e[1][0]:
# 		snopes.loc[e[0]] = e[1]
# 	elif "emergent" in e[1][0]:
# 		emergent.loc[e[0]] = e[1]
# 	elif "politifact" in e[1][0]:
# 		politifact.loc[e[0]] = e[1]
# 	elif "factcheck" in e[1][0]:
# 		factcheck.loc[e[0]] = e[1]

# ack_s = [1 for e in snopes.iterrows() if isinstance(e[1][8], str)]
# ack_e = [1 for e in emergent.iterrows() if isinstance(e[1][8], str)]
# ack_p = [1 for e in politifact.iterrows() if isinstance(e[1][8], str)]
# ack_f = [1 for e in factcheck.iterrows() if isinstance(e[1][8], str)]

# print("snopes:",sum(ack_s),len(snopes))
# print("emergent:",sum(ack_e),len(emergent))
# print("politifact:",sum(ack_p),len(politifact))
# print("factcheck:",sum(ack_f),len(factcheck))

# for e in results.iterrows():
# 	elem = e[1]
# 	if elem['label'] == 0:
# 		# if "not found" in elem['source_body']:
# 		print(elem['claim_source_url'])

def check_status(url):
	r = requests.get(url)
	return(r.status_code)


url = 'http://readconservatives.news/2017/02/24/trump-signed-executive-order-prevents-illegals-using-welfare-support/'
url2 = 'https://www.gop.gov/policy-news/09/09/22/aarp-helping-seniors-or-helping'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--dns-prefetch-disable")	
chrome_options.add_argument("--window-size=1920x1080")
chrome_driver = os.getcwd() +"/chromedriver"

browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

browser.get(url)
source_body = browser.page_source
current_url = browser.current_url

if check_status(url2) == 404:
	print('asda')