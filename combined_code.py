#       This is the combined code that contains working web scraping, NLP,
#       and interfacing. Use this as the main file for overall implementation.

from __future__ import unicode_literals
import spacy
import nltk
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
# nltk.download('stopwords')                # only run this once
from nltk.tokenize import word_tokenize
import spacy
import textwrap
import math
import numpy as np
from numpy import dot
from numpy.linalg import norm
from tkinter import *

root = "https://www.webmd.com/"
link = "https://www.webmd.com/a-to-z-guides/health-topics"

print("------------------start----------------------")

# open the disease link
matches_str = 'https://www.webmd.com/arthritis/default.htm'   # replace this with "link" above
req_2 = Request(matches_str, headers ={'User-Agent': 'Mozilla/5.0'})
webpage_2 = urlopen(req_2).read()
soup_2 = BeautifulSoup(webpage_2, 'html5lib')   # apply Beautiful Soup to the webpage

top_searches = soup_2.find('div', attrs={'id': 'ContentPane34'})   # "Top Searches" contain subcategories needed to be parsed

content_text = []   # where words will be stored from a page

# web scraping section; note: right click on the webpage and click "Inspect"
for items in top_searches:
   if soup_2.find_all('h3') is not None:
      links_2 = top_searches.find_all('a')  # locating the link with 'a' tags
      for each in links_2:
         link_2 = str(each.get('href'))
         req_3 = Request(link_2, headers ={'User-Agent': 'Mozilla/5.0'})
         webpage_3 = urlopen(req_3).read()
         soup_3 = BeautifulSoup(webpage_3, 'html5lib')
         for item in soup_3.find_all("div", attrs={"class": "article__body"}):   # note: "article body" often changes, so update the code accordingly pls!
            content_ = item.find_all("p")
            content_ul = item.find_all("ul")
            sources = item.find_all("span")
            ads = item.find_all("strong")
            for y in ads:
               y.decompose()            # remove ads
            for x in sources:
               x.decompose()            # remove sources
            for each in content_:
               content_text.append((str(each.get_text())))  # extracting text from an article

# NLP functions
def distance2d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def meanv(coords):
    # assumes every item in coords has same length as item 0
    sumv = [0] * len(coords[0])
    for item in coords:
        for i in range(len(item)):
            sumv[i] += item[i]
    mean = [0] * len(sumv)
    for i in range(len(sumv)):
        mean[i] = float(sumv[i]) / len(coords)
    return mean

def distance(coord1, coord2):    # getting numeral distance between two words
    return math.sqrt(sum([(i - j)**2 for i, j in zip(coord1, coord2)]))

def closest(space, coord, n=10):   # find closest word to a given word
    closest = []
    for key in sorted(space.keys(),
        key=lambda x: distance(coord, space[x]))[:n]:
        closest.append(key)
    return closest

def vec(s):
    return nlp.vocab[s].vector

def cosine(v1, v2):
    if norm(v1) > 0 and norm(v2) > 0:
        return dot(v1, v2) / (norm(v1) * norm(v2))
    else:
        return 0.0

def spacy_closest(token_list, vec_to_check, n=10):   # find closest word using a pre-trained Spacy model
    return sorted(token_list,
                  key=lambda x: cosine(vec_to_check, vec(x)),
                  reverse=True)[:n]

list_str = ''.join(content_text)   # conver list type to a string type, bcos the nlp function only accepts string inputs or a txt. file

nlp = spacy.load('en_core_web_md') # this is the pre-trained English model in Spacy
doc = nlp(list_str)
tokens = list(set([w.text for w in doc if w.is_alpha]))  # tokens of words in the model

root = Tk()

root.geometry("450x400")        # size of the window
root.title("Welcome")

fn = StringVar()                # store input here

options = ["patient", "doctor", "student/researcher", "other"]      # replace this with actual results from spacy_closest
clicked = StringVar()
clicked.set("patient")          # replace this with one of the words in spacy_closest



drop = OptionMenu(root, clicked, *options).place(x=250, y=40)  # drop down menu
# drop.pack()
close_list = []

def print_input():          # print input in the terminal, just to make sure your interface is connected to ur code
    occu_input = fn.get()
    input1,input2 = occu_input.split()
    closest_words = spacy_closest(tokens, meanv([vec(input1), vec(input2)]))
    close_list.append(closest_words)
    print(closest_words)
    
def exit_window():          # enables the "cancel" button to exit the program
    exit()

def second_win():           # define second window
    window=Tk()
    window.title("welcome to the second window")
    window.geometry("500x500")
    options1 = ['pain', 'Pain', 'back', 'excruciating', 'painful', 'discomfort', 'tenderness', 'feel', 'suffering', 'knee'] 
    # replace the content of options1 with result of closest_words, but make sure they are in a list
    
    gn = StringVar()
    clicked1 = gn
    clicked1.set(options[0])
    drop1 = OptionMenu(window, clicked1, *options1).place(x=250, y=40)   # find a way to connect the dropdown menu to the code
    label2 = Label(window, text="Enter Words: ", width=20, font=("arial", 10, "bold")).place(x=120, y=125)
    entry2 = Entry(window,textvar=gn).place(x=250, y=125)
    button2_enter = Button(window, text="enter", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = gn.get()).place(x=200,y=200)
    button2_cancel = Button(window, text="cancel", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = exit_window).place(x=300,y=200)

# buttons and labels on the first window
button_enter = Button(root, text="enter", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = print_input).place(x=200,y=200)   # enter button
button_cancel = Button(root, text="cancel", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = exit_window).place(x=300,y=200) # cancel button
button_next = Button(root, text="next", fg='white', bg='brown',relief=RIDGE, font=("arial", 10, "bold"), command = second_win).place(x=250,y=250)      # next button
label1 = Label(root, text="Search: ", width=20, font=("arial", 10, "bold")).place(x=120, y=160)
entry1 = Entry(root,textvar=fn).place(x=250, y=160)

root.mainloop()

print("----------------------end-------------------")

