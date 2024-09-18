
import struct
import csv
from tqdm import tqdm
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import plotly.io as pio

def parse_gps_binary(file_path1):
    records = []
    with open(file_path1, 'rb') as bin_file:
        while True:
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break
            message_id, = struct.unpack('I', sync_header)
            if message_id != 95:
                continue
            message_byte_count, = struct.unpack('I', bin_file.read(4))
            week_number, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            prn, = struct.unpack('I', bin_file.read(4))
            channel_status, = struct.unpack('I', bin_file.read(4))
            medll_status, = struct.unpack('I', bin_file.read(4))
            delay, = struct.unpack('f', bin_file.read(4))
            amplitude, = struct.unpack('f', bin_file.read(4))
            phase, = struct.unpack('f', bin_file.read(4))
            in_phase_residuals = [struct.unpack('f', bin_file.read(4))[0] for _ in range(12)]
            out_of_phase_residuals = [struct.unpack('f', bin_file.read(4))[0] for _ in range(12)]
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

    with open(csv_path1, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def parse_sata_binary(file_path2):
    records = []
    with open(file_path2, 'rb') as bin_file:
        while True:
            sync_header = bin_file.read(3)
            if len(sync_header) < 3:
                break
            checksum = bin_file.read(1)
            if len(checksum) < 1:
                break
            message_id_data = bin_file.read(4)
            if len(message_id_data) < 4:
                break
            message_id, = struct.unpack('I', message_id_data)
            if message_id != 12:
                continue
            message_byte_count_data = bin_file.read(4)
            if len(message_byte_count_data) < 4:
                break
            message_byte_count, = struct.unpack('I', message_byte_count_data)
            week_number_data = bin_file.read(4)
            if len(week_number_data) < 4:
                break
            week_number, = struct.unpack('I', week_number_data)
            seconds_of_week_data = bin_file.read(8)
            if len(seconds_of_week_data) < 8:
                break
            seconds_of_week, = struct.unpack('d', seconds_of_week_data)
            solution_status_data = bin_file.read(4)
            if len(solution_status_data) < 4:
                break
            solution_status, = struct.unpack('I', solution_status_data)
            num_observations_data = bin_file.read(4)
            if len(num_observations_data) < 4:
                break
            num_observations, = struct.unpack('I', num_observations_data)
            observations = []
            for _ in range(num_observations):
                prn_data = bin_file.read(4)
                if len(prn_data) < 4:
                    break
                prn, = struct.unpack('I', prn_data)
                azimuth_data = bin_file.read(8)
                if len(azimuth_data) < 8:
                    break
                azimuth, = struct.unpack('d', azimuth_data)
                elevation_data = bin_file.read(8)
                if len(elevation_data) < 8:
                    break
                elevation, = struct.unpack('d', elevation_data)
                residual_data = bin_file.read(8)
                if len(residual_data) < 8:
                    break
                residual, = struct.unpack('d', residual_data)
                reject_code_data = bin_file.read(4)
                if len(reject_code_data) < 4:
                    break
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

def parse_eats_binary(file_path3):
    records = []
    with open(file_path3, 'rb') as bin_file:
        while True:
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break
            message_id, = struct.unpack('I', sync_header)
            if message_id != 48:
                continue
            message_byte_count, = struct.unpack('I', bin_file.read(4))
            week_number, = struct.unpack('I', bin_file.read(4))
            time_of_week, = struct.unpack('d', bin_file.read(8))
            solution_status, = struct.unpack('I', bin_file.read(4))
            num_channels, = struct.unpack('I', bin_file.read(4))
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

def plotingfinals():
    csv_file = 'mpmbfinal.csv'
    df = pd.read_csv(csv_file)
    columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'Amplitude']
    df = df[columns_to_keep]
    GPS_EPOCH = datetime(1980, 1, 6)

    def gps_to_utc(week, seconds):
        gps_time = GPS_EPOCH + timedelta(weeks=week, seconds=seconds)
        return gps_time



    df['UTC Time'] = df.apply(lambda row: gps_to_utc(row['Week Number'], row['Seconds of Week']), axis=1)
    df = df.sort_values(by='Seconds of Week')

    fig = px.line(df, x='UTC Time', y='Amplitude', color='PRN')
    fig.update_layout(
        title='Amplitude vs. UTC Time',
        xaxis_title='UTC Time',
        yaxis_title='Amplitude',
        legend_title='PRN'
    )

    pio.write_html(fig, file='output.html', auto_open=True)

# Paths to the binary files
file_path1 = 'bin.gps'
file_path2 = 'bin.gps'
file_path3 = 'bin.gps'

# Paths to the output CSV files
csv_path1 = 'output_file1.csv'
csv_path2 = 'output_file2.csv'
csv_path3 = 'output_file3.csv'

# Read and parse the binary files
print("Parsing GPS binary file...")
gps_records = parse_gps_binary(file_path1)
write_to_csv1(gps_records, csv_path1)
print(f"Finished writing to {csv_path1}")

print("Parsing SATA binary file...")
sata_records = parse_sata_binary(file_path2)
write_to_csv2(sata_records, csv_path2)
print(f"Finished writing to {csv_path2}")

print("Parsing EATS binary file...")
eats_records = parse_eats_binary(file_path3)
write_to_csv3(eats_records, csv_path3)
print(f"Finished writing to {csv_path3}")

# Plotting the results
print("Generating plot...")
plotingfinals()
print("Plot saved as output.html")

# Process records and save to CSV with progress bar
print("Parsing GPS binary file with progress bar...")
gps_records = []
with open(file_path1, 'rb') as bin_file, tqdm(total=10**6) as pbar:
    while True:
        sync_header = bin_file.read(4)
        if len(sync_header) < 4:
            break
        message_id, = struct.unpack('I', sync_header)
        if message_id != 95:
            continue
        message_byte_count, = struct.unpack('I', bin_file.read(4))
        week_number, = struct.unpack('I', bin_file.read(4))
        seconds_of_week, = struct.unpack('d', bin_file.read(8))
        prn, = struct.unpack('I', bin_file.read(4))
        channel_status, = struct.unpack('I', bin_file.read(4))
        medll_status, = struct.unpack('I', bin_file.read(4))
        delay, = struct.unpack('f', bin_file.read(4))
        amplitude, = struct.unpack('f', bin_file.read(4))
        phase, = struct.unpack('f', bin_file.read(4))
        in_phase_residuals = [struct.unpack('f', bin_file.read(4))[0] for _ in range(12)]
        out_of_phase_residuals = [struct.unpack('f', bin_file.read(4))[0] for _ in range(12)]
        gps_records.append([
            week_number, seconds_of_week, prn, channel_status, medll_status,
            delay, amplitude, phase,
            *in_phase_residuals, *out_of_phase_residuals
        ])
        pbar.update(len(sync_header) + 4 + len(message_byte_count) + 4 + len(week_number) + 4 + len(seconds_of_week) + 8 + len(prn) + 4 + len(channel_status) + 4 + len(medll_status) + 4 + len(delay) + 4 + len(amplitude) + 4 + len(phase) + 4*12 + 4*12)
write_to_csv1(gps_records, csv_path1)
print(f"Finished writing to {csv_path1}")

print("Parsing SATA binary file with progress bar...")
sata_records = []
with open(file_path2, 'rb') as bin_file, tqdm(total=10**6) as pbar:
    while True:
        sync_header = bin_file.read(3)
        if len(sync_header) < 3:
            break
        checksum = bin_file.read(1)
        if len(checksum) < 1:
            break
        message_id_data = bin_file.read(4)
        if len(message_id_data) < 4:
            break
        message_id, = struct.unpack('I', message_id_data)
        if message_id != 12:
            continue
        message_byte_count_data = bin_file.read(4)
        if len(message_byte_count_data) < 4:
            break
        message_byte_count, = struct.unpack('I', message_byte_count_data)
        week_number_data = bin_file.read(4)
        if len(week_number_data) < 4:
            break
        week_number, = struct.unpack('I', week_number_data)
        seconds_of_week_data = bin_file.read(8)
        if len(seconds_of_week_data) < 8:
            break
        seconds_of_week, = struct.unpack('d', seconds_of_week_data)
        solution_status_data = bin_file.read(4)
        if len(solution_status_data) < 4:
            break
        solution_status, = struct.unpack('I', solution_status_data)
        num_observations_data = bin_file.read(4)
        if len(num_observations_data) < 4:
            break
        num_observations, = struct.unpack('I', num_observations_data)
        observations = []
        for _ in range(num_observations):
            prn_data = bin_file.read(4)
            if len(prn_data) < 4:
                break
            prn, = struct.unpack('I', prn_data)
            azimuth_data = bin_file.read(8)
            if len(azimuth_data) < 8:
                break
            azimuth, = struct.unpack('d', azimuth_data)
            elevation_data = bin_file.read(8)
            if len(elevation_data) < 8:
                break
            elevation, = struct.unpack('d', elevation_data)
            residual_data = bin_file.read(8)
            if len(residual_data) < 8:
                break
            residual, = struct.unpack('d', residual_data)
            reject_code_data = bin_file.read(4)
            if len(reject_code_data) < 4:
                break
            reject_code, = struct.unpack('I', reject_code_data)
            observations.append([
                prn, azimuth, elevation, residual, reject_code
            ])
        sata_records.append([
            week_number, seconds_of_week, solution_status, num_observations,
            observations
        ])
        pbar.update(len(sync_header) + len(checksum) + 4 + len(message_byte_count_data) + 4 + len(week_number_data) + 4 + len(seconds_of_week_data) + 8 + len(solution_status_data) + 4 + len(num_observations_data) + 4*len(observations) + 8*len(observations) + 8*len(observations) + 8*len(observations) + 4*len(observations))
write_to_csv2(sata_records, csv_path2)
print(f"Finished writing to {csv_path2}")

print("Parsing EATS binary file with progress bar...")
eats_records = []
with open(file_path3, 'rb') as bin_file, tqdm(total=10**6) as pbar:
    while True:
        sync_header = bin_file.read(4)
        if len(sync_header) < 4:
            break
        message_id, = struct.unpack('I', sync_header)
        if message_id != 48:
            continue
        message_byte_count, = struct.unpack('I', bin_file.read(4))
        week_number, = struct.unpack('I', bin_file.read(4))
        time_of_week, = struct.unpack('d', bin_file.read(8))
        solution_status, = struct.unpack('I', bin_file.read(4))
        num_channels, = struct.unpack('I', bin_file.read(4))
        for _ in range(num_channels):
            prn_number, = struct.unpack('I', bin_file.read(4))
            channel_tracking_status, = struct.unpack('I', bin_file.read(4))
            doppler, = struct.unpack('d', bin_file.read(8))
            cn0, = struct.unpack('d', bin_file.read(8))
            residual, = struct.unpack('d', bin_file.read(8))
            locktime, = struct.unpack('d', bin_file.read(8))
            pseudorange, = struct.unpack('d', bin_file.read(8))
            rejection_code, = struct.unpack('I', bin_file.read(4))
            eats_records.append([
                week_number, time_of_week, solution_status, num_channels,
                prn_number, channel_tracking_status, doppler, cn0,
                residual, locktime, pseudorange, rejection_code
            ])
            pbar.update(len(sync_header) + 4 + len(message_byte_count) + 4 + len(week_number) + 4 + len(time_of_week) + 8 + len(solution_status) + 4 + len(num_channels) + 4*len(num_channels) + 4*len(num_channels) + 8*len(num_channels) + 8*len(num_channels) + 8*len(num_channels) + 8*len(num_channels) + 8*len(num_channels) + 4*len(num_channels))
write_to_csv3(eats_records, csv_path3)
print(f"Finished writing to {csv_path3}")

#Plotting the results
print("Generating plot...")
plotingfinals()
print("Plot saved as output.html")
