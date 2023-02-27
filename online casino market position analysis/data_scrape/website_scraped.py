from bs4 import BeautifulSoup
import urllib
import urllib.request as ur
import pandas as pd
from datetime import datetime
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ngrams
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
import nltk
from urllib.request import Request, urlopen
import random
import matplotlib.pyplot as plt

df = pd.read_csv ('Online Gambling Sites.csv')

# clean the data
del df[df.columns[0]]
df = df.drop(['Crypto Currencies', 'Community','~AutoDice speed (~10 sec)'], axis=1)
df = df.replace('?',0).dropna()

# clean global rank and sort

df = df.loc[df['Global Rank'] != '-']
df['Global Rank'] = df['Global Rank'].astype(int) 
df = df.loc[df['Global Rank'] < 10000].sort_values(by=['Global Rank'])

# clean misdecoded numbers and convert strings to ints
df[df.columns[5:17]] = df[df.columns[5:17]].replace({"\xa0":"", " ": ""}, regex=True).astype(int)

# set companyname asindex
# haha = df['Link'].str.split('.')[0]
df['Company'] = df['Link'].str.split('.').str[0]
df = df.drop('Link', axis=1).set_index('Company')

df['Global Rank']

# plot month change 
df_mc = df[df.columns[-1]].replace({",":".", "%": ""}, regex=True).astype(float).T
df_mc.plot.bar()
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.show()

# plot volume trends
df_vt = df.drop(df.columns[0:4], axis = 1).drop(df.columns[-1], axis = 1).T

df_vt.plot.line()
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.show()

# Calculate corelation between global rank and volume

# clean
df_rv = df.drop(df.columns[0:3], axis = 1).drop(df.columns[-1], axis = 1)
df_rv['Mean'] = df_rv[df_rv.columns[1:-1]].mean(axis=1).astype(float)
df_rv = df_rv.drop(df_rv.columns[1:-1], axis = 1)

# calculate
cor = df_rv['Global Rank'].corr(df_rv['Mean']).astype(str)
print('The corelation between Global Rank and Mean of website visit is '+ cor )