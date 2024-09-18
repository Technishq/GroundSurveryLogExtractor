from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import struct
import csv
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PLOT_FOLDER'] = 'plotlyplots'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PLOT_FOLDER'], exist_ok=True)

# Your binary parsing functions
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
            in_phase_residuals = []
            out_of_phase_residuals = []
            for _ in range(12):
                in_phase_residuals.append(struct.unpack('f', bin_file.read(4))[0])
            for _ in range(12):
                out_of_phase_residuals.append(struct.unpack('f', bin_file.read(4))[0])
            records.append([
                week_number, seconds_of_week, prn, channel_status, medll_status,
                delay, amplitude, phase, *in_phase_residuals, *out_of_phase_residuals
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

# Add similar functions for parse_sata_binary and parse_eats_binary and their respective write_to_csv

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        process_file(file_path)
        return redirect(url_for('plot'))

def process_file(file_path):
    records1 = parse_gps_binary(file_path)
    csv_file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'mpmbfinal.csv')
    write_to_csv1(records1, csv_file_path1)
    # Call the plotting function and save the plot
    plotingfinals(csv_file_path1)

def plotingfinals(csv_file):
    df = pd.read_csv(csv_file)
    columns_to_keep = ['Week Number', 'Seconds of Week', 'PRN', 'Amplitude']
    df = df[columns_to_keep]
    GPS_EPOCH = datetime(1980, 1, 6)
    def gps_to_utc(week, seconds):
        gps_time = GPS_EPOCH + timedelta(weeks=week, seconds=seconds)
        return gps_time
    df['UTC Time'] = df.apply(lambda row: gps_to_utc(row['Week Number'], row['Seconds of Week']), axis=1)
    df['24-hour Time'] = df['UTC Time'].dt.strftime('%H:%M')
    df['Amplitude'] = df['Amplitude'].replace(0, np.nan)
    df['Amplitude'] = df['Amplitude'].fillna(df['Amplitude'].min() / 2)
    df['d/u'] = -1*20 * np.log10(df['Amplitude'])
    fig = go.Figure()
    for prn in df['PRN'].unique():
        group = df[df['PRN'] == prn]
        fig.add_trace(go.Scatter(x=group['24-hour Time'], y=group['d/u'], mode='lines', name=f'PRN {prn}'))
    fig.update_layout(
        title='d/u values for all PRNs',
        xaxis_title='Time (24-hour format)',
        yaxis_title='d/u (dB)',
        xaxis_tickformat='%H:%M:'
    )
    plot_path = os.path.join(app.config['PLOT_FOLDER'], 'default.html')
    plotly.offline.plot(fig, filename=plot_path)

@app.route('/plot')
def plot():
    return send_from_directory(app.config['PLOT_FOLDER'], 'default.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

