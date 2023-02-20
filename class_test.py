#  Python file that tests the effectiveness of classes and 
#  ability to access tokens in each class, such that when you
#  enter a word, it will output subcategories of a disease (in this test, arthirits)
#  that contain the input word

from __future__ import unicode_literals
import requests
import spacy
import nltk
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
#nltk.download('stopwords')      #only need to run once
from nltk.tokenize import word_tokenize
import textwrap
from numpy import dot
from numpy.linalg import norm
import math
import numpy as np
import en_core_web_sm
from numpy import dot
from numpy.linalg import norm
from tkinter import *

root = "https://www.webmd.com/"
link = "https://www.webmd.com/a-to-z-guides/health-topics"

# add additional stopwords
stop_words = stopwords.words('english')
stop_words.append(',')
stop_words.append('.')
stop_words.append('’')
stop_words.append('"')
stop_words.append('(')
stop_words.append(')')
stop_words.append(':')
stop_words.append(' ')
stop_words.append('\n')
stop_words.append('--')

dis_list = []   #array that holds all disease base classes

# define class Disease
class Disease:
    #'Common base class for all diseases'
    empCount = 0

    def __init__(self, name, link):
       self.name = name
       self.link = link
       self.subcategories = {}			# store subcategories in a dictionary
       Disease.empCount += 1

    def displayDisease(self):
       print ("Name : ", self.name,  ", Link: ", self.link)

    def add_subcategory(self, category, link):			# add a subcategory
       new_sub = Disease.Subcategory(category, link)
       self.subcategories[category] = new_sub
       return new_sub	
 
    def add_token_to_subcategory(self, category, token):	#add words to tokens in Subcategory
       sub = self.subcategories.get(category)
       if sub is not None:
          sub.add(token)
       else:
          raise Exception("No words found")

    class Subcategory:										# define inside class Subcategory
       def __init__ (self, category, link):
          self.category = category
          self.link = link
          self.tokens = []		# an array that holds tokens of words from a subcategory webpage

       def add(self, word):		# a function that does the adding to the tokens array
          self.tokens.append(word)
          
       def displaySubcategory(self):		# a function that does the adding to the tokens array
          print("Category: ", self.category, ", Link: ", self.link, ", Tokens: ", self.tokens  )

# set Arthirits to be the root website, for a smaller data set
matches_str = 'https://www.webmd.com/arthritis/default.htm'
req_2 = Request(matches_str, headers ={'User-Agent': 'Mozilla/5.0'})
webpage_2 = urlopen(req_2).read()
soup_2 = BeautifulSoup(webpage_2, 'html5lib')

top_searches = soup_2.find('div', attrs={'id': 'ContentPane34'})
# print(top_searches)
dis_name = Disease('arthritis', 'https://www.webmd.com/arthritis/default.htm')
dis_list.append(dis_name)

for items in top_searches:
   if soup_2.find_all('h3') is not None:    # h3 tag has "Top Searches"
   # looking for subcategory links
      links_2 = top_searches.find_all('a')  # locating the link with 'a' tags
      for each in links_2:
         type_ = str(each.get_text())
         link_2 = str(each.get('href'))
         dis_name.add_subcategory(type_, link_2)
         type_subcategory = dis_name.subcategories[type_]

         req_3 = Request(link_2, headers ={'User-Agent': 'Mozilla/5.0'})
         webpage_3 = urlopen(req_3).read()
         soup_3 = BeautifulSoup(webpage_3, 'html5lib')
         for item in soup_3.find_all("div", attrs={"class": "article__body"}):   # note: "article body" often changes, so update the code pls!
            content_ = item.find_all("p")
            content_ul = item.find_all("ul")
            sources = item.find_all("span")
            ads = item.find_all("strong")
            for y in ads:
               y.decompose()        # remove the ads
            for x in sources:
               x.decompose()        # remove sources
            for each in content_:
               content_text = (str(each.get_text().strip()))      
               text_tokens = word_tokenize(content_text)    # tokenize the paragraphs
               contents_wout_stopwords = [word for word in text_tokens if not word in stop_words]     # this removes stopwords like us, we, etc.   
               type_subcategory.add(contents_wout_stopwords)    # add this as a subcategory         


input_1 = input("Enter a word: ")   # prompt user to enter a single word
input_1 = input_1.casefold()

for sub in dis_name.subcategories:  # iterate over all subcategories
   flag = 0
   for x in range(len(dis_name.subcategories[sub].tokens)):
      if input_1 in dis_name.subcategories[sub].tokens[x] is not None:  # check if the input matches any word in tokens
         flag = 1          # set flag to 1 if its found
      if flag == 1:
         print(dis_name.subcategories[sub].link)      # if found, print the link and name of the subcategory
         print(dis_name.subcategories[sub].category)
         print("\n")
      flag = 0             # reset the flag to 0

