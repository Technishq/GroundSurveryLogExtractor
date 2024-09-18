#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd

# Load the CSV file
csv_file = 'finalmpmb.csv'
df = pd.read_csv(csv_file)

# Drop all columns except the specified ones
columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'Amplitude']
df = df[columns_to_keep]
#df.to_csv("finalmpmb.csv", sep=',', index=False, encoding='utf-8')


# Print the first few rows
print("Head of the file:")
print(df.head())

# Print the last few rows
print("\nTail of the file:")
print(df.tail())


# In[27]:


from datetime import datetime, timedelta

# Define the GPS epoch
GPS_EPOCH = datetime(1980, 1, 6)

def gps_to_utc(week, seconds):
    # Calculate the GPS time
    gps_time = GPS_EPOCH + timedelta(weeks=week, seconds=seconds)
    return gps_time

# Apply the conversion to the DataFrame
df['UTC Time'] = df.apply(lambda row: gps_to_utc(row['Week Number'], row['Seconds of Week']), axis=1)

# Convert 'UTC Time' to a 24-hour time format
df['24-hour Time'] = df['UTC Time'].dt.strftime('%H:%M')

# Print the first few rows to verify
print("Head of the file with 24-hour time format:")
print(df.head())


# In[28]:


# Round the "Seconds of Week" column to the nearest integer
#df['Seconds of Week'] = df['Seconds of Week'].round().astype(int)

# Normalize the "Seconds of Week" column by subtracting the first value
#first_seconds = df['Seconds of Week'].iloc[0]
#df['Seconds of Week'] = df['Seconds of Week'] - first_seconds

# Print the first few rows
#print("Head of the file:")
#print(df.head())

# Print the last few rows
#print("\nTail of the file:")
#print(df.tail())


# In[29]:


import numpy as np
# Replace zero or very small values of "Amplitude" to avoid log10 issues
df['Amplitude'] = df['Amplitude'].replace(0, np.nan)
df['Amplitude'] = df['Amplitude'].fillna(df['Amplitude'].min() / 2)

# Add a new column 'd/u' which is 20log10(Amplitude)
df['d/u'] = -1*20 * np.log10(df['Amplitude'])

# Print the first few rows
print("Head of the file:")
print(df.head())

# Print the last few rows
print("\nTail of the file:")
print(df.tail())


# In[30]:


import plotly.io as pio
pio.renderers.default = "iframe"
# Ask user to input a specific PRN
import plotly.express as px
import plotly.graph_objects as go
# Plot d/u values against 24-hour time for all PRNs together
fig = go.Figure()

# Add traces for each PRN
for prn in df['PRN'].unique():
    group = df[df['PRN'] == prn]
    fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['d/u'], mode='lines', name=f'PRN {prn}'))

# Update layout
fig.update_layout(
    title='d/u values for all PRNs',
    xaxis_title='Time (24-hour format)',
    yaxis_title='d/u (dB)',
    xaxis_tickformat='%H:%M:'
)

# Show the figure
fig.show()


# In[ ]:


#grouped = df.groupby('PRN')
grouped = df.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
grouped = df.groupby('PRN')

# Print the head and tail of each group
for prn, group in grouped:
    print(f"\nPRN: {prn}")
    print("Head of the group:")
    print(group.head())
    print("\nTail of the group:")
    print(group.tail())


# In[32]:


import plotly.io as pio
pio.renderers.default = "iframe"


# In[33]:


# Ask user to input a specific PRN
import plotly.express as px
import plotly.graph_objects as go
specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))

# Plot d/u values against 24-hour time for the specific PRN
if specific_prn in grouped.groups:
    group = grouped.get_group(specific_prn)
    fig = px.line(group, x='24-hour Time', y='d/u', title=f'd/u values for PRN {specific_prn}')
    fig.update_layout(
        xaxis_title='Time (24-hour format)',
        yaxis_title='d/u (dB)',
        xaxis_tickformat='%H:%M:%S'
    )
    fig.show()
else:
    print(f"PRN {specific_prn} not found in the dataset.")


# In[34]:


# Count the number of values below 16
count_below_16 = df["d/u"][df["d/u"] < 16].count()

# Calculate the total number of values in the column
total_values = df["d/u"].count()

# Calculate the percentage of values below 16
percentage_below_16 = (count_below_16 / total_values) * 100



# In[35]:


# Count the number of values below 20
count_below_20= df["d/u"][df["d/u"] < 20].count()

# Calculate the total number of values in the column
total_values = df["d/u"].count()

# Calculate the percentage of values below 16
percentage_below_20 = (count_below_20 / total_values) * 100



# In[36]:


# Count the number of values >= 20
count_eqgt_20= df["d/u"][df["d/u"] >= 20].count()

# Calculate the total number of values in the column
total_values = df["d/u"].count()

# Calculate the percentage of values below 16
percentage_eqgt_20 = (count_eqgt_20 / total_values) * 100
print(f"Percentage of d/u values below 16: {percentage_below_16:.2f}%")
print(f"Percentage of d/u values below 20: {percentage_below_20:.2f}%")
print(f"Percentage of d/u values >= 20: {percentage_eqgt_20:.2f}%")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




