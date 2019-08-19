import os
import pandas as pd

header = ["page", "claim", "claim_label", "tags", "claim_source_domain", "claim_source_url", "date_check", "source_body", "date_fake"]

cwd = os.getcwd()

# data = pd.read_csv(cwd+"/datasetSeleniumOnly.csv", sep="\t")
emergent = pd.read_csv(cwd+"/datasets/emergent_content.csv", sep="\t")
politifact = pd.read_csv(cwd+"/datasets/politifact_content.csv", sep="\t")
snopes = pd.read_csv(cwd+"/datasets/snopes_content.csv", sep="\t")
factcheck = pd.read_csv(cwd+"/datasets/factcheck_content.csv", sep="\t")

emergent.drop_duplicates(inplace=True)
politifact.drop_duplicates(inplace=True)
snopes.drop_duplicates(inplace=True)
factcheck.drop_duplicates(inplace=True)

emergent = emergent.loc[emergent['source_body'].notnull()]
politifact = politifact.loc[politifact['source_body'].notnull()]
snopes = snopes.loc[snopes['source_body'].notnull()]
factcheck = factcheck.loc[factcheck['source_body'].notnull()]

print(len(emergent))
print(len(politifact))
print(len(snopes))
print(len(factcheck))

datasets = [emergent, politifact, snopes, factcheck]

dataset = pd.concat(datasets)



dataset.to_csv(cwd+'/dataset.csv', sep='\t', header=header, index=False)

# dataset = pd.concat(datasets)

# emergent = emergent.sample(frac=1)
# politifact = politifact.sample(frac=1)
# snopes = snopes.sample(frac=1)
# factcheck = factcheck.sample(frac=1)

# emergent = emergent.head(11)
# politifact = politifact.head(145)
# snopes = snopes.sample(188)
# factcheck = factcheck.sample(9)

# samples = [emergent, politifact, snopes, factcheck]

# sample = pd.concat(samples)
# sample.to_csv(cwd+'/sample.csv', sep='\t', header=header, index=False)
# print(len(sample))