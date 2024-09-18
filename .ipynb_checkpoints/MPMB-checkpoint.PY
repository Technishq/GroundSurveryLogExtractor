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

def write_to_csv(records, csv_path):
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

def main():
    binary_file_path = 'bin.gps'  # Path to the binary GPS file
    csv_file_path = 'mpmb.csv'     # Path to the output CSV file

    records = parse_gps_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
