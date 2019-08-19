import requests
from bs4 import BeautifulSoup, Tag	
from urllib.parse import urlparse
import os

cwd = os.path.dirname(os.path.abspath(__file__))
bad_domains = ["youtube.com", ":///", "vimeo.com", "reddit.com", "twitter.com", "youtu.be"]
fc_agencies = ["snopes.com", "emergent.info", "politifact.com", "factcheck.org"]
base_urls = {"factcheck":"https://www.factcheck.org/fake-news/","snopes":"https://www.snopes.com/fact-check/page/2/", "politifact":"http://www.politifact.com/truth-o-meter/statements/"}
infofile = cwd+"/infofile.txt"

def logError(url, error, logfile):
	print(error)
	with open(cwd+"/"+logfile+"/logfile.txt","r+") as log:
		lines = log.readlines()
	for line in lines:
		if url not in line:
			with open(cwd+"/"+logfile+"/logfile.txt","a+") as log:
				log.write(error+url+"\n")

def getOnlyText(root):
	if root.string != None:
		return root.string
	else:
		return ''.join([getOnlyText(e) for e in root.contents])		

def check_status(url):
	r = requests.get(url)
	print(r.status_code)

def fix_source(page,source_elems, meta = None):
	for elem in source_elems:
		source_url = elem['href']
		if meta is not None:
			meta_date = meta.split(",")[-2][1:-2]
			source_text = elem.text
			if meta_date not in source_text:
				continue
		if source_url is not None:
			parsed_url = urlparse(source_url)
			source_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
			if sum([1 for e in fc_agencies if e in source_domain]) > 0:
				continue
			elif sum([1 for e in bad_domains if e in source_url]) > 0:
				continue
			elif ("facebook.com" in source_domain):
				if ("/videos/" in source_url) or ("/photos/" in source_url):
					continue
			elif ("archive" in source_domain):
				return (source_url.replace("/image",""),source_domain)
			elif (check_status(source_url) == 200):
					return (source_url,source_domain)
	return (None, None)

def update_last_saved_page(idx, page_num,agency):
	with open(infofile, "r+") as f:
		lines = f.readlines()
		
	lines[idx] = agency+": "+str(page_num)+"\n" 
	a = "".join(lines)
	# SAVE PROGRESS PAGE
	with open(infofile, "w+") as f:
		f.write(a)

def get_last_saved_page(agency):
	with open(infofile, "r+") as f:
		lines = f.readlines()
		for idx,line in enumerate(lines):
			if agency+": " in line:
				return(idx,int(line.split(" ")[1]))	

def get_num_of_pages(agency):
	base_url = base_urls[agency]
	req = requests.get(base_url)
	soup = BeautifulSoup(req.text,"html.parser")
	if agency == "snopes":
		pages = soup.find("span",{"class":"page-count"}).text.split(" ")[-1]
	elif agency == "factcheck":
		pagination = soup.find("ul",{"class":"pagination"})
		last_child = pagination.find_all(recursive=False)[-1]
		pages = last_child.a['href'].split("/")[-2]
	elif agency == "politifact":
		pages = soup.find("span",{"class":"step-links__current"}).text.split()[-1]	
	return int(pages)			

def getVerdict(text):
	answer = ''.join(text.split("A:")[1:]).strip(" ")
	verdict = answer.split(".")[0][:3]
	print(answer)
	if "No" in verdict:
		return "false" 
	elif "Yes" in verdict:
		return "true" 
	else:
		return "unverified"

def getSources(content):
	sources = []
	f_source = 0
	p_list = (i for i in content.contents[1:-1] if isinstance(i,Tag))
	
	for p in p_list:
		text = getOnlyText(p)
		if (f_source == 1):
			source_elem = p.find("a")
			if (source_elem != None) and (source_elem.has_attr('href')):
				sources.append(source_elem)
		if "sources" == text.lower():
			f_source = 1
	return sources