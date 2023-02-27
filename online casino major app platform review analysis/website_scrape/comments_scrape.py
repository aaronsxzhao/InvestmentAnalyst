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

def comment_scrape(WEBSITE, Page):
    comments = []
    rates = []
    dates = []

    # type in the website you want to scrape and analyze the trends over time!!!!!
    # example WEBSITE = 'www.betfair.com'
    
    user_agents_list = [
            'Mozilla/5.0 (iPad; CPU OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_16_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
            'python-requests/3.10.0',
            'python-requests/2.14.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
        ]
    

    for page in range(1, Page):
        if page == 1:
            req = Request(
                    url='https://www.trustpilot.com/review/'+ WEBSITE, 
                    headers={'User-Agent': random.choice(user_agents_list)}
                )
#             url = ur.urlopen('https://www.trustpilot.com/review/'+ WEBSITE)

        else:
            req = Request(
                    url='https://www.trustpilot.com/review/'+ WEBSITE +'?page=' + str(page), 
                    headers={'User-Agent': random.choice(user_agents_list)}
                )
            
#             url = ur.urlopen('https://www.trustpilot.com/review/'+ WEBSITE +'?page=' + str(page))
            
        content = urlopen(req).read()
#         content = url.read()
        soup = BeautifulSoup(content, 'lxml')

        table_com_date = soup.findAll('div',attrs={"class":"styles_reviewContent__0Q2Tg"})
        table_rate = soup.findAll('div',attrs={"class":"styles_reviewHeader__iU9Px"})

        # scrape rates
        for x in table_rate:
            rates.append(x['data-service-review-rating'])

        # scrape comments and dates
        for x in table_com_date:

            comments.append(x.find('p').text)
            date = x.find('p', attrs = {"class": "typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn"}).text[20:]
            date = datetime.strptime(date , "%B %d, %Y")
            dates.append(date)
        
    d = {'Review': comments, 'Rate': rates,'Date': dates }
    df = pd.DataFrame(d)
    df = df.set_index(['Date'])
    
    # print ratio
    print('Rate counts shows below:')
    print(df['Rate'].value_counts())
    print('\nRate counts ratio shows below:')
    print(df.Rate.value_counts(normalize=True))
    
    print('\nReview groupby year shows below:')
    print(df.groupby(df.index.year)['Review'].count())
    
    print('\nScraped ' + str(len(df)) + ' reviews of ' + WEBSITE)
    
    return df

def trends_analyze(filename, Rate, Date):
    
    # read
    df = pd.read_csv (filename, lineterminator='\n')

    # joins all the sentenses
    df['Review'] = [df['Review'].iloc[i].replace("\r", " ") for i in range(len(df['Review']))]
    df['Date'] = [datetime.strptime(df['Date'].iloc[i], "%Y-%m-%d") for i in range(len(df['Review']))]
    df = df.set_index(['Date'])
    df = df.loc[df['Rate'] == Rate].loc[Date]
    
    sentence = " ".join(df['Review'])
    # creates tokens, creates lower class, removes numbers and lemmatizes the words
    new_tokens = word_tokenize(sentence)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]

    # #counts the words, pairs and trigrams
    counted = Counter(new_tokens)
    counted_2= Counter(ngrams(new_tokens,2))
    counted_3= Counter(ngrams(new_tokens,3))

    # #creates 3 data frames and returns thems
    word_freq = pd.DataFrame(counted.items(),columns=['word','frequency']).sort_values(by='frequency',ascending=False)
    word_pairs =pd.DataFrame(counted_2.items(),columns=['pairs','frequency']).sort_values(by='frequency',ascending=False)
    trigrams =pd.DataFrame(counted_3.items(),columns=['trigrams','frequency']).sort_values(by='frequency',ascending=False)
    
    return word_freq, word_pairs, trigrams
    
def plot_chart(word_freq, word_pairs, trigrams):
    # create subplot of the different data frames
    fig, axes = plt.subplots(3,1,figsize=(9,15))
    sns.barplot(ax=axes[0],x='frequency',y='word',data=word_freq.head(30))
    sns.barplot(ax=axes[1],x='frequency',y='pairs',data=word_pairs.head(30))
    sns.barplot(ax=axes[2],x='frequency',y='trigrams',data=trigrams.head(30))
    
    return 

def review_star_split(df):
    df['Rate'] = df['Rate'].astype(float)
    
    fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(9, 4))

    df['Rate'].plot(kind='hist', edgecolor='black',ax=axes[0])
    axes[0].set_title("Review Star Distribution")
    
    df = df.groupby([df.index.year, "Rate"]).count()
    df = df.groupby(level=0, group_keys=False).apply(lambda x:100 * x / float(x.sum()))
    df.unstack().plot(kind='bar', stacked=True, ax=axes[1])
    
    axes[1].set_title("Review Star Percentage over Time")
    axes[1].legend(title="")
    plt.show()
    return

def review_volume_trend(df):
    df['Rate'] = df['Rate'].astype(float)
    
    fig = plt.figsize=(6, 6)
    df = df.groupby(df.index.year).count().pop('Review')
    df.plot(kind='bar', stacked=True)
    plt.title("Review Volume Trend")
    plt.show()

    return

def review_pie_chart(df):
    
    df['Rate'] = df['Rate'].astype(float)
    
    fig, axes = plt.subplots(nrows=3, ncols=4,figsize=(12, 9))
    
    number_group = df.groupby(df.index.year).ngroups
    
    df = df.groupby([df.index.year, "Rate"]).count()
    df = df.groupby(level=0, group_keys=False).apply(lambda x:100 * x / float(x.sum()))

    
    for i, e in enumerate(df.index.levels[0]):
        yy = df.loc[e]["Review"].tolist()

        axes[i//4 , i%4].pie(yy,  autopct='%1.1f%%', shadow=True, startangle=90)
        axes[i//4 , i%4].set_title(e)
        
    plt.show()
    
    return

# Single Company (1)

WEBSITE = 'williamhill.com'
Page = 150
df = comment_scrape(WEBSITE, Page)
df.to_csv('review.csv')

# Single Company (2)
filename = 'review.csv'

Rate = 1
Date = '2020'

word_freq, word_pairs, trigrams = trends_analyze(filename, Rate, Date)
plot_chart(word_freq, word_pairs, trigrams)

# Multi Company (1)
WEBSITE = ['www.888.com', 'www.ladbrokes.com', 'www.skybet.com', 'www.paddypower.com', 'williamhill.com']
Page = [30, 113, 73, 106, 197]

df_bag = pd.DataFrame()

for i in range(len(WEBSITE)):
    
    df = comment_scrape(WEBSITE[i], Page[i])
    df_bag = pd.concat([df_bag, df])
    
df_bag.to_csv('review.csv')

# Multi Company (2)
filename = 'review.csv'

Rate = 5
Date = '2012'

word_freq, word_pairs, trigrams = trends_analyze(filename, Rate, Date)
plot_chart(word_freq, word_pairs, trigrams)

# review star split percentage

review_star_split(df_bag)

# review volume trend

review_volume_trend(df_bag)

# pie chart of reviews

review_pie_chart(df_bag)