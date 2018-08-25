from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet as wn
import urllib.request as req
import datetime
import sys

class webdata:
    def __init__(self):
        self.tagsList = []
        self.eventList = []
        self.taglist = ["Seminar", "Talk", "Technology", "Workshop", "Economics", "History", "Fest", "Sports", "Gender", "Media", "Culture", "Faculty", "Concert", "Conference", "Politics", "Nationalism"] 
        self.scraping()
    def scraping(self):
        url = "https://www.ashoka.edu.in/events/events/list/?tribe_paged=1&tribe_event_display=list&tribe-bar-date=" + str(datetime.date.today())        
        page = req.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        nameList = []
        dateList = []
        for name in soup.findAll("a", { "class" : "tribe-event-url" }):
            nameList.append(name.text.strip())
        for date in soup.findAll("div", { "class" : "tribe-event-schedule-details" }):
            dateList.append(date.text.strip())
        if len(nameList) != len(dateList):
            print ("Scraping Error!")
            sys.exit()
        for i in range(len(nameList)):
            self.eventList.append((nameList[i], dateList[i]))
        for name in nameList:
            print ("Hit {}: {}".format(nameList.index(name) + 1, name))
            #Tokenizing
            eventtags = []
            pos = nltk.word_tokenize(name)
            tokenized_text = nltk.pos_tag(pos)
            nounset = []
            for item in (tokenized_text):
                if (item[1][:2] == "NN" and len(item[0])>=3 and "," not in item[0] and "." not in item[0]):
                    nounset.append(item[0])
            #Checking similarity of pre existing tags
            for tag in self.taglist:
                synset1 = wn.synsets(tag)
                max = 0
                for noun in nounset:
                    synset2 = wn.synsets(noun)
                    score = self.checksim(synset1, synset2)
                    if(score>max):
                        max = score
                if(max>3):
                    eventtags.append(tag)
            self.tagsList.append(eventtags)
    def checksim(self, synset1,synset2):
        score = 0
        for syn1 in synset1:
            for syn2 in synset2:
                try:
                    ns = wn.lch_similarity(syn1,syn2)
                except:
                    ns = 0
    #            ns = wn.wup_similarity(syn1,syn2)
                if isinstance(ns, float):
                    if ns > score:
                        score = ns
        return(score)
