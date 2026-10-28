import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm
import matplotlib as mpl
from noisy_binary_channel_mutual_information import capacity_and_capacity_achieving_p_with_err as capacity
font = {'family' : 'Arial',
        'weight' : 'regular',
        'size'   : 10}
mpl.rc('font',**font)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['figure.constrained_layout.use'] = True

def get_counts(df,pois = ['1','2','3','4']):
    cond = df.dropna()
    cts = np.array([np.count_nonzero(cond[n])for n in pois])
    bnd_rate = np.array([np.count_nonzero(cond[n])/len(cond) for n in pois])
    stds = np.array([np.sqrt(bnd_rate[n]*(1-bnd_rate[n])/(len(cond)-1)) for n in np.arange(len(pois))])
    return cts, bnd_rate, stds

df = pd.read_pickle(r"/Users/maxearle/Library/CloudStorage/OneDrive-Personal/mac_stuff/PhD/Error_Prot/mixture_resultz/checked_protected.pkl")
bcs = []
for index, row in df.iterrows():
    bc = np.array(row.iloc[1:])
    if np.isnan(np.sum(bc)):
        continue
    barcode = "".join(["1" if a else "0" for a in bc])
    bcs.append(barcode)

barcs_occurr = {}
for barc in set(bcs):
    barcs_occurr[barc]=bcs.count(barc)
counts_sorted=np.array(sorted(list(barcs_occurr.values()), reverse=True))
barcs_sorted=[key for _,key in sorted(zip(list(barcs_occurr.values()),list(barcs_occurr.keys())),reverse=True)]
print(barcs_occurr)
print(len(bcs))

barcodes_for_display=["0000","0001","0010","0100","1000","0011","0101","0110","0111","1001","1010","1011","1100","1101","1110","1111"]
display_counts=[barcs_occurr[barc] if barc in barcs_occurr else 0 for barc in barcodes_for_display]

fig,ax=plt.subplots(figsize=(2.75,1.3))
counts_rates=display_counts/np.sum(counts_sorted)*100
errs=np.sqrt(counts_rates/100*(1-counts_rates/100)/((np.sum(counts_sorted)-1)))*100
ax.bar(np.arange(len(counts_rates)),counts_rates)
ax.errorbar(np.arange(len(counts_rates)),counts_rates,yerr=errs,ls='none',capsize=0.75/25.4*72,ecolor='k')
ax.set_xticks(np.arange(len(counts_rates)),barcodes_for_display,rotation=-90,ha='left',rotation_mode='anchor')
ax.set_ylim(bottom=0,top=100)
ax.set_yticks(np.arange(0,101,20))
ax.set_ylabel("occurrence rate /%")
ax.set_xlabel("barcode")
print(display_counts)

fig1,ax1=plt.subplots(figsize=(2.75,1.3))
counts_rates=np.array([0,25,25,25,25,0,0,0,0,0,0,0,0,0,0,0])
errs=np.sqrt(counts_rates/100*(1-counts_rates/100)/((np.sum(counts_sorted)-1)))*100
ax1.bar(np.arange(len(counts_rates)),counts_rates)
ax1.set_xticks(np.arange(len(counts_rates)),barcodes_for_display,rotation=-90,ha='left',rotation_mode='anchor')
ax1.set_ylim(bottom=0,top=100)
ax1.set_yticks(np.arange(0,101,20))
ax1.set_ylabel("occurrence rate /%")
ax1.set_xlabel("barcode")
print(display_counts)
plt.show()
