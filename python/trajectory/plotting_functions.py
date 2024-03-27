import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

def creatfig(rows,cols,dimensions):
    x,y = dimensions
    fig, axs = plt.subplots(rows,cols, figsize=(x ,y), layout='constrained')
    return fig, axs

def subplotfunc(title,data, Range, xtick, ytick, axlabels, leg, ax=None):
    if ax is None:
        ax = plt.gca()
    scaling = np.empty(len(data[0]))
    for i in range(0,len(data[0])):
         ax.plot(Range,data[:, i])
         scaling[i] = abs(max(data[:, i]) - min(data[:, i]))
       
        

    # xscal_t = len(Range)/xtick
    # yscal_t = max(scaling)/ytick
    # ax.yaxis.set_major_locator(plt.MultipleLocator(yscal_t))
    # ax.xaxis.set_major_locator(plt.MultipleLocator(xscal_t))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(ytick))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(xtick))

    ax.set_xlabel(axlabels[0])
    ax.set_ylabel(axlabels[1])
    ax.title.set_text(title)
    if len(data[0])>1:
        ax.legend(leg,loc ='lower left')
    plt.grid

def save_figure(fig, plot_name): 
    plot_name = 'Graphs/' + plot_name
    script_location = Path(__file__).absolute().parent
    save_location = script_location / plot_name
    fig.savefig(save_location)

def save_figure_abs(fig, plot_name): 
    plot_name = plot_name[0]
    script_location = Path(__file__).absolute().parent
    save_location = script_location / plot_name
    fig.savefig(save_location)