# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 15:29:11 2019

@author: HG
"""

import os
import json
import operator 
from collections import OrderedDict

from nlp import tokenizer, remove_stop_words, count_word_frequency
from portal import read_portals_from_json_file, all_categories, exclude_portals_without_category
        
def count_portals_for_words(dictWordFreq, portals):
    
    dictWordPortals = {}
       
    for word, freq in dictWordFreq.items():
        
        for portal in portals:
    
            tokens = tokenizer(portal.categories)
            words = remove_stop_words(tokens, words_to_remove)
    
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
        
    dictWordPortals = count_portals_for_words(dictWordFreq, portals)
    dictWordPortalsDifference = fillDictWordPortalsDifference(dictWordPortals)
        
    portalWithCategories = exclude_portals_without_category(portals)
    
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
            
            categories = portal.categories
                
            for category in categories:
                
                lst = []
                lst.append(category)
                tokens = tokenizer(lst)
                words = remove_stop_words(tokens, words_to_remove)
                
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
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("\n")

portals_file = "../portals.json"
categories_output_file = output_dir + 'most_coverage_categories.json'

portals = read_portals_from_json_file(portals_file)

print("Number of Portals: " + "{0}".format(len(portals)))

lstCategories = all_categories(portals)
print("Number of Categories: " + "{0}".format(len(lstCategories)))

tokens = tokenizer(lstCategories)
print("Number of tokens in categories: " + "{0}".format(len(tokens)))

words_to_remove = ["&","gis","/","kc","fy","foia","geo","city","data","go",
                     "-",",","houston","use","public","department","."]

words = remove_stop_words(tokens, words_to_remove)

dictWordFreq = count_word_frequency(words)
print("Number of words in categories: " + "{0}".format(len(dictWordFreq)))
print("\n")
print(dictWordFreq)
print("\n")

dictPortalsCoverage = fillDictPortalsCoverage(dictWordFreq, portals)
print(dictPortalsCoverage)
print("\n")

trheshold = 98.0
more_coverage_words = more_coverage_words(dictPortalsCoverage, trheshold)
print(more_coverage_words)
print("\n")

dictWordCategoryFreq = fillDictWordCategoryFreq(more_coverage_words, portals, words_to_remove)
print(dictWordCategoryFreq)
print("\n")

dictWordFrequentlyCategories = fillDictWordFrequentlyCategories(dictWordCategoryFreq)
print(dictWordFrequentlyCategories)
print("\n")

write_categories(dictWordFrequentlyCategories, categories_output_file)