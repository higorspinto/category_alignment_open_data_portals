# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:39:23 2017

@author: Higor
"""

import matplotlib.pyplot as plt 
import pandas as pd
from math import pi

class Plotter():
    
    def __init__(self):
        pass
    
    def plotPizza(self, labels, valores, cores, file):     
        
        fig = plt.figure(figsize=(8,7))
        explode = []
        
        for i in range(0 , len(valores) - 1):
            explode.append(0)
            
        explode.append(0.02)
        
        plt.pie(valores, labels=labels, 
                colors=cores,autopct=lambda p: '{:.0f}'.format(p), 
                shadow=True, startangle=90, explode=explode)
        plt.axis('equal')
        plt.savefig(file)
    
        plt.close(fig)
        
    def plotHist(self, valores, barras):
        plt.hist(valores, bins=barras)
        plt.show()
    
    def plotBarH(self, x_val, y_val, y_labels, x_label, cor, file,):
        
        fig = plt.figure(figsize=(9,6))
        plt.barh(x_val, y_val, align='center',color=cor)
        plt.yticks(x_val, y_labels, rotation='horizontal')
        plt.xlabel(x_label)
        plt.savefig(file)  
        plt.show()
    
        plt.close(fig)
        
    def plotBarV(self, x_val, y_val, x_labels, x_label, y_label, cor, file):
        
        fig = plt.figure(figsize=(9,6))
        #plt.bar(x_val, y_val, align='center',color=cor)
        plt.bar(x_val, y_val, align='center')
        plt.xticks(x_val, x_labels)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(file)  
        plt.show()
    
        plt.close(fig)
        
    def plotBarEmpilhado(self, x_valA, y_valA, x_valB, y_valB, label_A, label_B, y_labels, x_label, y_label, file):
        
        fig = plt.figure(figsize=(12,10))
        
        colors2 = ['darkgray']
        colors1 = ['gray']
        
        p1 = plt.barh(x_valA, y_valA, color=colors1)
        p2 = plt.barh(x_valB, y_valB, left=y_valA, color=colors2)
        
        
        plt.legend((p1[0], p2[0]), (label_A, label_B), 
                   bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
                   ncol=2, borderaxespad=0.)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.yticks(x_valA, y_labels)
        
        plt.savefig(file)
        plt.show()
        plt.close(fig)
        
    def plotScatter(self, x, y, axis):
        
        plt.plot(x, y, 'b.')
        plt.axis(axis)
        plt.show()
        
    def plotRadar(self):
                
        # Set data
        df = pd.DataFrame({
        'group': ['A','B','C','D'],
        'var1': [0.8, 0.0, 0.0, 0.0],
        'var2': [0.0, 0.0, 0.7, 0.0],
        'var3': [0.0, 0.6, 0.0, 0.0],
        'var4': [0.0, 0.0, 0.0, 0.4]
        })
        
        # number of variable
        categories=list(df)[1:]
        N = len(categories)
        
        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        values = df.loc[0].drop('group').values.flatten().tolist()
        values += values[:1]
        print(values)
        
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        print(angles)
        
        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)
        
        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=8)
                
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([0.25, 0.5, 0.75], ["0.25","0.5","0.75"], color="grey", size=7)
        plt.ylim(0,1)
        
        plt.plot(angles, values, 'ro')
        # Plot data
        #ax.plot(angles, values, 'ro')
        
        # Fill area
        #ax.fill(angles, values, 'b', alpha=0.1)
        
    def plotMapa(self):
        
        pass

        
        
        