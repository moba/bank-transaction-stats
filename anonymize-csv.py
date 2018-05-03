#!/usr/bin/python
#  hacked together by Moritz Bartl
#  licensed under MIT

import csv
from datetime import datetime
from collections import OrderedDict, Counter
from sys import argv
import re
import numpy

MT940_DATE_FIELD = "Buchungstag"
MT940_AMOUNT_FIELD = "Betrag"
MT940_SOURCE_ACCOUNT = "Kontonummer"
AQ_DATE_FIELD = "date"
AQ_AMOUNT_FIELD = "value_value"
AQ_SOURCE_ACCOUNT = "remoteIban"

###########################################################

# parse command line
csvfiles = set()
try:
    for i in range(1, len(argv)):
        csv_filename = argv[i]
        csvfiles.add(open(csv_filename, 'rb'))
        # yes, binary mode is correct as per csv.reader documentation
except Exception:
    print argv[0] + ' transactions.csv [transactions2.csv...] [startbalance]'
    exit(2)


transactions = []

CONTAINS_DIGIT = re.compile(r'\d')

# import csv
for csvfile in csvfiles:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        # ok, on every line we try to parse as aqbanking CSV first
        # this could be optimized
        try:
            transaction_date = datetime.strptime(row[AQ_DATE_FIELD], '%Y/%m/%d').date()
        except Exception:
            transaction_date = datetime.strptime(row[MT940_DATE_FIELD], '%d.%m.%y').date()
            amount = float(row[MT940_AMOUNT_FIELD].replace(',', '.'))
            country = row[MT940_SOURCE_ACCOUNT][0:2]
        else:
            amount = float(row[AQ_AMOUNT_FIELD].replace('/100', '')) / 100
            country = row[AQ_SOURCE_ACCOUNT][0:2]

        # if extracted country code contains numbers or is empty,
        # source country is unknown
        if ((CONTAINS_DIGIT.search(country)) or (not country)):
            country = "?"

        transactions.append([transaction_date.strftime("%d.%m.%y"), str(amount), country])
    csvfile.close()

for transaction in transactions:
    print ",".join(transaction)
