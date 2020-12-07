# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 12:50:11 2017

@author: Higor
"""

from collections import OrderedDict
import operator 
import math

from portalService import PortalService

class PlotterPortal():
    
    portalService = PortalService()
    
    def __init__(self):
        pass
    
    def obterDadosPizzaPlataforma(self, portais):
        
        portalService = PortalService() 
        dictPlataforma = portalService.obterDictPlataforma(portais) 
        lstPlataforma = dictPlataforma.keys()

        labels = []
        contagem = []
        
        corte_minoria = 1
        soma_minoria = 0    
        str_minoria = ""
        
        dictFreq = {}
        
        for plataforma in lstPlataforma:
            
            lstPortais = dictPlataforma.get(plataforma)
            
            if(plataforma == "-"):
                    plataforma = "N/A"
            
            dictFreq.update( {plataforma : len(lstPortais)} )
           
        dictFreqOrd = OrderedDict(sorted(dictFreq.items(),key = operator.itemgetter(1),reverse = True))
            
        cont = 0
        for plataforma, freq in dictFreqOrd.items():
                        
            if freq > corte_minoria:  
                
                labels.append(plataforma)
                contagem.append(freq)
                
            else:
                
                soma_minoria += 1
                str_minoria += plataforma
                
                if cont == 0 :
                    str_minoria += ", "
                    str_minoria += "\n"
                elif cont == 1:
                    str_minoria += ", and"
                    str_minoria += "\n"
                elif cont == 1:
                    str_minoria += "\n"
                
                cont += 1
                
        str_minoria += "\n"
        str_minoria += "\n"
        str_minoria += "\n"
        str_minoria += "\n"
        labels.append(str_minoria)
        contagem.append(soma_minoria)  
        
        return labels, contagem
    
    def obterDadosPizzaCategorizacao(self, portais):
        
        dictCategorizacao = self.portalService.obterDictCategorizacao(portais)     
        lstCategorizacao = dictCategorizacao.keys()

        labels = []
        contagem = []
        
        corte_minoria = 1
        soma_minoria = 0    
        str_minoria = ""
        
        for categorizacao in lstCategorizacao:
            
            lstPortais = dictCategorizacao.get(categorizacao)
            
            if len(lstPortais) > corte_minoria:  
                labels.append(categorizacao)
                contagem.append(len(lstPortais))
            else:
                soma_minoria += 1
                str_minoria += categorizacao
                str_minoria += "\n"
        
        str_minoria += "\n"
        str_minoria += "\n"
        str_minoria += "\n"
        labels.append(str_minoria)
        contagem.append(soma_minoria)
        
        return labels, contagem
    
    def obterDadosBarCategorias(self, dictCategoriaFreq):
        
        labels = []
        lstFreq = []
        lstCategoria = dictCategoriaFreq.keys()
        for categoria in lstCategoria:
            lstFreq.append(dictCategoriaFreq.get(categoria))
            labels.append(categoria)
        
        labels.reverse()
        lstFreq.reverse()
            
        return range(len(lstFreq)), lstFreq, labels    
        
    def obterDadosBarNumCategorias(self, dictNumCategorias, maxCategorias):
        
        lstNumCidades = [] 
        labels = []
        
        dictIntervalo = {}
        
        contador = 0
        for i in range(1, maxCategorias + 1):
            
            if((i % 5) == 0):
            
                dictIntervalo.update({ contador : ("{0}".format(i - 4) + "-" + "{0}".format(i)) })
                contador += 1
        
        dictIntervaloNumPortais = {}
        for intervalo, strMinMax in dictIntervalo.items():
            dictIntervaloNumPortais.update( {intervalo : 0} )
        
        for cidade in dictNumCategorias.keys():
            
            numCategorias = dictNumCategorias.get(cidade)
            if( (numCategorias % 5) == 0):
                intervalo = ( (numCategorias / 5) - 1)
            else:
                intervalo = int(numCategorias / 5)
            
            numCidades = dictIntervaloNumPortais.get(intervalo)          
            if numCidades is None:
                numCidades = 0
                
            numCidades += 1
            
            dictIntervaloNumPortais.update( {intervalo : numCidades} )
            
        intervalos = dictIntervaloNumPortais.keys()
        for intervalo in intervalos:
            numCidades = dictIntervaloNumPortais.get(intervalo)
            lstNumCidades.append(numCidades)
            labels.append(dictIntervalo.get(intervalo))

        return range(len(lstNumCidades)), lstNumCidades, labels
    
    def obterDadosBarCategoriasPortais(self, dictCategoria, numPortais):
        
        lstNumPortais = []
        for categoria, freq in dictCategoria.items():
            lstNumPortais.append( (freq * 100) / numPortais )
            
        return range(len(lstNumPortais)), lstNumPortais
    
    def obterDadosBarCategoriasPortaisEmpilhado(self, dictPortaisDiferentes, y_valA, numPortais):
        
        contador = 0
        freqAcumulada = 0
        lstFreqAcumulada = []
        for categoria, portais in dictPortaisDiferentes.items():
            
            freqAcumulada += (len(portais)  * 100) / numPortais          
            lstFreqAcumulada.append(freqAcumulada - y_valA[contador])
            
            contador += 1
            
        return range(len(lstFreqAcumulada)), lstFreqAcumulada
            
    def obterDadosAbrangenciaPortais(self, categorias, portaisFiltro, addStopWords, numTopCategories):
        
        labels = []
        lstSoma = []
        
        i = 0
        while i < 500:
            
            num_Categorias = i + 50
            ordenado = 1
            
            dictCategoria = self.portalService.obterDictCategoriaFrequencia(categorias, num_Categorias, ordenado)
            dictCategoriasPortais = self.portalService.obterDictCategoriasPortais(dictCategoria, portaisFiltro, addStopWords)    
            dictPortaisDiferentes = self.portalService.obterDictDiferencaPortais(dictCategoriasPortais)
            
            somaPortais = 0
            for categoria, portais in dictPortaisDiferentes.items():
                somaPortais += (len(portais) * 100 / len(portaisFiltro))
            
            str = "{0}".format(num_Categorias)
            
            labels.append(str)
            lstSoma.append(somaPortais)
            
            i += 50
            
        return range(len(lstSoma)), lstSoma, labels
    
    def obterDadosSimilaridade(self, dictPortalCategoriaSimilaridade):
        
        x = []
        y = []    
        axis = [0,1,0,1]
        
        for city, dictMap in dictPortalCategoriaSimilaridade.items():

            for categoria, lst in dictMap.items():
                
                if(lst[1] <= 0):
                    continue
                
                x.append(lst[1])
                y.append(math.pow(lst[1],3))
                              
        return x, y, axis
            
        
        
            
            
            
            
        
        
        
        
        
        
        
        