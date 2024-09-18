#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd

# Load the CSV file
csv_file1 = 'sata.csv'
csv_file2 = 'mpmbfinal.csv'
df1 = pd.read_csv(csv_file1)

columns_to_keep1 = ['Week Number', 'Seconds of Week', 'PRN', 'Elevation']

df1=df1[columns_to_keep1]
# ##print the first few rows
###print("Head of the file:")
###print(df1.head())

# ##print the last few rows
###print("\nTail of the file:")
###print(df1.tail())



df2 = pd.read_csv(csv_file2)

# Drop all columns except the specified ones
columns_to_keep2 = ['Week Number', 'Seconds of Week', 'PRN', 'Amplitude']
df2 = df2[columns_to_keep2]
#df.to_csv("finalmpmb.csv", sep=',', index=False, encoding='utf-8')


# ##print the first few rows
##print("Head of the file:")
##print(df2.head())

# ##print the last few rows
##print("\nTail of the file:")
##print(df2.tail())



# In[5]:


# ##print the first few rows
##print("Head of the file:")
##print(df1.head())

# ##print the last few rows
##print("\nTail of the file:")
##print(df1.tail())
import numpy as np
# Replace zero or very small values of "Amplitude" to avoid log10 issues
df2['Amplitude'] = df2['Amplitude'].replace(0, np.nan)
df2['Amplitude'] = df2['Amplitude'].fillna(df2['Amplitude'].min() / 2)

# Add a new column 'd/u' which is 20log10(Amplitude)
df2['d/u'] = 20 * np.log10(df2['Amplitude'])

# ##print the first few rows
##print("Head of the file:")
##print(df2.head())

# ##print the last few rows
##print("\nTail of the file:")
##print(df2.tail())


df1.rename(columns={'PRN Number': 'PRN'}, inplace=True)


# In[7]:


from datetime import datetime, timedelta

# Define the GPS epoch
GPS_EPOCH = datetime(1980, 1, 6)

def gps_to_utc(week, seconds):
    # Calculate the GPS time
    gps_time = GPS_EPOCH + timedelta(weeks=week, seconds=seconds)
    return gps_time

# Apply the conversion to the DataFrame
df2['UTC Time'] = df2.apply(lambda row: gps_to_utc(row['Week Number'], row['Seconds of Week']), axis=1)
df1['UTC Time'] = df1.apply(lambda row: gps_to_utc(row['Week Number'], row['Seconds of Week']), axis=1)

# Convert 'UTC Time' to a 24-hour time format
df1['Time'] = df1['UTC Time'].dt.strftime('%H:%M:%S')
df2['Time'] = df2['UTC Time'].dt.strftime('%H:%M:%S')

# ##print the first few rows to verify
##print("Head of the file with 24-hour time format:")
##print(df1.head())
##print("Head of the file with 24-hour time format:")
##print(df2.head())



# In[8]:


#grouped = df.groupby('PRN')
grouped1 = df1.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
grouped2 = df2.sort_values(by=['PRN', 'Time']).reset_index(drop=True)

##print (grouped1)
##print (grouped2)


# In[9]:


# ##print unique combinations of 'PRN' and 'Time' in df1 and df2
##print("\nUnique combinations in df1:")
##print(grouped1[['PRN', 'Time']].drop_duplicates())
##print("\nUnique combinations in df2:")
##print(grouped2[['PRN', 'Time']].drop_duplicates())


# In[10]:


##print("Column names of df1:", grouped1.columns.tolist())
##print("Column names of df2:", grouped2.columns.tolist())

try:
    df_merged = grouped2.merge(grouped1[['PRN', 'Elevation', 'Time']], on=['PRN', 'Time'], how='left')
    print("Merging successful.")
except KeyError as e:
    print(f"KeyError: {e}")



#print (df_merged)


# In[12]:


#df_merged.to_csv("testingforcno.csv", sep=',', index=False, encoding='utf-8')
#grouped = df.groupby('PRN')
grouped= df_merged.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
grouped= df_merged.groupby('PRN')

# #print the head and tail of each group
#for prn, group in grouped:
    #print(f"\nPRN: {prn}")
    #print("Head of the group:")
    #print(group.head())
    #print("\nTail of the group:")
    #print(group.tail())


# In[13]:


import plotly.io as pio
pio.renderers.default = "iframe"


# In[15]:


import plotly.io as pio
pio.renderers.default = "iframe"

import plotly.graph_objects as go

# Plot d/u values against 24-hour time for all PRNs together
fig = go.Figure()

# Add traces for each PRN for d/u values
for prn in df_merged['PRN'].unique():
    group = df_merged[df_merged['PRN'] == prn]
    fig.add_trace(go.Scatter(x=group['Time'], y=group['d/u'], mode='lines', name=f'PRN {prn} - d/u '))

# Add traces for each PRN for C/N0 values (secondary y-axis)
for prn in df_merged['PRN'].unique():
    group = df_merged[df_merged['PRN'] == prn]
    fig.add_trace(go.Scatter(x=group['Time'], y=group['Elevation'], mode='lines', name=f'PRN {prn} - C/N0', yaxis='y2'))

# Update layout with dual y-axes
fig.update_layout(
    title='d/u values and Eleavation for all PRNs',
    xaxis_title='Time (24-hour format)',
    yaxis_title='d/u (dB)',
    yaxis2=dict(
        title='Eleavtion',
        overlaying='y',
        side='right'
    ),
    xaxis_tickformat='%H:%M'
)

# Show the figure
fig.show()


# In[16]:


import plotly.express as px
import plotly.graph_objects as go



import plotly.graph_objects as go

specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))

# Plot d/u values against 24-hour time for the specific PRN
if specific_prn in grouped.groups:
   
    # Assuming you have defined 'group' and 'specific_prn'
    
    fig = go.Figure()
    
    # Add d/u values
    fig.add_trace(go.Scatter(x=group['Time'], y=group['d/u'], mode='lines', name='d/u'))
    
    # Add C/N0 values
    fig.add_trace(go.Scatter(x=group['Time'], y=group['Elevation'], mode='lines', name='C/N0', yaxis='y2'))
    
    # Update layout to have two y-axes
    fig.update_layout(
        title=f'd/u and C/N0 values for PRN {specific_prn}',
        xaxis_title='Time (24-hour format)',
        xaxis_tickformat='%H:%M:%S',
        yaxis=dict(
            title='d/u (dB)',
            titlefont=dict(
                color='blue'
            ),
            tickfont=dict(
                color='blue'
            )
        ),
        yaxis2=dict(
            title='Elevation',
            titlefont=dict(
                color='green'
            ),
            tickfont=dict(
                color='green'
            ),
            overlaying='y',
            side='right'
        )
    )
    
    fig.show()

else:
    print(f"PRN {specific_prn} not found in the dataset.")


# In[ ]:





