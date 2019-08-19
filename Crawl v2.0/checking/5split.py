import pandas as pd

s = pd.read_csv("sample_p.csv",sep='\t')

d1 = s.iloc[:67]
d2 = s.iloc[67:134]
d3 = s.iloc[134:202]
d4 = s.iloc[202:269]
d5 = s.iloc[269:]

d1.to_csv("sample1.csv",sep='\t',index=False)
d2.to_csv("sample2.csv",sep='\t',index=False)
d3.to_csv("sample3.csv",sep='\t',index=False)
d4.to_csv("sample4.csv",sep='\t',index=False)
d5.to_csv("sample5.csv",sep='\t',index=False)
