import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur
from datetime import date
import os
# import requests



# Enter a stock symbol
index= 'FLTR.L'
# URL link 
url_is = 'https://finance.yahoo.com/quote/' + index + '/financials?p=' + index
url_bs = 'https://finance.yahoo.com/quote/' + index +'/balance-sheet?p=' + index
url_cf = 'https://finance.yahoo.com/quote/' + index + '/cash-flow?p='+ index

req_is = ur.Request(url_is, headers={'User-Agent': 'Mozilla/5.0'})
read_data_is = ur.urlopen(req_is).read()
soup_is= BeautifulSoup(read_data_is,'html.parser')

req_bs = ur.Request(url_bs, headers={'User-Agent': 'Mozilla/5.0'})
read_data_bs = ur.urlopen(req_bs).read()
soup_bs= BeautifulSoup(read_data_bs,'html.parser')

req_cf = ur.Request(url_cf, headers={'User-Agent': 'Mozilla/5.0'})
read_data_cf = ur.urlopen(req_cf).read()
soup_cf= BeautifulSoup(read_data_cf,'html.parser')

# create directory
try:
   os.makedirs('pesudo_data/' + index)
except FileExistsError:
   # directory already exists
   pass


# Income Statement scrape

ls= [] # Create empty list
# print(soup_is)
for l in soup_is.findAll('div') or soup_is.findAll("div", {"class" : "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined"}):

    if l in soup_is.findAll("div", {"class" : "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined"}):    
        ls.append(l.span.text)
        
    else:
        ls.append(l.string) # add each element one by one to the list
new_ls = list(filter(None,ls))
new_ls = new_ls[new_ls.index("Quarterly")-1:]
del new_ls[1:3]
is_data = list(zip(*[iter(new_ls)]*new_ls.index("Total Revenue")))

Income_st = pd.DataFrame(is_data[0:])
Income_st.columns = Income_st.iloc[0] 
Income_st = Income_st.iloc[1:,].T 

Income_st.columns = Income_st.iloc[0] 
Income_st.drop(Income_st.index[0],inplace=True) 
Income_st.index.name = "" 
Income_st.rename(index={"ttm": date.today().strftime("%m/%d/%y")},inplace=True) 
Income_st = Income_st[Income_st.columns[:-5]]
Income_st.to_csv('pesudo_data/' + index +'/Income_st.csv')  


# Balance Sheet scrape

ls= [] # Create empty list
# print(soup_bs)
for l in soup_bs.findAll('div') or soup_bs.findAll("div", {"class" : "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined"}):

    if l in soup_bs.findAll("div", {"class" : "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined"}):    
        ls.append(l.span.text)
        
    else:
        ls.append(l.string) # add each element one by one to the list
new_ls = list(filter(None,ls))

new_ls = new_ls[new_ls.index("Quarterly")-1:]

del new_ls[1:3]

bs_data = list(zip(*[iter(new_ls)]*new_ls.index("Total Assets")))

balance_St = pd.DataFrame(bs_data[0:])

balance_St.columns = balance_St.iloc[0] 
balance_St = balance_St.iloc[1:,].T 

balance_St.columns = balance_St.iloc[0] 
balance_St.drop(balance_St.index[0],inplace=True) 
balance_St.index.name = "" 

balance_St.to_csv('pesudo_data/' + index +'/balance_St.csv')  


# Cash Flow scrape

ls= [] # Create empty list
# print(soup_bs)
for l in soup_cf.findAll('div') or soup_cf.findAll("div", {"class" : "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined"}):

    if l in soup_cf.findAll("div", {"class" : "D(ib) Va(m) Ell Mt(-3px) W(215px)--mv2 W(200px) undefined"}):    
        ls.append(l.span.text)
        
    else:
        ls.append(l.string) # add each element one by one to the list
new_ls = list(filter(None,ls))
new_ls = new_ls[new_ls.index("Quarterly")-1:]

del new_ls[1:3]

cf_data = list(zip(*[iter(new_ls)]*new_ls.index("Operating Cash Flow")))

cash_Fl = pd.DataFrame(cf_data[0:])

cash_Fl.columns = cash_Fl.iloc[0] 
cash_Fl = cash_Fl.iloc[1:,].T 

cash_Fl.columns = cash_Fl.iloc[0] 
cash_Fl.drop(cash_Fl.index[0],inplace=True) 
cash_Fl.index.name = "" 
cash_Fl.rename(index={"ttm": date.today().strftime("%m/%d/%y")},inplace=True) 
cash_Fl.to_csv('pesudo_data/' + index +'/cash_Fl.csv') 