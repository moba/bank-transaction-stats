# bank-transaction-stats.py

This is a script that I use to generate statistics over CSV files exported from a bank account at a German Sparkasse bank that I don't have EBICS/HBCI access to, and for CSV exports from [aqbanking](https://www.aquamaniac.de/sites/aqbanking/) ("full" profile).

The script first tries to parse the CSV using the aqbanking format, and then falls back to the variant of "CSV-MT940" used by that German Sparkasse. It relies on some named headers, and, since Sparkasse exports the amount with German currency divider (10,00€ instead of 10.00€), it will very likely need some adaptation for different banks and different currencies even if they use the same "CSV format".

Patches that add support for more banks/formats welcome.
https://github.com/moba/bank-transaction-stats

## output/usage example
(no this is not real data)

```
❯ ./bank-transaction-stats.py transactions-*.csv 2140.20
From 2016-01-04 to 2016-04-18

Start balance: 2140.20
End balance: 7526.65

Total number of transactions: 79
Mean amount: 68.18

date       |      total | number of transactions 
---------------------------------------------
04.01.16   |     2442.5 | *************** (15)
05.01.16   |     537.31 | *********** (11)
07.01.16   |     393.12 | ******** (8)
08.01.16   |       35.0 | ** (2)
11.01.16   |      115.0 | **** (4)
12.01.16   |      382.5 | **** (4)
13.01.16   |       65.0 | ** (2)
15.01.16   |       35.0 | ** (2)
18.01.16   |       50.0 | * (1)
19.01.16   |       20.0 | * (1)
22.01.16   |       50.0 | * (1)
26.01.16   |      575.0 | **** (4)
27.01.16   |     101.72 | ** (2)
29.01.16   |      100.0 | * (1)
10.02.16   |       80.0 | * (1)
11.02.16   |       10.0 | * (1)
15.02.16   |       10.0 | * (1)
17.02.16   |      105.0 | ** (2)
01.03.16   |      106.8 | **** (4)
07.03.16   |       30.0 | *** (3)
08.03.16   |      105.0 | ** (2)
01.04.16   |        2.5 | * (1)
04.04.16   |       10.0 | ** (2)
05.04.16   |        5.0 | * (1)
07.04.16   |        5.0 | * (1)
15.04.16   |       10.0 | * (1)
18.04.16   |        5.0 | * (1)
---------------------------------------------

amount     | count | as bar
---------------------------------------------
52.0       | 1     | #
55.0       | 1     | #
60.0       | 4     | ####
70.0       | 1     | #
73.81      | 1     | #
75.0       | 11    | ###########
80.0       | 2     | ##
91.72      | 1     | #
100.0      | 36    | ####################################
120.0      | 1     | #
130.0      | 1     | #
134.12     | 1     | #
150.0      | 2     | ##
200.0      | 12    | ############
250.0      | 1     | #
256.0      | 1     | #
300.0      | 2     | ##
---------------------------------------------

country   | number of transactions
---------------------------------
BE        | 1
CH        | 5
NL        | 3
DE        | 55
IT        | 2
AT        | 5
FI        | 1
ES        | 2
?         | 5
---------------------------------
```

## Licensed under MIT

```
Moritz Bartl (c) 2016-2017

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
