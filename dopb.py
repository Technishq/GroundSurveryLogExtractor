import struct
import csv

def parse_dopb_binary(file_path):
    records = []

    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break  # End of file reached
            
            message_id, = struct.unpack('I', sync_header)
            if message_id != 7:
                continue  # Not a DOPB message, skip
            
            # Read the rest of the DOPB message
            message_byte_count, = struct.unpack('I', bin_file.read(4))
            
            # Read the data fields
            week_number, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            gdop, = struct.unpack('d', bin_file.read(8))
            pdop, = struct.unpack('d', bin_file.read(8))
            htdop, = struct.unpack('d', bin_file.read(8))
            hdop, = struct.unpack('d', bin_file.read(8))
            tdop, = struct.unpack('d', bin_file.read(8))
            num_sats, = struct.unpack('I', bin_file.read(4))
            
            prn_list = []
            for _ in range(num_sats):
                prn, = struct.unpack('I', bin_file.read(4))
                prn_list.append(prn)

            records.append([
                week_number, seconds_of_week, gdop, pdop, htdop,
                hdop, tdop, num_sats, *prn_list
            ])

    return records

def write_to_csv(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'GDOP', 'PDOP', 'HTDOP',
        'HDOP', 'TDOP', 'Number of Satellites Used'
    ]
    max_sats = max(len(record) - 8 for record in records)
    headers.extend([f'PRN {i}' for i in range(1, max_sats + 1)])

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    binary_file_path = 'bin.gps'  # Path to the binary DOPB file
    csv_file_path = 'dopb.csv'      # Path to the output CSV file

    records = parse_dopb_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
