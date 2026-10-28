import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import h5py as h5
import matplotlib as mpl
font = {'family' : 'Gill Sans',
        'weight' : 'regular',
        'size'   : 10}
mpl.rc('font',**font)
mpl.rcParams['axes.titlesize'] = 10
mpl.rcParams['figure.titlesize'] = 10

df = pd.read_pickle(r"/Users/maxearle/Library/CloudStorage/OneDrive-Personal/cambridge_stuff/Error_Protection_Data/mismatch_protectors/1min/checked_assignments_from_peak_assignments_for_propsfilt1.pkl")
data_loc = r"/Users/maxearle/Library/CloudStorage/OneDrive-Personal/cambridge_stuff/Error_Protection_Data/mismatch_protectors/1min/EVENTS.hdf5"

with h5.File(data_loc,'r') as f:
    group = f["current_data"]
    dataset_names = list(group.keys())

print(df)
bcs = {}
for index, row in df.iterrows():
    name = row.iloc[0]
    bc = np.array(row.iloc[1:])
    if np.isnan(np.sum(bc)):
        bcs[name] = None
        continue
    barcode = "".join(["1" if a else "0" for a in bc])
    bcs[name] = barcode

bc_of_i = '0000'
keys = list(bcs.keys())
bcs_list = list(bcs.values())
print(bcs_list)
names=[name for name,bc in zip(keys,bcs_list) if bc==bc_of_i]

with h5.File(data_loc,'r') as f:
    group = f["current_data"]
    datasets = [np.array(group[name][:]) for name in names]
    dataset_names = [name for name in names]

a4_width_in = 210/25.4
margin_in = 1.0
fig,ax = plt.subplots(5,3,figsize=(a4_width_in-2*margin_in,4.8),sharex=True,sharey=True)
for i,dataset in enumerate(datasets[:15]):
    ax[i//3,i%3].plot(dataset,lw=0.35/25.4*72)
    ax[i//3,i%3].set_title(dataset_names[i].replace("_"," "))
    ax[i//3,i%3].axis('off')

# scale bar in the bottom-right subplot; 1 MHz sampling so 1 sample = 1 us, trace values in nA
sb_len_us = 500
sb_height_nA = 0.1
sample_period_us = 1
sb_ax = ax[-1,-1]
x_right = sb_ax.get_xlim()[1]
y_bottom = sb_ax.get_ylim()[0]
sb_len = sb_len_us/sample_period_us
sb_ax.plot([x_right-sb_len,x_right,x_right],[y_bottom,y_bottom,y_bottom+sb_height_nA],
           color='k',lw=0.35/25.4*72,solid_capstyle='butt',clip_on=False)
sb_ax.text(x_right-sb_len/2,y_bottom,f"{sb_len_us} µs",ha='center',va='top')
sb_ax.text(x_right,y_bottom+sb_height_nA/2,f"{sb_height_nA} nA",ha='left',va='center',rotation=90)
fig.suptitle("Events with barcode " + bc_of_i)
fig.tight_layout()
plt.show()