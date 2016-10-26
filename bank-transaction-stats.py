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
from collections import OrderedDict
from sys import argv

DATE_FIELD = "Buchungstag"
AMOUNT_FIELD = "Betrag"
SOURCE_ACCOUNT = "Kontonummer"

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
class Counter(dict):
    def __missing__(self,key):
        return 0
transactions = Transactions()
countries = Counter()

# import csv
for csvfile in csvfiles:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        date = datetime.strptime(row[DATE_FIELD], '%d.%m.%y').date()
        amount = float(row[AMOUNT_FIELD].replace(',','.'))
        transactions[date] = transactions[date]+[amount]

        country = row[SOURCE_ACCOUNT][0:2]
        countries[country] = countries[country]+1
    csvfile.close()

transactions = OrderedDict(sorted(transactions.items())) # sort chronologically

all_transactions = [num for elem in transactions.values() for num in elem]

first_day = transactions.keys()[0]
last_day  = transactions.keys()[-1]

print "From {} to {}".format(first_day,last_day)
print ""
print "Start balance: %.2f" % float(start_balance)
print "End balance: %.2f" % float(sum(all_transactions)+start_balance)
print ""
print "Total number of transactions: " + str(len(all_transactions))
print "Mean amount: %.2f" % float(sum(all_transactions)/max(len(all_transactions),1))
print ""
print "date     |   amount | number of transactions "
print "-"*45

for date in transactions:
    amounts = transactions[date]
    print "{} | {:>8} | {} ({})".format(date.strftime('%d.%m.%y') , sum(amounts), '*'*len(amounts), len(amounts))

print "-"*45

print ""
print "country | number of transactions"
print "-" * 33
for country in countries:
    print "{:<2}      | {}".format(country, countries[country])
print "-" * 33
print "(as you can see, source country detection is not perfect yet)"
