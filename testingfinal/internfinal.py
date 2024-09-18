import struct
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import csv
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly
import os
pio.renderers.default = "iframe"

path ="plots"

def parse_gps_binary(file_path1):
    records = []
    
    # Open the binary file in read mode
    with open(file_path1, 'rb') as bin_file:
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

def write_to_csv1(records, csv_path1):
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

    with open (csv_path1, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def parse_sata_binary(file_path2):
    records = []
    
    # Open the binary file in read mode
    with open(file_path2, 'rb') as bin_file:
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

def write_to_csv2(records, csv_path2):
    headers = [
        'Week Number', 'Seconds of Week', 'Solution Status', 'Number of Observations',
        'PRN', 'Azimuth', 'Elevation', 'Residual', 'Reject Code'
    ]

    with open(csv_path2, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        
        for record in records:
            week_number, seconds_of_week, solution_status, num_observations, observations = record
            for observation in observations:
                csv_writer.writerow([
                    week_number, seconds_of_week, solution_status, num_observations,
                    *observation
                ])

def test_sata(file_path2, output_file):
    # Define the format for the header
    header_format = '3s B I I I d I I'
    header_size = struct.calcsize(header_format)

    # Define the format for the observations with little-endian byte order
    observation_format = '<I d d d I'
    observation_size = struct.calcsize(observation_format)

    # Open the binary file for reading and CSV file for writing
    with open(file_path2, 'rb') as bin_file, open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write CSV header
        csv_writer.writerow(['Week Number', 'Seconds of Week', 'Solution Status', 'Number of Observations', 
                             'PRN', 'Azimuth', 'Elevation', 'Residual', 'Reject Code'])

        while True:
            # Read the header
            header_data = bin_file.read(header_size)
            if len(header_data) < header_size:
                break  # End of file or incomplete header

            try:
                # Unpack the header
                sync, checksum, message_id, byte_count, week_number, seconds_of_week, \
                solution_status, num_observations = struct.unpack(header_format, header_data)

                # Debug print for the header
                #print(f"Header - Sync: {sync}, Checksum: {checksum}, Message ID: {message_id}, Byte Count: {byte_count}, Week Number: {week_number}, Seconds of Week: {seconds_of_week}, Solution Status: {solution_status}, Number of Observations: {num_observations}")

                # Validate the data
                if message_id != 12:
                    #print(f"Unexpected message ID: {message_id}")
                    # Skip to the next header based on byte_count
                    bin_file.seek(byte_count - header_size, 1)
                    continue

                for _ in range(num_observations):
                    observation_data = bin_file.read(observation_size)
                    if len(observation_data) < observation_size:
                        #print("Incomplete observation data")
                        break  # End of observations or incomplete observation

                    try:
                        # Unpack the observation
                        prn, azimuth, elevation, residual, reject_code = struct.unpack(observation_format, observation_data)

                        # Debug print for the observation
                        #print(f"Observation - PRN: {prn}, Azimuth: {azimuth}, Elevation: {elevation}, Residual: {residual}, Reject Code: {reject_code}")

                        # Write the data to the CSV file
                        csv_writer.writerow([week_number, seconds_of_week, solution_status, num_observations, 
                                             prn, azimuth, elevation, residual, reject_code])
                    except struct.error as e:
                        #print(f"Error unpacking observation: {e}")
                        continue  # Skip to the next observation
            except struct.error as e:
                #print(f"Error unpacking header: {e}")
                continue  # Skip to the next header

def parse_eats_binary(file_path3):
    records = []

    # Open the binary file in read mode
    with open(file_path3, 'rb') as bin_file:
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

def write_to_csv3(records, csv_path3):
    headers = [
        'Week Number', 'Seconds of Week', 'Solution Status', 'Number of Channels',
        'PRN', 'Channel Tracking Status', 'Doppler', 'C/N0',
        'Residual', 'Locktime', 'Pseudorange', 'Rejection Code'
    ]

    with open(csv_path3, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)
def clear_screen():
    # Check if the operating system is Windows or Unix-like
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For Unix-like systems (Linux, macOS, etc.)
        _ = os.system('clear')



def Populating_mpmb_df():
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
    return df
def Populating_cnot_df():

    csv_file = 'etsa.csv'
    df = pd.read_csv(csv_file)


    # Print the last few rows
    print("\nTail of the file:")
    print(df.tail())

    # Drop all columns except the specified ones
    columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'C/N0']
    df = df[columns_to_keep]





    # Define the GPS epoch
    GPS_EPOCH = datetime(1980, 1, 6)

    def gps_to_utc(week, seconds):
        # Calculate the GPS time
        gps_time = GPS_EPOCH + timedelta(weeks=week, seconds=seconds)
        return gps_time

    # Apply the conversion to the DataFrame
    df['UTC Time'] = df.apply(lambda row: gps_to_utc(row['Week Number'], row['Seconds of Week']), axis=1)

    # Convert 'UTC Time' to a 24-hour time format
    df['24-hour Time'] = df['UTC Time'].dt.strftime('%H:%M:%S')

    return df
def Populating_elev_df():
    csv_file = 'sata.csv'
    df = pd.read_csv(csv_file)

    # Print the last few rows
    
    # Drop all columns except the specified ones
    columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'Elevation']
    df = df[columns_to_keep]
    df = df[df['Seconds of Week'] >= 0]
    
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
    df['24-hour Time'] = df['UTC Time'].dt.strftime('%H:%M:%S')
    print("\nTail of the file:")
    print(df.tail())
    return df

def Populating_residual_df():
    csv_file = 'sata.csv'
    df = pd.read_csv(csv_file)

    # Print the last few rows
    
    # Drop all columns except the specified ones
    columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'Residual']
    df = df[columns_to_keep]
    df = df[df['Seconds of Week'] >= 0]
    
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
    df['24-hour Time'] = df['UTC Time'].dt.strftime('%H:%M:%S')
    print("\nTail of the file:")
    print(df.tail())
    return df

def Populating_combinedcnodu_df():

    # Load the CSV file
    csv_file1 = 'etsa.csv'
    csv_file2 = 'mpmbfinal.csv'
    df1 = pd.read_csv(csv_file1)

    df2 = pd.read_csv(csv_file2)

    # Drop all columns except the specified ones
    columns_to_keep1 = ['Week Number', 'Seconds of Week', 'PRN', 'Amplitude']
    df2 = df2[columns_to_keep1]
    #df.to_csv("finalmpmb.csv", sep=',', index=False, encoding='utf-8')

    # Drop all columns except the specified ones
    columns_to_keep2 = ['Week Number', 'Seconds of Week', 'PRN', 'C/N0']
    df1 = df1[columns_to_keep2]


    df2['Amplitude'] = df2['Amplitude'].replace(0, np.nan)
    df2['Amplitude'] = df2['Amplitude'].fillna(df2['Amplitude'].min() / 2)

    # Add a new column 'd/u' which is 20log10(Amplitude)
    df2['d/u'] = 20 * np.log10(df2['Amplitude'])

    
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
    df1['24-hour Time'] = df1['UTC Time'].dt.strftime('%H:%M:%S')
    df2['24-hour Time'] = df2['UTC Time'].dt.strftime('%H:%M:%S')

    # Print the first few rows to verify
    print("Head of the file with 24-hour time format:")
    print(df1.head())
    print("Head of the file with 24-hour time format:")
    print(df2.head())


    yield df1
    yield df2

def Populating_combinedelevdu_df():
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



        df2['Amplitude'] = df2['Amplitude'].replace(0, np.nan)
        df2['Amplitude'] = df2['Amplitude'].fillna(df2['Amplitude'].min() / 2)

        # Add a new column 'd/u' which is 20log10(Amplitude)
        df2['d/u'] = 20 * np.log10(df2['Amplitude'])
        from datetime import datetime, timedelta

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

        df1.rename(columns={'PRN Number': 'PRN'}, inplace=True)


# In[7]:
        yield df1
        yield df2






def plotingfinals():






    def duvt():


        print('Please Wait while MPMB Data gets loaded...')
        df= Populating_mpmb_df()
        print('Data Loaded Plotting Graph...')
        print("Do you want plot for specific PRN?")

        choice = input("Enter Y or N: ")

        if choice in {'Y','YES','yes','Yes','y'}:
            specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))
            #grouped = df.groupby('PRN')
            grouped = df.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped = df.groupby('PRN')
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
                plotly.offline.plot(fig, filename=f'plots/du_prn={specific_prn}.html')
                menu1()
            else:
                print(f"PRN {specific_prn} not found in the dataset.")
                menu1()

        elif choice in {'N','no','NO','No','n'}:
            
            pio.renderers.default = "iframe"
            # Ask user to input a specific PRN

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
            plotly.offline.plot(fig, filename='plots/DUvsTforall.html')





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
            menu1()
        else :
            print ("Invalid Input , Please Try Again")
            menu1()

    def cnot ():
        fig = go.Figure()
        print('Please Wait while ETSA Data gets loaded...')

        df= Populating_cnot_df()

        print("Do you want plot for specific PRN?")

        choice = input("Enter Y or N: ")

        if choice in {'Y','YES','yes','Yes','y'}:
            specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))
            #grouped = df.groupby('PRN')
            grouped = df.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped = df.groupby('PRN')
            # Plot d/u values against 24-hour time for the specific PRN
            if specific_prn in grouped.groups:
                group = grouped.get_group(specific_prn)
                fig = px.line(group, x='24-hour Time', y='C/N0', title=f'd/u values for PRN {specific_prn}')
                fig.update_layout(
                    xaxis_title='Time (24-hour format)',
                    yaxis_title='C/N0)',
                    xaxis_tickformat='%H:%M:%S'
                )
                fig.show()
                plotly.offline.plot(fig, filename=f'plots/cno_prn={specific_prn}.html')
                menu1()
            else:
                print(f"PRN {specific_prn} not found in the dataset.")
                menu1()

        elif choice in {'N','no','NO','No','n'}:

        
            print('Data Loaded Plotting Graph...')

            # Add traces for each PRN
            for prn in df['PRN'].unique():
                group = df[df['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['C/N0'], mode='lines', name=f'PRN {prn}'))

            # Update layout
            fig.update_layout(
                title='d/u values for all PRNs',
                xaxis_title='Time (24-hour format)',
                yaxis_title='C/N0',
                xaxis_tickformat='%H:%M:%S'
            )

            # Show the figure
            fig.show()
            plotly.offline.plot(fig, filename='plots/CN0vsTime_For_all.html')

            grouped = df.groupby('PRN')
            menu1()
        else:
                print ("Invalid Input , Please Try Again")
                menu1()


    def elev():
        pio.renderers.default = "iframe"
        print('Please Wait while SATA Data gets loaded...')
        df= Populating_elev_df()
        print("Do you want plot for specific PRN?")

        choice = input("Enter Y or N: ")

        if choice in {'Y','YES','yes','Yes','y'}:
            specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))
            #grouped = df.groupby('PRN')
            grouped = df.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped = df.groupby('PRN')
            # Plot d/u values against 24-hour time for the specific PRN
            if specific_prn in grouped.groups:
                group = grouped.get_group(specific_prn)
                fig = px.line(group, x='24-hour Time', y='Elevation', title=f'Elevation values for PRN {specific_prn}')
                fig.update_layout(
                    xaxis_title='Time (24-hour format)',
                    yaxis_title='Elevation',
                    xaxis_tickformat='%H:%M:%S'
                )
                fig.show()
                plotly.offline.plot(fig, filename=f'plots/elev_prn={specific_prn}.html')
                menu1()
            else:
                print(f"PRN {specific_prn} not found in the dataset.")
                menu1()

        elif choice in {'N','no','NO','No','n'}:        
            print('Data Loaded Plotting Graph...')
            fig = go.Figure()

            # Add traces for each PRN
            for prn in df['PRN'].unique():
                group = df[df['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['Elevation'], mode='lines', name=f'PRN {prn}'))

            # Update layout
            fig.update_layout(
                title='d/u values for all PRNs',
                xaxis_title='Time (24-hour format)',
                yaxis_title='Elevation',
                xaxis_tickformat='%H:%M:%S'
            )

            # Show the figure
            fig.show()
            plotly.offline.plot(fig, filename='plots/elev_vs_time_total.html')

            menu1()
        else:
                print ("Invalid Input , Please Try Again")
                menu1()

    def cnudu():

        print('Please Wait while ETSA and MPMB Data gets loaded...')
        result=Populating_combinedcnodu_df()

        df1 = (next(result))
        df2= (next(result))
        print("Do you want plot for specific PRN?")

        choice = input("Enter Y or N: ")

        if choice in {'Y','YES','yes','Yes','y'}:
            #grouped = df.groupby('PRN')
            grouped1 = df1.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped2 = df2.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)

            #print (grouped1)
            #print (grouped2)
            # Print unique combinations of 'PRN' and 'Time' in df1 and df2
            print("\nUnique combinations in df1:")
            print(grouped1[['PRN', '24-hour Time']].drop_duplicates())
            print("\nUnique combinations in df2:")
            print(grouped2[['PRN', '24-hour Time']].drop_duplicates())


            try:
                df_merged = grouped2.merge(grouped1[['PRN', 'C/N0', '24-hour Time']], on=['PRN', '24-hour Time'], how='left')
                print("Merging successful.")
            except KeyError as e:
                print(f"KeyError: {e}")
                #df_merged.to_csv("testingforcno.csv", sep=',', index=False, encoding='utf-8')
            #grouped = df.groupby('PRN')
            grouped = df_merged.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped = df_merged.groupby('PRN')

            # Print the head and tail of each group
            '''
            for prn, group in grouped:
                print(f"\nPRN: {prn}")
                print("Head of the group:")
                print(group.head())
                print("\nTail of the group:")
                print(group.tail())
            '''
            for prn in df_merged['PRN'].unique():
                group = df_merged[df_merged['PRN'] == prn]
    


            specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))

            # Plot d/u values against 24-hour time for the specific PRN
            if specific_prn in grouped.groups:
            
                # Assuming you have defined 'group' and 'specific_prn'
                fig = go.Figure()   
                # Add d/u values
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['d/u'], mode='lines', name='d/u'))
                
                # Add C/N0 values
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['C/N0'], mode='lines', name='C/N0', yaxis='y2'))
                
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
                        title='C/N0',
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
                plotly.offline.plot(fig, filename=f'plots/cno_du_vs_time_for_{specific_prn}.html')
                menu1()

            else:
                print(f"PRN {specific_prn} not found in the dataset.")
                menu1()
            #code hereq

        elif choice in {'N','no','NO','No','n'}:
                        #grouped = df.groupby('PRN')
            grouped1 = df1.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped2 = df2.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)

            #print (grouped1)
            #print (grouped2)
            # Print unique combinations of 'PRN' and 'Time' in df1 and df2
            print("\nUnique combinations in df1:")
            print(grouped1[['PRN', '24-hour Time']].drop_duplicates())
            print("\nUnique combinations in df2:")
            print(grouped2[['PRN', '24-hour Time']].drop_duplicates())


            try:
                df_merged = grouped2.merge(grouped1[['PRN', 'C/N0', '24-hour Time']], on=['PRN', '24-hour Time'], how='left')
                print("Merging successful.")
            except KeyError as e:
                print(f"KeyError: {e}")
                #df_merged.to_csv("testingforcno.csv", sep=',', index=False, encoding='utf-8')
            #grouped = df.groupby('PRN')
            grouped = df_merged.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped = df_merged.groupby('PRN')

            # Print the head and tail of each group
            '''
            for prn, group in grouped:
                print(f"\nPRN: {prn}")
                print("Head of the group:")
                print(group.head())
                print("\nTail of the group:")
                print(group.tail())
            '''

            print('Data Loaded Plotting Graph...')
           


           


            pio.renderers.default = "iframe"


            # Plot d/u values against 24-hour time for all PRNs together
            fig = go.Figure()

            # Add traces for each PRN for d/u values
            for prn in df_merged['PRN'].unique():
                group = df_merged[df_merged['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['d/u'], mode='lines', name=f'PRN {prn} - d/u '))

            # Add traces for each PRN for C/N0 values (secondary y-axis)
            for prn in df_merged['PRN'].unique():
                group = df_merged[df_merged['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['C/N0'], mode='lines', name=f'PRN {prn} - C/N0', yaxis='y2'))

            # Update layout with dual y-axes
            fig.update_layout(
                title='d/u values and C/N0 for all PRNs',
                xaxis_title='Time (24-hour format)',
                yaxis_title='d/u (dB)',
                yaxis2=dict(
                    title='C/N0 (dB-Hz)',
                    overlaying='y',
                    side='right'
                ),
                xaxis_tickformat='%H:%M'
            )

            # Show the figure
            fig.show()
            plotly.offline.plot(fig, filename='plots/cno_du_vs_time.html')
            menu1()
        else:
                print ("Invalid Input , Please Try Again")
                menu1()





    def elevdu():
        print('Please Wait while MPMB and ETSA Data gets loaded...')
        result = Populating_combinedelevdu_df()
        df1 = (next(result))
        df2 = (next(result))
        print("Do you want plot for specific PRN?")

        choice = input("Enter Y or N: ")

        if choice in {'Y','YES','yes','Yes','y'}:
            #grouped = df.groupby('PRN')
            grouped1 = df1.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
            grouped2 = df2.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
            try:
                df_merged = grouped2.merge(grouped1[['PRN', 'Elevation', 'Time']], on=['PRN', 'Time'], how='left')
                print("Merging successful.")
            except KeyError as e:
                print(f"KeyError: {e}")
            grouped = df_merged.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
            grouped = df_merged.groupby('PRN')
    
            # Print the head and tail of each group
            
            #for prn, group in grouped:
               # print(f"\nPRN: {prn}")
                #print("Head of the group:")
                #print(group.head())
                #print("\nTail of the group:")
                #print(group.tail())
            
            for prn in df_merged['PRN'].unique():
                group = df_merged[df_merged['PRN'] == prn]


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
                plotly.offline.plot(fig, filename=f'plots/elev_du_vs_time_for_{specific_prn}.html')
                menu1()

            else:
                print(f"PRN {specific_prn} not found in the dataset.")


            # In[ ]:



    



        elif choice in {'N','no','NO','No','n'}:
            print('Data Loaded Plotting Graph...')

            #grouped = df.groupby('PRN')
            grouped1 = df1.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
            grouped2 = df2.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
            try:
                df_merged = grouped2.merge(grouped1[['PRN', 'Elevation', 'Time']], on=['PRN', 'Time'], how='left')
                print("Merging successful.")
            except KeyError as e:
                print(f"KeyError: {e}")
            grouped= df_merged.sort_values(by=['PRN', 'Time']).reset_index(drop=True)
            grouped= df_merged.groupby('PRN')


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



            # In[15]:


            pio.renderers.default = "iframe"


            # Plot d/u values against 24-hour time for all PRNs together
            fig = go.Figure()

            # Add traces for each PRN for d/u values
            for prn in df_merged['PRN'].unique():
                group = df_merged[df_merged['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['Time'], y=group['d/u'], mode='lines', name=f'PRN {prn} - d/u '))

            # Add traces for each PRN for C/N0 values (secondary y-axis)
            for prn in df_merged['PRN'].unique():
                group = df_merged[df_merged['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['Time'], y=group['Elevation'], mode='lines', name=f'PRN {prn} - elev', yaxis='y2'))

            # Update layout with dual y-axes
            fig.update_layout(
                title='d/u values and Elevation for all PRNs',
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
            plotly.offline.plot(fig, filename='plots/ele_du_vs_time.html')
            menu1()

        else:
                print ("Invalid Input , Please Try Again")
                menu1()







    def residual():
        print('Please Wait while SATA Data gets loaded...')
        df= Populating_residual_df()
        print("Do you want plot for specific PRN?")

        choice = input("Enter Y or N: ")

        if choice in {'Y','YES','yes','Yes','y'}:
            specific_prn = int(input("Enter a PRN to plot (e.g., 32): "))
            #grouped = df.groupby('PRN')
            grouped = df.sort_values(by=['PRN', '24-hour Time']).reset_index(drop=True)
            grouped = df.groupby('PRN')
            # Plot d/u values against 24-hour time for the specific PRN
            if specific_prn in grouped.groups:
                group = grouped.get_group(specific_prn)
                fig = px.line(group, x='24-hour Time', y='Residual', title=f'd/u values for PRN {specific_prn}')
                fig.update_layout(
                    xaxis_title='Time (24-hour format)',
                    yaxis_title='d/u (dB)',
                    xaxis_tickformat='%H:%M:%S'
                )
                fig.show()
                plotly.offline.plot(fig, filename=f'plots/residual_prn={specific_prn}.html')
                menu1()
            else:
                print(f"PRN {specific_prn} not found in the dataset.")
                menu1()

        elif choice in {'N','no','NO','No','n'}:
            print('Data Loaded Plotting Graph...')
            fig = go.Figure()

            # Add traces for each PRN
            for prn in df['PRN'].unique():
                group = df[df['PRN'] == prn]
                fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['Residual'], mode='lines', name=f'PRN {prn}'))

            # Update layout
            fig.update_layout(
                title='d/u values for all PRNs',
                xaxis_title='Time (24-hour format)',
                yaxis_title='Residual',
                xaxis_tickformat='%H:%M:%S'
            )

            # Show the figure
            fig.show()
            plotly.offline.plot(fig, filename='plots/residual_vs_time_total.html')
            menu1()
        else:
            print ("Invalid Input , Please Try Again")
            menu1()

            

    def default_option():
        return "Invalid option. Please select a valid option."
        menu1()

    options = {
        1: duvt,
        2: cnot,
        3: elev,
        4: cnudu,
        5: elevdu,
        6: residual

    }
    

    def menu1():
        print("Menu:")
        print("1. D/U vs Time")
        print("2. C/No vs Time")
        print("3. Elev vs Time")
        print("4. C/NO & D/U vs Time")
        print("5. Elevation & D/U vs Time")
        print("6. Residual & D/U vs Time")

        print("Enter your choice:")
        try:
            choice = int(input())
            # Get the function from the dictionary and call it, or call the default function if choice is invalid
            result = options.get(choice, default_option)()
            print(result)
            menu1 ()
        except ValueError:
            print("Invalid input. Please enter a number.")
            menu1()
        
    menu1()
    
        


# Ask user to input a specific PRN
'''
def spec_prn ():
   # Populating_mpmb_df()
    df= Populating_mpmb_df()
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
        plotly.offline.plot(fig, filename='plots/specific_prn.html')

    else:
        print(f"PRN {specific_prn} not found in the dataset.")
'''

def calc_table():
    #Populating_mpmb_df()
    df= Populating_mpmb_df()

    # Count the number of values below 16
    count_below_16 = df["d/u"][df["d/u"] < 16].count()

    # Calculate the total number of values in the column
    total_values = df["d/u"].count()

    # Calculate the percentage of values below 16
    percentage_below_16 = (count_below_16 / total_values) * 100


    # Count the number of values below 20
    count_below_20= df["d/u"][df["d/u"] < 20].count()

    # Calculate the total number of values in the column
    total_values = df["d/u"].count()

    # Calculate the percentage of values below 16
    percentage_below_20 = (count_below_20 / total_values) * 100


    # Count the number of values >= 20
    count_eqgt_20= df["d/u"][df["d/u"] >= 20].count()

    # Calculate the total number of values in the column
    total_values = df["d/u"].count()

    # Calculate the percentage of values below 16
    percentage_eqgt_20 = (count_eqgt_20 / total_values) * 100
    # Print values in a table format
    table = f"""
    +-----------------------------+--------------------+
    |       Description           |      Percentage    |
    +-----------------------------+--------------------+
    | Percentage of d/u values < 16|    {percentage_below_16:.2f}%    |
    | Percentage of d/u values < 20|    {percentage_below_20:.2f}%    |
    | Percentage of d/u values >= 20|   {percentage_eqgt_20:.2f}%    |
    +-----------------------------+--------------------+
    """

    print(table)
    
def test_calc_table():
    #Populating_mpmb_df()
    df= Populating_residual_df()

    # Count the number of values below 16
    count_below_16 = df["Residual"][df["Residual"] == 0].count()

    # Calculate the total number of values in the column
    total_values = df["Residual"].count()

    # Calculate the percentage of values below 16
    percentage_below_16 = (count_below_16 / total_values) * 100


    # Count the number of values below 20
    count_below_20= df["Residual"][df["Residual"] < 20].count()

    # Calculate the total number of values in the column
    total_values = df["Residual"].count()

    # Calculate the percentage of values below 16
    percentage_below_20 = (count_below_20 / total_values) * 100


   
    table = f"""
    +-----------------------------+--------------------+
    |       Description           |      Percentage    |
    +-----------------------------+--------------------+
    | Percentage of d/u values < 0|    {percentage_below_16:.2f}%    |
    | Percentage of d/u values < 20|    {percentage_below_20:.2f}%    |
    | Percentage of d/u values >= 20|      |
    +-----------------------------+--------------------+
    """

    print(table)

    
def bin_to_csv ():
    print("Input Binary File Path")
    binary_file_path = input()  # Path to the binary GPS file

    csv_file_path1 = 'mpmbfinal.csv'     
    csv_file_path2= 'sata.csv'
    csv_file_path3= 'etsa.csv'
    # Path to the output CSV file
    print("Please wait while the bin file converts to CSVs")

    records1= parse_gps_binary(binary_file_path)
    write_to_csv1(records1, csv_file_path1)
    print(f"MPMB Data successfully converted from {binary_file_path} to {csv_file_path1}")

    records2 = test_sata(binary_file_path,csv_file_path2)
    #write_to_csv2(records2, csv_file_path2)


    print(f"SATA data successfully converted from {binary_file_path} to {csv_file_path2}")
    
    records3 = parse_eats_binary(binary_file_path)
    write_to_csv3(records3, csv_file_path3)

    print(f"EATSA Data successfully converted from {binary_file_path} to {csv_file_path3}")


def main():
    isExist =os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    def default_option():
     return "Invalid option. Please select a valid option."
    

    menu_options = {
    1: bin_to_csv,
    2: plotingfinals,
    3: calc_table
}
    

    def menu():
        print("Menu:")
        print("1. Process BIN File")
        print("2. Plot Graphs")
        print("3. Calculate d/u Table")
        print("Enter your choice:")

        try:
            choice = int(input())
            # Get the function from the dictionary and call it, or call the default function if choice is invalid
            result = menu_options.get(choice, default_option)()
            print(result)
            menu()

           
        except ValueError:
            clear_screen()
            print("Invalid input. Please enter a number.")
            menu()

    print("Do you want to use last used bin file")
    user_input = input("Enter Y or N: ")

    if user_input in {'Y','YES','yes','Yes','y'}:

    #if user_input == 'Y' or user_input == 'N' or user_input == 'YES' or user_input =='NO' or user_input == 'yes' or user_input =='no' or user_input == 'Yes' or user_input =='No':
        menu()
    elif user_input in {'N','no','NO','No','n'}:
        bin_to_csv()
        #test_calc_table()
        menu()
    else:
        clear_screen()
        print("Invalid Input, Please Try Again.")
        main()
            
if __name__ == '__main__':
     main()


