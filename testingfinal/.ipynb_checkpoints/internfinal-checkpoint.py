import struct
import csv

def parse_gps_binary(file_path):
    records = []
    
    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break  # End of file reached
            
            message_id, = struct.unpack('I', sync_header)
            if message_id != 95:
                continue  # Not a $MPMA message, skip
            
            # Read the rest of the MPMA message
            message_byte_count, = struct.unpack('I', bin_file.read(4))
            
            # Read the data fields
            week_number, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            prn, = struct.unpack('I', bin_file.read(4))
            channel_status, = struct.unpack('I', bin_file.read(4))
            medll_status, = struct.unpack('I', bin_file.read(4))
            delay, = struct.unpack('f', bin_file.read(4))
            amplitude, = struct.unpack('f', bin_file.read(4))
            phase, = struct.unpack('f', bin_file.read(4))
            
            in_phase_residuals = []
            out_of_phase_residuals = []
            
            for _ in range(12):
                in_phase_residuals.append(struct.unpack('f', bin_file.read(4))[0])
            for _ in range(12):
                out_of_phase_residuals.append(struct.unpack('f', bin_file.read(4))[0])
            
            records.append([
                week_number, seconds_of_week, prn, channel_status, medll_status,
                delay, amplitude, phase,
                *in_phase_residuals, *out_of_phase_residuals
            ])
    
    return records

def write_to_csv1(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'PRN', 'Channel Status', 'MEDLL Status',
        'Delay', 'Amplitude', 'Phase',
        '1st In Phase Residual', '2nd In Phase Residual', '3rd In Phase Residual',
        '4th In Phase Residual', '5th In Phase Residual', '6th In Phase Residual',
        '7th In Phase Residual', '8th In Phase Residual', '9th In Phase Residual',
        '10th In Phase Residual', '11th In Phase Residual', '12th In Phase Residual',
        '1st Out of Phase Residual', '2nd Out of Phase Residual', '3rd Out of Phase Residual',
        '4th Out of Phase Residual', '5th Out of Phase Residual', '6th Out of Phase Residual',
        '7th Out of Phase Residual', '8th Out of Phase Residual', '9th Out of Phase Residual',
        '10th Out of Phase Residual', '11th Out of Phase Residual', '12th Out of Phase Residual'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)


def parse_sata_binary(file_path):
    records = []
    
    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(3)
            if len(sync_header) < 3:
                break  # End of file reached
            
            # Read the checksum
            checksum = bin_file.read(1)
            if len(checksum) < 1:
                break  # End of file reached
            
            # Read the message ID
            message_id_data = bin_file.read(4)
            if len(message_id_data) < 4:
                break  # End of file reached
            message_id, = struct.unpack('I', message_id_data)
            if message_id != 12:
                continue  # Not a SATB message, skip
            
            # Read the message byte count
            message_byte_count_data = bin_file.read(4)
            if len(message_byte_count_data) < 4:
                break  # End of file reached
            message_byte_count, = struct.unpack('I', message_byte_count_data)
            
            # Read the rest of the fields
            week_number_data = bin_file.read(4)
            if len(week_number_data) < 4:
                break  # End of file reached
            week_number, = struct.unpack('I', week_number_data)
            
            seconds_of_week_data = bin_file.read(8)
            if len(seconds_of_week_data) < 8:
                break  # End of file reached
            seconds_of_week, = struct.unpack('d', seconds_of_week_data)
            
            solution_status_data = bin_file.read(4)
            if len(solution_status_data) < 4:
                break  # End of file reached
            solution_status, = struct.unpack('I', solution_status_data)
            
            num_observations_data = bin_file.read(4)
            if len(num_observations_data) < 4:
                break  # End of file reached
            num_observations, = struct.unpack('I', num_observations_data)
            
            observations = []
            for _ in range(num_observations):
                prn_data = bin_file.read(4)
                if len(prn_data) < 4:
                    break  # End of file reached
                prn, = struct.unpack('I', prn_data)
                
                azimuth_data = bin_file.read(8)
                if len(azimuth_data) < 8:
                    break  # End of file reached
                azimuth, = struct.unpack('d', azimuth_data)
                
                elevation_data = bin_file.read(8)
                if len(elevation_data) < 8:
                    break  # End of file reached
                elevation, = struct.unpack('d', elevation_data)
                
                residual_data = bin_file.read(8)
                if len(residual_data) < 8:
                    break  # End of file reached
                residual, = struct.unpack('d', residual_data)
                
                reject_code_data = bin_file.read(4)
                if len(reject_code_data) < 4:
                    break  # End of file reached
                reject_code, = struct.unpack('I', reject_code_data)
                
                observations.append([
                    prn, azimuth, elevation, residual, reject_code
                ])
            
            records.append([
                week_number, seconds_of_week, solution_status, num_observations,
                observations
            ])
    
    return records

def write_to_csv2(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'Solution Status', 'Number of Observations',
        'PRN', 'Azimuth', 'Elevation', 'Residual', 'Reject Code'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        
        for record in records:
            week_number, seconds_of_week, solution_status, num_observations, observations = record
            for observation in observations:
                csv_writer.writerow([
                    week_number, seconds_of_week, solution_status, num_observations,
                    *observation
                ])

import struct
import csv

def parse_eats_binary(file_path):
    records = []

    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break  # End of file reached

            message_id, = struct.unpack('I', sync_header)
            if message_id != 48:
                continue  # Not an ETSB message, skip

            # Read the message byte count
            message_byte_count, = struct.unpack('I', bin_file.read(4))

            # Read the fixed part of the message
            week_number, = struct.unpack('I', bin_file.read(4))
            time_of_week, = struct.unpack('d', bin_file.read(8))
            solution_status, = struct.unpack('I', bin_file.read(4))
            num_channels, = struct.unpack('I', bin_file.read(4))

            # Read channel-specific data
            for _ in range(num_channels):
                prn_number, = struct.unpack('I', bin_file.read(4))
                channel_tracking_status, = struct.unpack('I', bin_file.read(4))
                doppler, = struct.unpack('d', bin_file.read(8))
                cn0, = struct.unpack('d', bin_file.read(8))
                residual, = struct.unpack('d', bin_file.read(8))
                locktime, = struct.unpack('d', bin_file.read(8))
                pseudorange, = struct.unpack('d', bin_file.read(8))
                rejection_code, = struct.unpack('I', bin_file.read(4))

                records.append([
                    week_number, time_of_week, solution_status, num_channels,
                    prn_number, channel_tracking_status, doppler, cn0,
                    residual, locktime, pseudorange, rejection_code
                ])

    return records

def write_to_csv3(records, csv_path):
    headers = [
        'Week Number', 'Time of Week', 'Solution Status', 'Number of Channels',
        'PRN Number', 'Channel Tracking Status', 'Doppler', 'C/N0',
        'Residual', 'Locktime', 'Pseudorange', 'Rejection Code'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)




def main():
    print("Input Binary File Path")
    binary_file_path = input()  # Path to the binary GPS file

    csv_file_path = 'mpmbfinal.csv'     # Path to the output CSV file
    print("Please wait while the bin file converts to CSVs")

    records1= parse_gps_binary(binary_file_path)
    write_to_csv1(records1, csv_file_path)
    print(f"MPMB Data successfully converted from {binary_file_path} to {csv_file_path}")

    records2 = parse_sata_binary(binary_file_path)
    write_to_csv2(records2, csv_file_path)


    print(f"SATA data successfully converted from {binary_file_path} to {csv_file_path}")
    
    records3 = parse_eats_binary(binary_file_path)
    write_to_csv3(records3, csv_file_path)

    print(f"EATSA Data successfully converted from {binary_file_path} to {csv_file_path}")
if __name__ == '__main__':
    main()





#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pandas as pd

# Load the CSV file
csv_file = 'mpmbfinal.csv'
#print ("Please enter csv file location")
#csv_file = input()
df = pd.read_csv(csv_file)

# Drop all columns except the specified ones
columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'Amplitude']
df = df[columns_to_keep]
#df.to_csv("finalmpmb.csv", sep=',', index=False, encoding='utf-8')


# Print the first few rows
#print("Head of the file:")
#print(df.head())

# Print the last few rows
#print("\nTail of the file:")
#print(df.tail())


# In[38]:


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
#print("Head of the file with 24-hour time format:")
#print(df.head())


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


# In[39]:


import numpy as np
# Replace zero or very small values of "Amplitude" to avoid log10 issues
df['Amplitude'] = df['Amplitude'].replace(0, np.nan)
df['Amplitude'] = df['Amplitude'].fillna(df['Amplitude'].min() / 2)

# Add a new column 'd/u' which is 20log10(Amplitude)
df['d/u'] = -1*20 * np.log10(df['Amplitude'])

# Print the first few rows
#print("Head of the file:")
#print(df.head())

# Print the last few rows
#print("\nTail of the file:")
#print(df.tail())


# In[40]:

import plotly
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
plotly.offline.plot(fig, filename='plotlyplots/default.html')



# In[43]:


#grouped = df.groupby('PRN')
grouped = df.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
grouped = df.groupby('PRN')

# Print the head and tail of each group
"""
for prn, group in grouped:
    print(f"\nPRN: {prn}")
    print("Head of the group:")
    print(group.head())
    print("\nTail of the group:")
    print(group.tail())
"""    


# In[44]:


import plotly.io as pio
pio.renderers.default = "iframe"


# In[33]:


# Ask user to input a specific PRN
import plotly
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
    plotly.offline.plot(fig, filename='plotlyplots/specific_prn.html')

else:
    print(f"PRN {specific_prn} not found in the dataset.")


# In[45]:


# Count the number of values below 16
count_below_16 = df["d/u"][df["d/u"] < 16].count()

# Calculate the total number of values in the column
total_values = df["d/u"].count()

# Calculate the percentage of values below 16
percentage_below_16 = (count_below_16 / total_values) * 100



# In[46]:


# Count the number of values below 20
count_below_20= df["d/u"][df["d/u"] < 20].count()

# Calculate the total number of values in the column
total_values = df["d/u"].count()

# Calculate the percentage of values below 16
percentage_below_20 = (count_below_20 / total_values) * 100



# In[47]:


# Count the number of values >= 20
count_eqgt_20= df["d/u"][df["d/u"] >= 20].count()

# Calculate the total number of values in the column
total_values = df["d/u"].count()

# Calculate the percentage of values below 16
percentage_eqgt_20 = (count_eqgt_20 / total_values) * 100
print(f"Percentage of d/u values below 16: {percentage_below_16:.2f}%")
print(f"Percentage of d/u values below 20: {percentage_below_20:.2f}%")
print(f"Percentage of d/u values >= 20: {percentage_eqgt_20:.2f}%")


