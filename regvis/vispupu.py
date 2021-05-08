
import copy
from textwrap import dedent
import warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def _countna(df,x,val):
    return df[val].isnull().groupby([df[x]]).sum().astype(int)

def missingview(data,var,groupby='obs',cmp = None, main=None, edgecolors='k', linewidths=1):
    """
    data: dataframe
    var: variable list
    if groupby == obs, no groupby would be conducted 
    """
    
    if groupby == 'obs':
        ma = np.asarray([data[i] for i in var])
        ma = np.where(np.isnan(ma), 0, 1)
        cmap = mpl.colors.ListedColormap(['#DE3163','#F5EEF8'])

    else: 
        ma = np.asarray([countna(data,groupby,i) for i in var])
        cmap = mpl.colors.ListedColormap(color_styles['Turquoise'])
    x = np.arange(ma.shape[1] + 1)
    y = np.arange(ma.shape[0] + 1)
    
    if cmp:
        cmap = mpl.colors.ListedColormap(cmp)
    
    ##plot
    fig, ax = plt.subplots(figsize=(16,9),dpi=400)
    im = ax.pcolor(x, y, ma, vmin=ma.min(), vmax=ma.max(),cmap=cmap)
    ax.hlines(np.arange(ma.shape[0]), xmin=0, xmax=ma.shape[1],linestyles='-', alpha=0.4,lw=2, label='Multiple Lines')

    ##set legends
    fig.colorbar(im, ax=ax)

    ##set main
    if main:
        ax.set_title(main)
    ## set labels 
    ax.set_yticks(np.arange(len(var))+0.5)
    ax.set_yticklabels(var)
    
    if groupby != 'obs':
        ax.set_xticks(np.arange(ma.shape[1])+0.5)
        ax.set_xticklabels(data[groupby],rotation=90)
    ##lables    
    ax.set_xlabel(groupby, fontsize=18)
    ax.set_ylabel('Varibles', fontsize=16)


def panelview(data,var,groupby='obs',cmp = None, main=None, edgecolors='k', linewidths=1):
    """
    data: dataframe
    var: variable list
    if groupby == obs, no groupby would be conducted 
    """
    
    if groupby == 'obs':
        ma = np.asarray([data[i] for i in var])
        ma = np.where(np.isnan(ma), 0, 1)
        cmap = mpl.colors.ListedColormap(['#DE3163','#F5EEF8'])

    else: 
        ma = np.asarray([countna(data,groupby,i) for i in var])
        cmap = mpl.colors.ListedColormap(color_styles['Turquoise'])
    x = np.arange(ma.shape[1] + 1)
    y = np.arange(ma.shape[0] + 1)
    
    if cmp:
        cmap = mpl.colors.ListedColormap(cmp)
    
    ##plot
    fig, ax = plt.subplots(figsize=(16,9),dpi=400)
    im = ax.pcolor(x, y, ma, vmin=ma.min(), vmax=ma.max(),cmap=cmap)
    ax.hlines(np.arange(ma.shape[0]), xmin=0, xmax=ma.shape[1],linestyles='-', alpha=0.4,lw=2, label='Multiple Lines')

    ##set legends
    fig.colorbar(im, ax=ax)

    ##set main
    if main:
        ax.set_title(main)
    ## set labels 
    ax.set_yticks(np.arange(len(var))+0.5)
    ax.set_yticklabels(var)
    
    if groupby != 'obs':
        ax.set_xticks(np.arange(ma.shape[1])+0.5)
        ax.set_xticklabels(data[groupby],rotation=90)
    ##lables    
    ax.set_xlabel(groupby, fontsize=18)
    ax.set_ylabel('Varibles', fontsize=16)


def panelviewline(data,formula,mode="treat",colormap = ['#B5D4E9', '#E4B4B4']):
    '''
    data: pandas dataframe
    formula: string, 
        if mode = treat,formula is  outcome~treatment + category + x_var
        if mode = notreat,formula is  outcome~ category + x_var
    outcome: also the y axis
    treatment: pre and post treatment color will be different for a line
    category: set as different lines 
    x_var: x axis (often year)
    mode: treat or no treat
    '''
    ## get variables from formula
    outcome = formula.split("~")[0]
    if mode == "treat":
        treatment = formula.split("~")[1].split("+")[0]
        category = formula.split("~")[1].split("+")[1]
        x_var = formula.split("~")[1].split("+")[2]
    elif mode == "notreat":
        treatment = None
        category = formula.split("~")[1].split("+")[0]
        x_var = formula.split("~")[1].split("+")[1]    
    
    ## new dataframe 
    df = data[[outcome,treatment,category,x_var]].sort_values([category],ascending=True)
    
    #line_names = sorted(list(df_dic.keys()))
    if treatment:
        
        ## categories with treatment 
        ## categories without treatment
        cate_treat = sorted(set(data[data[treatment]==1][category]))
        cate_notreat = sorted(set(data[data[treatment]==0][category]))

        ## dataframe dictionary,then set x and y 
        df_dic_treat = {k: v for k, v in df.groupby(category) if k in cate_treat}
        df_dic_con = {k: v for k, v in df.groupby(category)if k in cate_notreat}
        
        ###control group
        x_control_val_li = [d.sort_values(by=x_var, ascending=True)[x_var] for d in df_dic_con.values()]
        y_control_val_li = [d.sort_values(by=x_var, ascending=True)[outcome] for d in df_dic_con.values()]
        
        ###treat group 
        #x_treat_val_li = [d.sort_values(by=x_var, ascending=True)[x_var] for d in df_dic_treat.values()]
        #y_treat_val_li = [d.sort_values(by=x_var, ascending=True)[outcome] for d in df_dic_treat.values()]
        ###before treat
        x_treat_val_li_bf = [d.sort_values(by=x_var, ascending=True)[d[treatment]==0][x_var] for d in df_dic_treat.values()]
        y_treat_val_li_bf = [d.sort_values(by=x_var, ascending=True)[d[treatment]==0][outcome] for d in df_dic_treat.values()]
        ###after treat
        x_treat_val_li_af = [d.sort_values(by=x_var, ascending=True)[d[treatment]==1][x_var] for d in df_dic_treat.values()]
        y_treat_val_li_af = [d.sort_values(by=x_var, ascending=True)[d[treatment]==1][outcome] for d in df_dic_treat.values()]
        
        ## draw plots:control
        fig, ax = plt.subplots(figsize=(15,10),dpi=400)
        for x,y in zip(x_control_val_li,y_control_val_li):
            ax.plot(x,y,color="#CCD1D1")

        ## draw plots: treatments
        for x,y in zip(x_treat_val_li_bf,y_treat_val_li_bf):
            ax.plot(x,y,color=colormap[0])
        
        for x,y in zip(x_treat_val_li_af,y_treat_val_li_af):
            ax.plot(x,y,color=colormap[1])
                 
    else:
        df_dic = {k: v for k, v in df.groupby(category)}
        x_val_li = [d.sort_values(by=x_var, ascending=True)[x_var] for d in df_dic.values()]
        y_val_li = [d.sort_values(by=x_var, ascending=True)[outcome] for d in df_dic.values()]
        
        ### draw plots
        fig, ax = plt.subplots(figsize=(15,10),dpi=400)
        for x,y in zip(x_val_li,y_val_li):
            ax.plot(x,y,color="#E9967A")

    ## set labels 
#     ax.set_xticks(np.arange(0, x, 1))
#     ax.set_yticks(np.arange(0, y, 1))
#     ax.set_yticklabels(ylb,rotation=0, fontsize=2)
#     ax.set_xticklabels(xlb,rotation=90, fontsize=2)
    return(fig)



def _r2d(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    conf = results.conf_int()

    results_df = pd.DataFrame({"pvals":pvals,
                               "coeff":coeff,
                                })
    results_df = pd.concat([results_df,res.conf_int()],axis=1)
    return results_df

def resultview(reg):
    resmry = r2d(reg)
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.axvline(0, linestyle='--', color='black', linewidth=1)
    ax.hlines(np.arange(len(resmry)), xmin=resmry.lower, xmax=resmry.upper,linestyles='-', alpha=0.4,lw=2, label='Multiple Lines')
    ax.plot(resmry.coeff,np.arange(len(resmry)), marker='o',linestyle='none', alpha=0.4)

    ax.set_yticks(np.arange(0,len(resmry), 1))
    ax.set_yticklabels(resmry.index,rotation=0, fontsize=16)
    plt.show()