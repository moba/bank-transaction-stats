#!/usr/bin/python
# bank-transaction-stats.py
#  reads a CSV file from bank and prints out some statistics
#  of the transactions
#
#  likely only works for German Sparkasse CSV-MT940 files but
#  is pretty straightforward to adapt
#
##
#  hacked together by Moritz Bartl
#  licensed under MIT

import csv
from datetime import date, datetime
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
        try:
            csvfiles.add(open(csv_filename, 'rb')) # yes, binary mode is correct as per csv.reader documentation
        except:
            break
    try:
        start_balance = float(argv[-1])
    except:
        start_balance = 0
except:
    print argv[0] + ' transactions.csv [transactions2.csv...] [startbalance]'
    exit(2)

# prepare dictionary for transactions
class Transactions(dict):
    def __missing__(self, key):
        return list()
transactions = Transactions()
countries = Counter()

CONTAINS_DIGIT = re.compile('\d')

# import csv
for csvfile in csvfiles:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
	# ok, on every line we try to parse as aqbanking CSV first
	# this could be optimized
	try:
	        date = datetime.strptime(row[AQ_DATE_FIELD], '%Y/%m/%d').date()
	except:
        	date = datetime.strptime(row[MT940_DATE_FIELD], '%d.%m.%y').date()
        	amount = float(row[MT940_AMOUNT_FIELD].replace(',','.'))
		country = row[MT940_SOURCE_ACCOUNT][0:2]
	else:
                amount = float(row[AQ_AMOUNT_FIELD].replace('/100',''))/100
                country = row[AQ_SOURCE_ACCOUNT][0:2]

        # if extracted country code contains numbers or is empty, source country is unknown
        if ( (CONTAINS_DIGIT.search(country)) or (not country) ):
            country = "?"

        transactions[date] = transactions[date]+[amount]
        countries[country] = countries[country]+1
    csvfile.close()

transactions = OrderedDict(sorted(transactions.items())) # sort chronologically

amounts = [num for elem in transactions.values() for num in elem]
deposits = [num for num in amounts if num > 0]

first_day = transactions.keys()[0]
last_day  = transactions.keys()[-1]

# print overview
print "From {} to {}".format(first_day,last_day)
print ""
print "Start balance: %.2f" % float(start_balance)
print "End balance: %.2f" % float(sum(amounts)+start_balance)
print ""
print "Total number of transactions: " + str(len(amounts))
print "Mean amount (deposits only): %.2f" % float(sum(deposits)/max(len(deposits),1))
print "Median (deposits only): %.2f" % float(numpy.median(deposits))

# print daily summary
print ""
print "date       |      total | number of transactions "
print "-"*45

for date in transactions:
    daily_total = transactions[date]
    print "{:<10} | {:>10} | {} ({})".format(date.strftime('%d.%m.%y') , sum(daily_total), '*'*len(daily_total), len(daily_total))

print "-"*45
print ""

# print number of occurrences per amount

amount_counter = Counter(amounts)

print ""
print "amount     | count | as bar"
print "-"*45

for amount, count in sorted(amount_counter.items()):
    print "{:<10} | {:<5} | {}".format(amount, count, '#'*count)

print "-"*45

# print distribution of source countries
print ""
print "country | number of transactions"
print "-" * 33
for country in countries:
    print "{:<2}      | {}".format(country, countries[country])
print "-" * 33
