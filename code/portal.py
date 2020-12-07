# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 14:08:36 2019

@author: HG
"""

class Portal:
        
    def __init__(self):
        self.city = ""
        self.url = ""
        self.coord = ""
        self.categorization = ""
        self.platform = ""
        self.categories = []
    
    def setCity(self,city):
        self.city = city
        
    def getCity(self):
        return self.city
    
    def setUrl(self,url):
        self.url = url
        
    def getUrl(self):
        return self.url
    
    def setCoord(self,coord):
        self.coord = coord
    
    def getCoord(self):
        return self.coord
    
    def setCategorization(self, categorization):
        self.categorization = categorization
        
    def getCategorization(self):
        return self.categorization
    
    def setPlatform(self, platform):
        self.platform = platform
    
    def getPlatform(self):
        return self.platform
    
    def addCategorie(self,categoria):
        self.categories.append(categoria)
        
    def setCategories(self, categories):
        self.categories = categories

    def getCategories(self):
        return self.categories

