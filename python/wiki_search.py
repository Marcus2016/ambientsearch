#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Benjamin Milde'

import wikipedia
from timer import Timer

summary_cache = {}
keyword_cache = {}
wiki_cache = {}

#Remove text between () and [] in a string, taken from http://stackoverflow.com/questions/14596884/remove-text-between-and-in-python
def filterBrackets(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

# Input: sorted list of tuples (keyword,scores), maximal number of articles (can be more keywords, if no)
# This version does not perform clustering
#@profile
def getSummariesSingleKeyword(keywords, max_entries=4, lang='en', pics_folder='pics/'):
    with Timer() as t:
        wikipedia.set_lang(lang)
        articles = []
        summary_box_info = {}

        num_results = 0

        for keyword,score in keywords:
            if num_results >= max_entries:
                break
            #check cache first
            if  keyword in keyword_cache:
                articles.append(keyword_cache[keyword])
                num_results += 1
            else:
                result = wikipedia.search(keyword)
                if len(result) > 0:
                    try:
                        article = result[0]
                        #exclude number articles
                        if not "(number)" in article and not "Unk"==article:
                            summary = filterBrackets(wikipedia.summary(article, sentences=1))
                            articles.append((article,summary,score))
                            num_results += 1
                            keyword_cache[keyword] = (article,summary,score)
                    except Exception as e: #TODO: we should jut ignore DisambiguationError and report the rest
                        pass
                else:
                    keyword_cache[keyword] = ("","",0.0)
                    
        for article,summary,score in articles:
            if article != '':

                if article in wiki_cache:
                    wiki_article = wiki_cache[article]
                else:
                    wiki_article = wikipedia.page(article)

                summary_box_info[wiki_article.title] = {'title':wiki_article.title,'text':summary,'url':"https://en.wikipedia.org/w/index.php?title="+wiki_article.title.replace(' ','_'),'score':score}

    return summary_box_info
