# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:37:07 2020

@author: rayde
"""

#!pip install EIA-python
#!pip install networkx
import numpy as np 
import pandas as pd
import eia
import networkx as nx
import matplotlib.pyplot as plt


apiKey = "5f54b3e66477e22ec068066b1de8026d"
api = eia.API(apiKey)

url = "http://api.eia.gov/geoset/?geoset_id=sssssss&regions=region1,region2,region3,...&api_key={0}[&start=|&num=][&end=][&out=xml|json]".format(api)

series_id_list = ["INTL.57-1-DZA-TBPD.M", "INTL.57-1-AGO-TBPD.M", "INTL.57-1-COG-TBPD.M", "INTL.57-1-COD-TBPD.M", 
                  "INTL.57-1-ECU-TBPD.M","INTL.57-1-GNQ-TBPD.M","INTL.57-1-GAB-TBPD.M","INTL.57-1-IRN-TBPD.M",
                  "INTL.57-1-IRQ-TBPD.M", "INTL.57-1-KWT-TBPD.M", "INTL.57-1-LBY-TBPD.M", "INTL.57-1-NGA-TBPD.M",
                  "INTL.57-1-QAT-TBPD.M", "INTL.57-1-RUS-TBPD.M", "INTL.57-1-SAU-TBPD.M","INTL.57-1-ARE-TBPD.M",
                  "INTL.57-1-VEN-TBPD.M", "INTL.57-1-USA-TBPD.M"]

df_list = [pd.DataFrame(api.data_by_series(series)) for series in series_id_list]

oil_data = pd.concat(df_list, axis=1)

oil_data = oil_data.replace("--", np.nan)

 
oil_data.dropna().shape

 
oil_data.shape

 
oil_data_reduced = oil_data.dropna()

 
oil_data_reduced

 
oil_data_reduced.columns = ["Algeria", "Angola", "Congo-Brazzaville", "Congo-Kinshasa", "Ecuador", "Equatorial Guinea", "Gabon", "Iran",
                "Iraq", "Kuwait", "Libya", "Nigeria", "Qatar", "Russia", "Saudi Arabia", "United Arab Emirates", "Venezuela", "USA"]
corrs = oil_data_reduced.corr()

 
corrs[(corrs>=.5) | (corrs<=-.5) & (corrs!=1)]

 
# Transform it in a links data frame (3 columns only):
links = corrs.stack().reset_index()
links

 
links.columns = ['var1', 'var2','value']
len(links['var1'].unique())

 
# Keep only correlation over a threshold and remove self correlation (cor(A,A)=1)
links_filtered=links.loc[ (links['value'] > 0.5) & (links['var1'] != links['var2']) ]

 
all_links = nx.from_pandas_edgelist(links_filtered, 'var1', 'var2')


pos = nx.circular_layout(all_links)

labels = list(pos.keys())
labels = dict(zip(labels, labels))

pos_higher = {}

for k, v in pos.items():
    if(v[1]>0):
        pos_higher[k] = (v[0], v[1]+0.06)
    else:
        pos_higher[k] = (v[0], v[1]-0.06)
        
pos_higher['Congo-Kinshasa'] = (pos_higher['Congo-Kinshasa'][0]+.05, pos_higher['Congo-Kinshasa'][1])
pos_higher['Algeria'] = (pos_higher['Algeria'][0]+.05, pos_higher['Algeria'][1]+.1)


fig, ax = plt.subplots(figsize=(20,20))
margin=.05
fig.subplots_adjust(margin, margin, 1.-margin, 1.-margin)
ax.axis('equal')
nx.draw(all_links, pos =pos, edge_color='black')
nx.draw_networkx_labels(all_links, pos_higher,labels)
plt.savefig("positive_correlation.jpg")

 
list(nx.shortest_path_length(all_links))

 
links_filtered['var1'].value_counts()

 
links_filtered=links.loc[ (links['value'] < -0.5) & (links['var1'] != links['var2']) ]

 
all_links = nx.from_pandas_edgelist(links_filtered, 'var1', 'var2')


pos = nx.circular_layout(all_links)

labels = list(pos.keys())
labels = dict(zip(labels, labels))

pos_higher = {}

for k, v in pos.items():
    if(v[1]>0):
        pos_higher[k] = (v[0], v[1]+0.06)
    else:
        pos_higher[k] = (v[0], v[1]-0.06)
        
pos_higher['Congo-Kinshasa'] = (pos_higher['Congo-Kinshasa'][0]+.05, pos_higher['Congo-Kinshasa'][1])
pos_higher['Algeria'] = (pos_higher['Algeria'][0]+.05, pos_higher['Algeria'][1]+.1)


fig, ax = plt.subplots(figsize=(20,20))
margin=.05
fig.subplots_adjust(margin, margin, 1.-margin, 1.-margin)
ax.axis('equal')
nx.draw(all_links, pos =pos, edge_color='black')
nx.draw_networkx_labels(all_links, pos_higher,labels)
plt.savefig("negative_correlation.jpg")

 
eccentricity = nx.eccentricity(all_links)
ecc_df = pd.DataFrame.from_dict(eccentricity, orient='index', columns=['Eccentricity']).rename_axis('Country', axis='index')
ecc_df.sort_values(by='Eccentricity', ascending=False)

 
nx.diameter(all_links, e=eccentricity)

 
list(nx.shortest_path_length(all_links))

 