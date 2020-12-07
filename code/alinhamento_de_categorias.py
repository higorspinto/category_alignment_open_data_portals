# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 17:16:18 2019

@author: HG
"""

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import WordNetError

import time

import logging
logging.basicConfig(filename='logging.log',level=logging.DEBUG)

#import nltk
#nltk.download('averaged_perceptron_tagger')

#import nltk
#nltk.download('wordnet')

#nltk.download('wordnet_ic')

import json
from portal import Portal

def readPortalsFromJsonFile(portalsFile):
        
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
    
    return lstPortals[:5]

def readCategoriesFromJsonFile(categoriesFile):
    
    lstCategories = []
    
    with open(categoriesFile, 'r') as json_file:  
        data = json.load(json_file)
        for p in data:
            lstCategories.append(p)
    
    return lstCategories

def penn_to_wn(tag):
    
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    if tag.startswith('D'):
        return 'd'
    
    return None

def tagged_to_synset(word, tag, first_synset = True):
        
    wn_tag = penn_to_wn(tag)
        
    if wn_tag is None:
        return None
     
    try:
        if(first_synset == True):
            synsets = []
            synsets.append((wn.synsets(word, wn_tag)[0]))
            return synsets
        else:
            return wn.synsets(word, wn_tag)
    except:
        return None

# calcula a similaridade entre dois synset
def synset_similarity(synset1, synset2):
    
    brown_ic = wordnet_ic.ic('ic-brown.dat')
        
    sim_path = synset1.path_similarity(synset2)
        
    sim_wup = synset1.wup_similarity(synset2)
    
    try:
        sim_lch = synset1.lch_similarity(synset2)
    except WordNetError as err:
        sim_lch = 0.0
        logging.warning(err)
        
    try:
        sim_res = synset1.res_similarity(synset2, brown_ic)
    except WordNetError as err:
        sim_res = 0.0
        logging.warning(err)
        
    try:
        sim_jcn = synset1.jcn_similarity(synset2, brown_ic)
    except WordNetError as err:
        sim_jcn = 0.0
        logging.warning(err)
    
    try:
        sim_lin = synset1.lin_similarity(synset2, brown_ic)
    except WordNetError as err:
        sim_lin = 0.0
        logging.warning(err)
        
            
    return sim_path, sim_wup, sim_lch, sim_res, sim_jcn, sim_lin

def synsets_similarity(synsets1, synsets2):

    ### calcula a maior similaridade entre os dois synsets  
    best_score_path = 0.0
    best_score_wup = 0.0
    best_score_lch = 0.0
    best_score_res = 0.0
    best_score_jcn = 0.0
    best_score_lin = 0.0
    
    it_synsets1 = iter(synsets1)
    
    # For each synset in the first synsets
    for synset1 in it_synsets1:
        
        it_synsets2 = iter(synsets2)
        
        for synset2 in it_synsets2:
            
            sim_path, sim_wup, sim_lch, \
            sim_res, sim_jcn, sim_lin = synset_similarity(synset1, synset2)
              
            if sim_path is None:
                sim_path = 0.0
                
            if sim_wup is None:
                sim_wup = 0.0
                
            if sim_lch is None:
                sim_lch = 0.0
                
            if sim_res is None:
                sim_res = 0.0
                    
            if sim_jcn is None:
                sim_jcn = 0.0
                
            if sim_lin is None:
                sim_lin = 0.0
                
            if sim_path > best_score_path:
                best_score_path = sim_path
                
            if sim_wup > best_score_wup:
                best_score_wup = sim_wup
                
            if sim_lch > best_score_lch:
                best_score_lch = sim_lch
            
            if sim_res > best_score_res:
                best_score_res = sim_res
                
            if sim_jcn > best_score_jcn:
                best_score_jcn = sim_jcn
                
            if sim_lin > best_score_lin:
                best_score_lin = sim_lin
                
    return best_score_path, best_score_wup, best_score_lch, best_score_res, best_score_jcn, best_score_lin

#calcula a similaridade entre duas sentenças, utilizando os seis métodos    
def sentence_similarity(sentence1, sentence2, first_synset=True):
    
    """ compute the sentence similarity using Wordnet """
    
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word, first_synset) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word, first_synset) for tagged_word in sentence2]

    # Filter out the Nones
    all_synsets1 = [ss for ss in synsets1 if ss]
    all_synsets2 = [ss for ss in synsets2 if ss]
    
    score1_path = 0.0
    score1_wup = 0.0
    score1_lch = 0.0
    score1_res = 0.0
    score1_jcn = 0.0
    score1_lin = 0.0
    count1 = 0
 
    it_all_synsets1 = iter(all_synsets1)
    
    # For each synsets of each word in the first sentence
    for synsets1 in it_all_synsets1:
        
        best_score_path = 0.0
        best_score_wup = 0.0 
        best_score_lch = 0.0
        best_score_res = 0.0
        best_score_jcn = 0.0
        best_score_lin = 0.0
        
        it_all_synsets2 = iter(all_synsets2)
        
        # For each synsets of each word in the second sentence
        # Get the similarity value of the most similar synset in the other sentence
        for synsets2 in it_all_synsets2:
            
            best_score_path, best_score_wup, best_score_lch, \
            best_score_res, best_score_jcn, best_score_lin = synsets_similarity(synsets1, synsets2)
            
            score1_path += best_score_path
            score1_wup += best_score_wup
            score1_lch += best_score_lch
            score1_res += best_score_res
            score1_jcn += best_score_jcn
            score1_lin += best_score_lin
        
            count1 += 1
 
    # Average the values
    if(score1_path != 0):
        score1_path /= count1
    
    if(score1_wup != 0):
        score1_wup /= count1
        
    if(score1_lch != 0):
        score1_lch /= count1
        
    if(score1_res != 0):
        score1_res /= count1
    
    if(score1_jcn != 0):
        score1_jcn /= count1
        
    if(score1_lin != 0):
        score1_lin /= count1
        
    score2_path = 0.0 
    score2_wup = 0.0
    score2_lch = 0.0
    score2_res = 0.0
    score2_jcn = 0.0 
    score2_lin = 0.0
    count2 = 0    
       
    it_all_synsets2 = iter(all_synsets2)
    
    # For each word in the second sentence
    for synsets2 in it_all_synsets2:
        
        best_score_path = 0.0 
        best_score_wup = 0.0
        best_score_lch = 0.0
        best_score_res = 0.0
        best_score_jcn = 0.0 
        best_score_lin = 0.0
        
        it_all_synsets1 = iter(all_synsets1)
        
        # For each synsets of each word in the first sentence
        # Get the similarity value of the most similar synset in the other sentence
        for synsets1 in it_all_synsets1:
            
            best_score_path, best_score_wup, best_score_lch, \
            best_score_res, best_score_jcn, best_score_lin = synsets_similarity(synsets1, synsets2)          
            
            score2_path += best_score_path
            score2_wup += best_score_wup
            score2_lch += best_score_lch
            score2_res += best_score_res
            score2_jcn += best_score_jcn
            score2_lin += best_score_lin
        
            count2 += 1
 
    # Average the values
    if(score2_path != 0 ):
        score2_path /= count2
        
    if(score2_wup != 0 ):
        score2_wup /= count2
        
    if(score2_lch != 0 ):
        score2_lch /= count2
        
    if(score2_res != 0 ):
        score2_res /= count2
        
    if(score2_jcn != 0 ):
        score2_jcn /= count2
        
    if(score2_lin != 0 ):
        score2_lin /= count2
    
    score_path = (score1_path + score2_path) / 2
    score_wup = (score1_wup + score2_wup) / 2
    score_lch = (score1_lch + score2_lch) / 2
    score_res = (score1_res + score2_res) / 2
    score_jcn = (score1_jcn + score2_jcn) / 2
    score_lin = (score1_lin + score2_lin) / 2
    
    return score_path, score_wup, score_lch, score_res, score_jcn, score_lin

def get_lst_similarities(category, lstCategoriesToMatch):
    
    best_sim_path = 0.0 
    best_sim_wup = 0.0
    best_sim_lch = 0.0
    best_sim_res = 0.0
    best_sim_jcn = 0.0 
    best_sim_lin = 0.0
    
    best_category_path = ""
    best_category_wup = ""
    best_category_lch = ""
    best_category_res = ""
    best_category_jcn = ""
    best_category_lin = ""
        
    it_categories_to_match = iter(lstCategoriesToMatch)
    for category_coverage in it_categories_to_match:
        
        sim_path, sim_wup, sim_lch, \
        sim_res, sim_jcn, sim_lin = sentence_similarity(category, category_coverage)
        
        if sim_path > best_sim_path:
            best_sim_path = sim_path
            best_category_path = category_coverage
            
        if sim_wup > best_sim_wup:
            best_sim_wup = sim_wup
            best_category_wup = category_coverage
            
        if sim_lch > best_sim_lch:
            best_sim_lch = sim_lch
            best_category_lch = category_coverage
            
        if sim_res > best_sim_res:
            best_sim_res = sim_res
            best_category_res = category_coverage
            
        if sim_jcn > best_sim_jcn:
            best_sim_jcn = sim_jcn
            best_category_jcn = category_coverage
            
        if sim_lin > best_sim_lin:
            best_sim_lin = sim_lin
            best_category_lin = category_coverage
    
    lstSimilarities = []
    lstSimilarities.append("path"), lstSimilarities.append(best_sim_path), lstSimilarities.append(best_category_path)
    lstSimilarities.append("wup"), lstSimilarities.append(best_sim_wup), lstSimilarities.append(best_category_wup)
    lstSimilarities.append("lch"), lstSimilarities.append(best_sim_lch), lstSimilarities.append(best_category_lch)
    lstSimilarities.append("res"), lstSimilarities.append(best_sim_res), lstSimilarities.append(best_category_res)
    lstSimilarities.append("jcn"), lstSimilarities.append(best_sim_jcn), lstSimilarities.append(best_category_jcn)
    lstSimilarities.append("lin"), lstSimilarities.append(best_sim_lin), lstSimilarities.append(best_category_lin)
    
    return lstSimilarities

from collections import OrderedDict
import operator 
import random

def get_most_elected_category(lst_similarities):

    dictCategoryFreq = {}
    
    best_category_path = lst_similarities[2]
    best_category_wup = lst_similarities[5]
    best_category_lch = lst_similarities[8]
    best_category_res = lst_similarities[11]
    best_category_jcn = lst_similarities[14]
    best_category_lin = lst_similarities[17]
    
    freq = dictCategoryFreq.get(best_category_path)
    if(freq is None):
        freq = 0
    freq += 1
    dictCategoryFreq.update( {best_category_path : freq} )
    
    freq = dictCategoryFreq.get(best_category_wup)
    if(freq is None):
        freq = 0
    freq += 1
    dictCategoryFreq.update( {best_category_wup : freq} )
    
    freq = dictCategoryFreq.get(best_category_lch)
    if(freq is None):
        freq = 0
    freq += 1
    dictCategoryFreq.update( {best_category_lch : freq} )
    
    freq = dictCategoryFreq.get(best_category_res)
    if(freq is None):
        freq = 0
    freq += 1
    dictCategoryFreq.update( {best_category_res : freq} )
    
    freq = dictCategoryFreq.get(best_category_jcn)
    if(freq is None):
        freq = 0
    freq += 1
    dictCategoryFreq.update( {best_category_jcn : freq} )
    
    freq = dictCategoryFreq.get(best_category_lin)
    if(freq is None):
        freq = 0
    freq += 1
    dictCategoryFreq.update( {best_category_lin : freq} )
    
    dictFreqOrd = OrderedDict(sorted(dictCategoryFreq.items(),
                                     key = operator.itemgetter(1),
                                     reverse = True))

    maxFreq = max(dictFreqOrd.values())
    
    best_categories = []
    for best_category, freq in dictFreqOrd.items():
        if (freq == maxFreq):     
            best_categories.append(best_category)

    if len(best_categories) > 1:
        index = random.randint(0, len(best_categories) - 1)
        return best_categories[index]
    
    return best_categories[0]
            
    
def fillDictCategoriesMatch(categories, lstCategoriesToMatch):
    
    dictCategorySimilarities = {}
    dictCategoryMatch = {}
    
    it_categories = iter(categories)
    for category in it_categories:
        
        lst_similarities = get_lst_similarities(category, lstCategoriesToMatch) 
        dictCategorySimilarities.update( {category : lst_similarities} )
        
        best_category = get_most_elected_category(lst_similarities)
        dictCategoryMatch.update( {category : best_category} )
 
    return dictCategorySimilarities, dictCategoryMatch 

def fillDictPortalsCategoryMatch(lstPortal, lstCategoriesCoverage):
    
    dictPortalsCategoryMatch = {}
    dictPortalsCategorySimilarities = {}

    it_portals = iter(lstPortal)
    for portal in it_portals:
        
        categories = portal.getCategories()
        dictCategorySimilarities, dictCategoryMatch = fillDictCategoriesMatch(categories, lstCategoriesCoverage)
        
        dictPortalsCategorySimilarities.update( {portal.getCity() : dictCategorySimilarities} )
        dictPortalsCategoryMatch.update( { portal.getCity() : dictCategoryMatch} )
    
    return dictPortalsCategoryMatch, dictPortalsCategorySimilarities

def write_categories_match(dictPortalsCategoryMatch, dictPortalsCategorySimilarities, similarityFile, categoryMatchFile ):
    
    file = open(similarityFile, 'w')
    s = json.dumps(list(dictPortalsCategorySimilarities.items()), 
                   indent=4, ensure_ascii=False).encode('utf8').decode('latin1')
    file.writelines(s)
    file.close()
    
    file = open(categoryMatchFile, 'w')
    s = json.dumps(list(dictPortalsCategoryMatch.items()), 
                   indent=4, ensure_ascii=False).encode('utf8').decode('latin1')
    file.writelines(s)
    file.close()

def test(first_synset = True):
    # Testing the code
    sentence1 = 'Public Safety'
    sentence2 = 'Safety'

    import time 
    start = time.time()
     
    sim_path, sim_wup, sim_lch, \
    sim_res, sim_jcn, sim_lin = sentence_similarity(sentence1, sentence2, first_synset)
    
    print("path sim: {:.2f}".format(sim_path))
    print("wup sim:  {:.2f}".format(sim_wup))
    print("lch sim:  {:.2f}".format(sim_lch))
    print("res sim:  {:.2f}".format(sim_res))
    print("jcn sim:  {:.2e}".format(sim_jcn))
    print("lin sim:  {:.2f}".format(sim_lin))
    
    end = time.time()
    
    print("\n")
    time = (end - start)
    print('duracao: {:.2f}'.format(time) + " s")


if __name__ == '__main__':

    #test()

    output_dir = "output/"

    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    portalsFile = '../portals.json'
    categoriesFile = output_dir + 'most_coverage_categories_edited.json'
    similarityFile = output_dir + 'portals_category_similarities_100_cities_all_synsets.json'
    categoryMatchFile = output_dir + 'portals_category_match_100_cities_all_synsets.json'

    lstPortal = readPortalsFromJsonFile(portalsFile)
    print("Number of Portals: " + "{0}".format(len(lstPortal)))

    lstCategoriesCoverage = readCategoriesFromJsonFile(categoriesFile)
    print("Number of Best Coverage Categories: " + "{0}".format(len(lstCategoriesCoverage)))
    print("\n")

    start = time.time()

    dictPortalsCategoryMatch, dictPortalsCategorySimilarities = fillDictPortalsCategoryMatch(lstPortal, lstCategoriesCoverage)
    write_categories_match(dictPortalsCategoryMatch, dictPortalsCategorySimilarities, similarityFile, categoryMatchFile)

    end = time.time()

    print("\n")
    time = (end - start)
    print('duracao: {:.2f}'.format(time) + " s")