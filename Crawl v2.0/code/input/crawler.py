import time
import os
from bs4 import BeautifulSoup as bs
import requests
import subprocess
import re

cwd2 = os.getcwd()

while True:
	subprocess.call(["python3",cwd2+"/emergent/c_emergent.py"])
	print("done with emergent")

	subprocess.call(["python3",cwd2+"/snopes/c_snopes.py"])
	print("done with snopes")

	subprocess.call(["python3",cwd2+"/factcheck/c_factcheck.py"])
	print("done with factcheck")

	subprocess.call(["python3",cwd2+"/politifact/c_politifact.py"])
	print("done with politifact")

	time.sleep(300)