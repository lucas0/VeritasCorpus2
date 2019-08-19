import pandas as pd
import os

cwd = os.getcwd()



s1 = pd.read_csv(cwd+'/Snopes/results1.csv',sep='\t')
s2 = pd.read_csv(cwd+'/Snopes/results2.csv',sep='\t')
s3 = pd.read_csv(cwd+'/Snopes/results3.csv',sep='\t')
s4 = pd.read_csv(cwd+'/Snopes/results4.csv',sep='\t')
s5 = pd.read_csv(cwd+'/Snopes/results5.csv',sep='\t')


p1 = pd.read_csv(cwd+'/Politifact/results1.csv',sep='\t')
p2 = pd.read_csv(cwd+'/Politifact/results2.csv',sep='\t')
p3 = pd.read_csv(cwd+'/Politifact/results3.csv',sep='\t')
p4 = pd.read_csv(cwd+'/Politifact/results4.csv',sep='\t')
p5 = pd.read_csv(cwd+'/Politifact/results5.csv',sep='\t')


emergent = pd.read_csv(cwd+'/results_e.csv',sep='\t')
snopes = pd.concat([s1,s2,s3,s4,s5],ignore_index=True)
politifact = pd.concat([p1,p2,p3,p4,p5],ignore_index=True)

# print("Emergent",emergent.groupby('label').count())
# print("Snopes",snopes.groupby('label').count())
# print("Politifact",politifact.groupby('label').count())

e = emergent.loc[emergent['label'] == 1]
s = snopes.loc[snopes['label'] == 1]
p = politifact.loc[politifact['label'] == 1]

pos = pd.concat([e,s,p],ignore_index=True)

pos.loc[pos['claim_label'] == 'attribution-false', 'claim_label'] = 'false'
pos.loc[pos['claim_label'] == 'False', 'claim_label'] = 'false'
pos.loc[pos['claim_label'] == 'mostly true', 'claim_label'] = 'mtrue'
pos.loc[pos['claim_label'] == 'mostly false', 'claim_label'] = 'mfalse'
pos.loc[pos['claim_label'] == 'pants on fire!', 'claim_label'] = 'false'
pos.loc[pos['claim_label'] == 'half-true', 'claim_label'] = 'mtrue'
pos.loc[pos['claim_label'] == 'unproven', 'claim_label'] = 'unverified'

pos.drop(pos[pos.claim_label == 'no flip'].index, inplace=True)
pos.drop(pos[pos.claim_label == 'full flop'].index, inplace=True)
pos.drop(pos[pos.claim_label == 'miscaptioned'].index, inplace=True)

source_values = pd.Series(['emergent'] * len(e))
e = e.assign(data_source=source_values.values)
source_values = pd.Series(['snopes'] * len(s))
s = s.assign(data_source=source_values.values)
source_values = pd.Series(['politifact'] * len(p))
p = p.assign(data_source=source_values.values)

print(pos.groupby('claim_label').count())
print(len(pos))

pos.to_csv("pos_samples.csv",sep='\t', index=False)