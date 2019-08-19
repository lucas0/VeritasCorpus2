import os, sys
import tkinter as tk
from tkinterhtml import HtmlFrame
import webbrowser
import pandas as pd
	
root = tk.Tk()

tb_col_size = 5
tb_row_size = 5
tb_h = 500
tb_w = 50

pos = 0
neg = 0

logbox = tk.Text(root, width=100, height=50)
logbox.config(highlightbackground="black")
logbox.grid(row=1, column=0, columnspan=10, rowspan=1)

samples = pd.read_csv('sample_s.csv',sep='\t')
results = pd.read_csv('results.csv',sep='\t')

pointer = -1

def writeResult(value):
	global pointer
	entry = samples.loc[pointer]
	n_entry = list(entry)
	n_entry.append(value)
	results = pd.read_csv('results.csv',sep='\t')
	results.loc[entry.page] = n_entry
	results.to_csv('results.csv',sep='\t',index=False)
	nextArticle()

def nextArticle():
	global pointer,logbox
	pointer += 1
	entry = samples.loc[pointer]
	print()
	if entry.page in results['page'].tolist():
		nextArticle()
		return

	webbrowser.open(new=1,url=entry.claim_source_url, autoraise=False)
	webbrowser.open(new=1,url=entry.page, autoraise=False)

	logbox.delete('1.0', "end")
	logbox.insert('1.0',entry.source_body+"\n")


buttonA = tk.Button(root, text="ACK", command=lambda: writeResult("1"))
buttonA.grid(row=0, column=0, sticky="N")

buttonN = tk.Button(root, text="NACK", command=lambda: writeResult("0"))
buttonN.grid(row=0, column=1, sticky="N")

buttonP = tk.Button(root, text="pACK", command=lambda: writeResult("2"))
buttonP.grid(row=0, column=2, sticky="N")


root.bind("1", lambda: writeResult("1"))
root.bind("2", lambda: writeResult("2"))
root.bind("0", lambda: writeResult("3"))

nextArticle()
root.mainloop()

