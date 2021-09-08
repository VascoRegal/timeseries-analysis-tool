import matplotlib.pyplot as plt
import numpy as np

from utils import TIME_CONVERSION_TABLE

#path onde as imagens são guardadas
SAVE_PATH = './'

def gen_plot(x, y, xlabel, ylabel, title, window, **kwargs):
        '''
        Gera um Plot
        
        Params:
                (list) x       ->      valores eixo x          
                (list) y       ->      valores eixo y
                (str)  xlabel  ->      label do eixo x
                (str)  ylabel  ->      label do eixo y
                (str)  title   ->      titulo do plot
                (str)  window  ->      nome da janela onde o plot vai ser gerado
                (dict) kwargs  ->      dicionario com outras options do matplotlib

        Return:
                None 

        '''
        plt.figure(window)
        plt.plot(x,y, **kwargs)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

def gen_hist(x, bins, xlabel, ylabel, title, window, **kwargs):
        '''
        Gera um Histograma
        
        Params:
                (list)        x       ->      dataset 
                (numpy array) bins    ->      intervalos de valores de cada barra (numpy array)
                (str)         xlabel  ->      label do eixo x
                (str)         ylabel  ->      label do eixo y
                (str)         title   ->      titulo do plot
                (str)         window  ->      nome da janela onde o plot vai ser gerado
                (dict)        kwargs  ->      dicionario com outras options do matplotlib

        Return:
                None 

        '''

        plt.figure(window)
        hst, edges = np.histogram(x, bins)

        plt.bar(range(len(hst)), hst, tick_label=
                        [f'{bins[i], bins[i+1]}' for i,j in enumerate(hst)], **kwargs)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

def show_plots(save=True):
        '''
        Mostra todos os plots e histograms gerados
        
        Params:
                (bool) save    ->      boolean para guardar ou não os plots como imagem
        Return:
                None 

        '''

        for i in plt.get_fignums():
                fig = plt.figure(i)
                plt.legend()
                if save:
                        plt.savefig(SAVE_PATH + str(i))
        plt.show()





