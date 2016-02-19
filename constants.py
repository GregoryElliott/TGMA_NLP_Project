import json

with open('gg2013.json') as data_2013:
    db2013 = json.load(data_2013)

with open('gg2015.json') as data_2015:
    db2015 = json.load(data_2015)

TPM_THRESHOLD = 1000
