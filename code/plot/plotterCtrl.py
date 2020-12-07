# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 16:05:45 2018

@author: HG
"""

from portalService import PortalService
from plotterPortal import PlotterPortal
from plotter import Plotter

class PlotterCtrl():
    
    portalService = PortalService()
    plotterPortal = PlotterPortal()
    plotter = Plotter()
    
    def __init__(self):
        pass
    
    ############# Funções de Plotagem
        
    def plotarDadosPortais(self, portais):
        
        cores = ['paleturquoise','lightblue','powderblue',
         'lightblue','lightskyblue','steelblue']
        
        cores_gray = ['gray','darkgray','silver','lightgray','gainsboro','whitesmoke']
        
        labels, contagem = self.plotterPortal.obterDadosPizzaPlataforma(portais)
        self.plotter.plotPizza(labels,contagem, cores, 'plataforma.svg')
    
        #labels, contagem = self.plotterPortal.obterDadosPizzaCategorizacao(portais)    
        #self.plotter.plotPizza(labels,contagem, cores, 'categorizacao.pdf')
        
    def plotarDadosCategorias(self, dictCategoria, dictDiferencaPortais, portais, addStopWords):
        
        barColor = 'dimgray'
        
        eixo_x, eixo_y, labels = self.plotterPortal.obterDadosBarCategorias(dictCategoria)
        self.plotter.plotBarH(eixo_x, eixo_y, labels, 'Frequency',barColor, 'categoria_freq.pdf')
        
        portaisFiltro = self.portalService.removerPortaisSemCategorias(portais)
        dictNumCategorias = self.portalService.obterDictNumCategorias(portaisFiltro)
        #self.portalService.imprimirDictNumCategorias(dictNumCategorias)
        
        minCategorias, maxCategorias = self.portalService.obterMinMaxNumCategorias(portaisFiltro)
        eixo_x, eixo_y, labels = self.plotterPortal.obterDadosBarNumCategorias(dictNumCategorias, maxCategorias)
        self.plotter.plotBarV(eixo_x, eixo_y, labels,'\n Number Of Categories','\n Number of Portals',barColor,'num_categorias.pdf')
        
        print("\n")
        print(minCategorias)
        print(maxCategorias)
        
        #dictCategoriasPortais = dictWordPortals
        #portalService.imprimirDictCategoriasPortais(dictCategoriasPortais)

        #dictCategoriasNumPortais = portalService.obterDictCategoriasNumPortais(dictCategoria, portais, addStopWords)
        #portalService.imprimirDictCategoriasNumPortais(dictCategoriasNumPortais)

        dictPortaisDiferentes = dictDiferencaPortais
        self.portalService.imprimirDictDiferencaPortais(dictPortaisDiferentes, len(portaisFiltro)) 

        x_valA, y_valA = self.plotterPortal.obterDadosBarCategoriasPortais(dictCategoria, len(portaisFiltro))
        x_valB, y_valB = self.plotterPortal.obterDadosBarCategoriasPortaisEmpilhado(dictPortaisDiferentes, y_valA, len(portaisFiltro))

        labels_y = list(dictPortaisDiferentes.keys())

        labels_y.reverse()
        y_valA.reverse()

        y_valB[0] = 0
        y_valB.reverse()

        self.plotter.plotBarEmpilhado(x_valA, y_valA, x_valB, y_valB, 
                         "Frequency", "Portals Coverage", 
                         labels_y,
                         "Frequency / Portals Coverage (%)","", "freq_emp.pdf")

    def plotarAbrangenciaPortais(self,categorias, portaisFiltro, addStopWords, numTopCategories):
        
        eixo_x, eixo_y, labels = self.plotterPortal.obterDadosAbrangenciaPortais(categorias, portaisFiltro, addStopWords, numTopCategories)
        
        eixo_y.reverse()
        labels.reverse()
        
        self.plotter.plotBarH(eixo_x, eixo_y, labels, 'Coverage of Portals (%)', 'abrangencia_portais.pdf')
        
    def plotarDadosSimilaridade(self, dictPortalCategoriaSimilaridade):
        
        minWup = 0
        minPath = 0
        minLch = 0
        minRes = 0
        minJcn = 0
        minLin = 0
        
        for city, dictMap in dictPortalCategoriaSimilaridade.items():

            for categoria, lst in dictMap.items():
                
                simWup = lst[1]
                simPath = lst[3]
                simLch = lst[5]
                simRes = lst[7]
                simJcn = lst[9]
                simLin = lst[11]
        
    def plotarDadosPercentualConcordancia(self, dictPercentual):
        
        eixo_x = []
        eixo_y =[]
        
        cont = 1
        for frac, freq in dictPercentual.items():
        
            eixo_x.append(cont)
            if freq is None:
                freq = 0
            eixo_y.append(freq)
            
            cont += 1
        
        labels = ['6', '5', '4', '3', '2', '1','0']
        
        barColor = 'lightblue'
        
        self.plotter.plotBarV(eixo_x, eixo_y, labels,'\n Valor de Concordância','\n Número de Categorias', barColor, 'percentual_concordancia.pdf')
        
    def plotarMapa(self):
        
        self.plotter.plotMapa()