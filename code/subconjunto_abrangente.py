# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 15:29:11 2019

@author: HG
"""

#import nltk
#nltk.download('stopwords')

import json
from portal import Portal

def readPortalsFromJsonFile(portalsFile, platform=None):
        
    lstPortals = []
    with open(portalsFile, 'r') as json_file:  
        data = json.load(json_file)
        for p in data:
            portal = Portal()
            portal.setCity(p["city"])
            portal.setUrl(p["url"])
            portal.setCoord(p["coord"])
            portal.setCategorization(p["categorization"])
            portal.setPlatform(p["platform"])
            portal.setCategories(p['categories'])
            lstPortals.append(portal)

    if platform is None:
        return lstPortals

    platform_portals = []
    for portal in lstPortals:
        if (portal.getPlatform() == platform):
            platform_portals.append(portal)
    
    return platform_portals

def allCategories(lstPortals):
    
    lstCategories = []
    
    for portal in lstPortals:
        categories = portal.getCategories()
        for category in categories:
            lstCategories.append(category)
        
    return lstCategories
        
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def tokenizer(lstString):
        
    tokens = []
    for string in lstString:
            
        tokenize = word_tokenize(string)
        for token in tokenize:
            tokens.append(token)
        
    return tokens
    
def removeStopWords(tokens, words_to_remove):
        
    processed_word_list = []  
    for word in tokens:
        word = word.lower()
        if word not in stopwords.words("english"):
            if word not in words_to_remove:
                processed_word_list.append(word)
                
    return processed_word_list

from collections import OrderedDict
import operator 

def frequency_word_count(lstWords):
    
    dictWordFreq = {}
    for word in lstWords:
        freq = dictWordFreq.get(word)
        if freq is None:
            freq = 0
        freq += 1
        dictWordFreq.update({word : freq})
    
    return OrderedDict(sorted(dictWordFreq.items(),
                            key = operator.itemgetter(1),
                            reverse = True))
    
def portalsWithCategories(portals):
    
    portalsWithCategories = []
    
    for portal in portals:
        
        categories = portal.getCategories()
        if(len(categories) > 0):
            portalsWithCategories.append(portal)

    return portalsWithCategories
    
def fillDictWordPortals(dictWordFreq, portals):
    
    dictWordPortals = {}
       
    for word, freq in dictWordFreq.items():
        
        for portal in portals:
            
            categories = portal.getCategories()
            
            tokens = tokenizer(categories)
            words = removeStopWords(tokens, words_to_remove)
    
            if word in words:
        
                lstPortals = dictWordPortals.get(word)
                if(lstPortals is None):
                    lstPortals = []
                      
                lstPortals.append(portal)
                    
                dictWordPortals.update( {word : lstPortals} )
                     
    return dictWordPortals
    
def fillDictWordPortalsDifference(dictWordPortals):
        
    dictWordPortalsDifference = {}
    previousPortals = []

    for word, portals in dictWordPortals.items():
    
        differentPortals = list( set(portals) - set(previousPortals) )  
        dictWordPortalsDifference.update( {word : differentPortals} )
    
        for portal in portals:
            previousPortals.append(portal)
                
    return dictWordPortalsDifference

def fillDictPortalsCoverage(dictWordFreq, portals):
        
    dictPortalsCoverage = {}
        
    dictWordPortals = fillDictWordPortals(dictWordFreq, portals)
    dictWordPortalsDifference = fillDictWordPortalsDifference(dictWordPortals)
        
    portalWithCategories = portalsWithCategories(portals)
    
    somaPerc = 0
    for word, portais in dictWordPortalsDifference.items():
        perc = (len(portais) * 100 / len(portalWithCategories))
        somaPerc = somaPerc + perc
            
        dictPortalsCoverage.update({word : somaPerc})
        
    return dictPortalsCoverage

def more_coverage_words(dictAbrangenciaPortais, threshold):
    
    more_coverage_words = []
    
    for word, abrangencia in dictAbrangenciaPortais.items():
        
        if abrangencia < threshold:
            
            more_coverage_words.append(word)
        
        elif abrangencia == threshold:  
            
            more_coverage_words.append(word)
            return more_coverage_words
        
        elif abrangencia > threshold:
            
            return more_coverage_words
            
    return more_coverage_words

def fillDictWordCategoryFreq(more_coverage_words, portals, words_to_remove):
        
    dictWordCategoryFreq = {}
    for word in more_coverage_words:
                        
        dictFreq = {}
        for portal in portals:
            
            categories = portal.getCategories()
                
            for category in categories:
                
                lst = []
                lst.append(category)
                tokens = tokenizer(lst)
                words = removeStopWords(tokens, words_to_remove)
                
                if word in words:
                    freq = dictFreq.get(category)
                    
                    if freq is None:
                        freq = 0
                    
                    freq += 1
                        
                    dictFreq.update( {category : freq} )
                        
        dictFreqOrd = OrderedDict(sorted(dictFreq.items(),
                                         key = operator.itemgetter(1),
                                         reverse = True))            
        dictWordCategoryFreq.update( {word : dictFreqOrd} )  
    
    return dictWordCategoryFreq    

def fillDictWordFrequentlyCategories(dictTarget):
        
    dictWordFrequentlyCategories = {}       
    for target, dictFreq in dictTarget.items():
            
        maiorFreq = 0
        for categoria, freqB in dictFreq.items():
                        
            if freqB > maiorFreq:
                maiorFreq = freqB
            
        lstCategorias = []            
        for categoria, freqB in dictFreq.items():
                
            if(freqB == maiorFreq):
                lstCategorias.append(categoria)
            
        dictWordFrequentlyCategories.update({target : lstCategorias})
    
    return dictWordFrequentlyCategories

def get_categories_from_dict_word_frequently(dictWordFrequentlyCategories):
    
    categories_lst = []
    for frequently_word, categories in dictWordFrequentlyCategories.items():
        
        for categorie in categories:
            categories_lst.append(categorie)
    
    return categories_lst
        

def write_categories(dictWordFrequentlyCategories, outputCategoriesFile):
    
    categories_lst = get_categories_from_dict_word_frequently(dictWordFrequentlyCategories)
    
    file = open(outputCategoriesFile, 'w')
    
    s = json.dumps(categories_lst, indent=4, ensure_ascii=False).encode('utf8').decode('latin1')
    
    file.writelines(s)
    file.close()

output_dir = "output/"

import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("\n")

portalsFile = "../portals.json"
outputCategoriesFile = output_dir + 'most_coverage_categories.json'

lstPortal = readPortalsFromJsonFile(portalsFile)

print("Number of Portals: " + "{0}".format(len(lstPortal)))

lstCategories = allCategories(lstPortal)
print("Number of Categories: " + "{0}".format(len(lstCategories)))

tokens = tokenizer(lstCategories)
print("Number of tokens in categories: " + "{0}".format(len(tokens)))

words_to_remove = ["&","gis","/","kc","fy","foia","geo","city","data","go",
                     "-",",","houston","use","public","department","."]

lstWords = removeStopWords(tokens, words_to_remove)

dictWordFreq = frequency_word_count(lstWords)
print("Number of words in categories: " + "{0}".format(len(dictWordFreq)))
print("\n")
print(dictWordFreq)
print("\n")

dictPortalsCoverage = fillDictPortalsCoverage(dictWordFreq, lstPortal)
print(dictPortalsCoverage)
print("\n")

trheshold = 98.0
more_coverage_words = more_coverage_words(dictPortalsCoverage, trheshold)
print(more_coverage_words)
print("\n")

dictWordCategoryFreq = fillDictWordCategoryFreq(more_coverage_words, lstPortal, words_to_remove)
print(dictWordCategoryFreq)
print("\n")

dictWordFrequentlyCategories = fillDictWordFrequentlyCategories(dictWordCategoryFreq)
print(dictWordFrequentlyCategories)
print("\n")

write_categories(dictWordFrequentlyCategories, outputCategoriesFile)


