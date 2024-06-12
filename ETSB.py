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

def write_to_csv(records, csv_path):
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
    binary_file_path = 'bin.gps'  # Path to the binary EATS file
    csv_file_path = 'etsb.csv'     # Path to the output CSV file

    records = parse_eats_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
