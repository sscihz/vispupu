import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
import re
from . import colors

def _bin_data(data, yname, xname, bins=50, agg_fn=np.mean):
    data.dropna(inplace=True)
    hist, edges = np.histogram(data[xname], bins=bins)
    bin_midpoint = np.zeros(edges.shape[0]-1)
    binned_df = pd.DataFrame(np.zeros((edges.shape[0]-1, 1)))
    for i in range(edges.shape[0]-1):
        bin_midpoint[i] = (edges[i] + edges[i+1]) / 2
        if i < edges.shape[0]-2:
            dat_temp = data.loc[(data[xname] >= edges[i]) & (
                data[xname] < edges[i+1]), :]
            binned_df.loc[binned_df.index[i], yname] = agg_fn(dat_temp[yname])
            binned_df.loc[binned_df.index[i], xname] = bin_midpoint[i]
            binned_df.loc[binned_df.index[i], 'n_obs'] = dat_temp.shape[0]
        else:
            dat_temp = data.loc[(data[xname] >= edges[i]) & (
                data[xname] <= edges[i+1]), :]
            binned_df.loc[binned_df.index[i], yname] = agg_fn(dat_temp[yname])
            binned_df.loc[binned_df.index[i], xname] = bin_midpoint[i]
            binned_df.loc[binned_df.index[i], 'n_obs'] = dat_temp.shape[0]
    return binned_df

##TODO: Add some Prof. XU's interflex and fect estimation and plot functions
class regview:
    """
    panelview:
    extract data
    panel eda
    panel 
    effect list, if len(effect) equals to two, the first is crosssection while the second is time 
    formula: outcome ~ *key + @treatment + (control1 + control2 + control3)
    """
    def __init__(self,data,outcome=None,key=None,treatment =None, controls=None,effect=None,
        entity_effects=False,
        TimeEffects=False,
        main = None
        ):
        if effect:
            data = data.set_index(effect)
            if len(effect) == 2:
                data = data.sort_index(level=0) ###TODO: this is for my convenience, but I have to write in a more general way
                
    ##TODO: support formula
        self.outcome = outcome
        self.key = key
        self.treatment = treatment
        self.controls = controls
        self.effect = effect
        self.data = data
        self.main = main
   
        
    #heatmap        
    def panelviewtreat(self,cmp=None):
        if self.effect == None:
            err = "to draw panel data plots, you must set index first"
            raise ValueError(err)
        t = sorted(set(self.data.index.get_level_values(1)))
        r = sorted(set(self.data.index.get_level_values(0)))
        
        ma_li = []
        for i in r:
            r_li = []
            for j in t:
                if j in self.data.loc[i].index:
                    r_li.append(self.data.loc[i].loc[j][self.treatment])
                else:
                    r_li.append(np.nan)
            ma_li.append(r_li)
        ma = np.asarray(ma_li)
        cmap = mpl.colors.ListedColormap(['#3D71A0', '#B70050'])


        x = np.arange(ma.shape[1] + 1)
        y = np.arange(ma.shape[0] + 1)

        if cmp:
            cmap = mpl.colors.ListedColormap(cmp)
        
        size_x = 10
        size_y = round(10/len(x)*len(y))
        fig, ax = plt.subplots(figsize=(size_x,size_y),dpi=400)
        im = ax.pcolor(x, y, ma, vmin=0, vmax=1,cmap=cmap)
        
        ax.vlines(np.arange(ma.shape[1]), ymin=0, ymax=ma.shape[0],linestyles='-', alpha=0.4,lw=.2)
        ax.hlines(np.arange(ma.shape[0]), xmin=0, xmax=ma.shape[1],linestyles='-', alpha=0.4,lw=.2)
        
        miss = mpl.lines.Line2D([], [], color='#EAF2F8',ls='', marker = 's',label='missing')
        uncon = mpl.lines.Line2D([], [], color= '#3D71A0',ls='',  marker = 's',label='under control')
        untreat = mpl.lines.Line2D([], [], color= '#B70050',ls='',  marker = 's',label='under treatment')
        # etc etc
        plt.legend(bbox_to_anchor=(.8, -.03),handles=[miss, uncon,untreat],ncol=3)
        

        ##set main
        if self.main:
            ax.set_title(self.main)
        ## set labels 
        ax.set_yticks(np.arange(ma.shape[0])+0.5)
        ax.set_yticklabels(r)

        ax.set_xticks(np.arange(ma.shape[1])+0.5)
        ax.set_xticklabels(t,rotation=90)
        ##lables    
        ax.set_xlabel(self.effect[0], fontsize=18)
        ax.set_ylabel(self.effect[1], fontsize=16)

    ##line                  
    def panelviewline(self,colormap = ['#B5D4E9', '#E4B4B4']):
        if self.effect == None:
            err = "to draw panel data plots, you must set index first"
            raise ValueError(err)
        
        def _color_line(d,cate,y,t,c): #data, category, y(outcome), treatment, color
            x = d.loc[cate].index
            y = d.loc[cate][y]
            t = d.loc[cate][t]
            # select how to color
            color = []
            for i in range(len(y)):
                if t.iloc[i] == 0:
                    color.append(c[0]) 
                else:
                    color.append(c[1])
            # get segments
            xy = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.hstack([xy[:-1], xy[1:]])
            # make line collection
            lc = LineCollection(segments, linewidths=lwidths, color=color)
            return(lc)
        
        def _grey_line(d,cate,y,t,c="#CCD1D1"):
            x = d.loc[cate].index
            y = d.loc[cate][y]
            # get segments
            xy = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.hstack([xy[:-1], xy[1:]])
            # make line collection
            lc = LineCollection(segments, linewidths=lwidths, color=c)
            return(lc)

        ## categories with treatment 
        ## categories without treatment
        cate_treat = sorted(set([cat[0] for cat in self.data[self.data[self.treatment]==1].index]))
        cate_notreat = [i for i in set(self.data.index.get_level_values(0)) if i not in cate_treat]
        
        
        treatlines = [_color_line(self.data,cat,self.outcome,self.treatment,colormap) for cat in cate_treat]
        conlines = [_grey_line(self.data,cat,self.outcome,self.treatment) for cat in cate_notreat]
        fig, ax = plt.subplots(figsize=(15,10),dpi=400)

        #set axis
        ax.set_xlim(min(set(self.data.index.get_level_values(1))), max(set(self.data.index.get_level_values(1))))
        ax.set_ylim(min(self.data[self.outcome]), max(self.data[self.outcome]))
        ##set main
        if self.main:
            ax.set_title(self.main)
        ##axis labels    
        ax.set_xlabel(self.effect[1], fontsize=18)
        ax.set_ylabel(self.key, fontsize=16)
        #
        #color legend 
        cont = mpl.lines.Line2D([], [], color='#CCD1D1',ls='-', label='control')
        tbf = mpl.lines.Line2D([], [], color= colormap[0],ls='-', label='before treatment')
        taf = mpl.lines.Line2D([], [], color= colormap[1],ls='-', label='after treatment')
        # etc etc
        plt.legend(handles=[cont, tbf,taf])
        ###plot
        for tl in treatlines:
            ax.add_collection(tl)
        for tl in conlines:
            ax.add_collection(tl)
        fig.tight_layout()

    def rddview(self):
        if self.bins:
            bins = self.bins
            data = _bin_data(self.data, self.outcome, self.key,bins=bins)
        else:
            data = self.data
        colors = []
        for i in range(len(data)):
            if data[self.key].iloc[i] >= self.th:
                colors.append("#F5B7B1")
            else:
                colors.append("#AED6F1")
        data['colors'] = colors

        fig, ax = plt.subplots(figsize=(16,9),dpi=400)
        ax.scatter(data[self.key], data[ self.outcome], color=colors)
        ax.axvline(x=self.th, color='#C0392B')
        ax.set_xlabel(self.key)
        ax.set_ylabel(self.outcome)
    
    def _fit_lowess(self):
        """Fit a locally-weighted regression, which returns its own grid."""
        from statsmodels.nonparametric.smoothers_lowess import lowess
        grid, yhat = lowess(self.data[self.outcome], self.data[self.key]).T
        return grid, yhat
                
    def vvview(self):
        fig, ax = plt.subplots(figsize=(16,9),dpi=400)
        grid, yhat = self._fit_lowess()
        ax.scatter(self.data[self.key], self.data[self.outcome], color='#17202A')
        ax.plot(grid, yhat,color = '#E74C3C')
        ax.set_xlabel(self.key)
        ax.set_ylabel(self.outcome)

    #TODO:  fit: panel, rdd, did, ols    
    #mod = IV2SLS.from_formula('np.log(wage) ~ 1 + exper + exper ** 2 + [educ ~ motheduc + fatheduc]', data)
    #TODO: regview

###key var distributions 

def keyvarview(data,keyvar,main=None):
    
    fig = plt.figure(figsize=(16,9),dpi=400)
    num = len(keyvar)*100 + 10
    for k in range(len(keyvar)):
        n = num + k + 1
        var = keyvar[k]
        ax = fig.add_subplot(n)
        ax.hist(data[var], bins=10,alpha=.2)
        ax.set_xlabel(var, fontsize=18)
        ax.set_ylabel('Number', fontsize=16)
        if main:
            ax.set_title(main)

def panelviewtreat(data,outcome=None,key=None,treatment =None, controls=None,effect=None,
        bins = None, th = None,
        entity_effects=False,
        TimeEffects=False,
        main = None):
    plotter = regview(data = data,outcome=outcome,key=key,treatment =treatment, controls=controls,effect=controls,
        bins = bins, th = bins,
        entity_effects=bins,
        TimeEffects=bins,
        main = bins)

    ax = plotter.panelviewtreat()

    return ax
    

def panelviewline(data,outcome=None,key=None,treatment =None, controls=None,effect=None,
        bins = None, th = None,
        entity_effects=False,
        TimeEffects=False,
        main = None):
    plotter = regview(data = data,outcome=outcome,key=key,treatment =treatment, controls=controls,effect=controls,
        bins = bins, th = bins,
        entity_effects=bins,
        TimeEffects=bins,
        main = bins)

    ax = plotter.panelviewtreat()

    return ax

def rddview(data,outcome=None,key=None,treatment =None, controls=None,effect=None,
        bins = None, th = None,
        entity_effects=False,
        TimeEffects=False,
        main = None):

    plotter = regview(data = data,outcome=outcome,key=key,treatment =treatment, controls=controls,effect=controls,
        bins = bins, th = bins,
        entity_effects=bins,
        TimeEffects=bins,
        main = bins)

    ax = plotter.rddview()

    return ax

def vvview(sdata,outcome=None,key=None,treatment =None, controls=None,effect=None,
        bins = None, th = None,
        entity_effects=False,
        TimeEffects=False,
        main = None):
    
    plotter = regview(data = data,outcome=outcome,key=key,treatment =treatment, controls=controls,effect=controls,
        bins = bins, th = bins,
        entity_effects=bins,
        TimeEffects=bins,
        main = bins)

    ax = plotter.vvview()

    return ax


def _countna(df,x,val):
    return df[val].isnull().groupby([df[x]]).sum().astype(int)

def missingview(data,var,groupby='obs',cmp = None, main=None, edgecolors='k', linewidths=.5):
    """
    data: dataframe
    var: variable list
    if groupby == obs, no groupby would be conducted 
    """
    
    if groupby == 'obs':
        ma = np.asarray([data[i] for i in var])
        ma = np.where(np.isnan(ma), 0, 1)
        cmap = mpl.colors.ListedColormap(['#F92802','#FFDA64'])###pupu color

    else: 
        ma = np.asarray([countna(data,groupby,i) for i in var])
        cmap = mpl.colors.ListedColormap(list(reversed(color_styles['Asbestos'])))
    x = np.arange(ma.shape[1] + 1)
    y = np.arange(ma.shape[0] + 1)
    
    if cmp:
        cmap = mpl.colors.ListedColormap(cmp)
    
    ##plot
    fig, ax = plt.subplots(figsize=(16,9),dpi=400)
    if groupby == "obs":
        im = ax.pcolor(x, y, ma, vmin=ma.min(), vmax=ma.max(),cmap=cmap)
        ax.hlines(np.arange(ma.shape[0]), xmin=0, xmax=ma.shape[1],linestyles='-', alpha=0.4,lw=2)
        fig.colorbar(im, ax=ax,ticks = [0,1])    ##set legends
    else: 
        im = ax.pcolor(x, y, ma, vmin=ma.min(), vmax=ma.max(),cmap=cmap,edgecolors=edgecolors, linewidths=linewidths)
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
