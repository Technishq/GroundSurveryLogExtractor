import struct
import csv

def parse_tm1b_binary(file_path):
    records = []
    
    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(3)
            if len(sync_header) < 3:
                break  # End of file reached
            
            message_id, = struct.unpack('B', bin_file.read(1))
            if message_id != 3:
                continue  # Not a TM1B message, skip
            
            # Read the rest of the TM1B message
            message_byte_count, = struct.unpack('B', bin_file.read(1))
            
            # Read the data fields
            week_number, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            clock_offset, = struct.unpack('d', bin_file.read(8))
            std_dev_clock_offset, = struct.unpack('d', bin_file.read(8))
            utc_offset, = struct.unpack('d', bin_file.read(8))
            clock_model_status, = struct.unpack('i', bin_file.read(4))

            records.append([
                week_number, seconds_of_week, clock_offset, std_dev_clock_offset,
                utc_offset, clock_model_status
            ])
    
    return records

def write_to_csv(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'Clock Offset', 'StdDev Clock Offset',
        'UTC Offset', 'Clock Model Status'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    binary_file_path = 'bin.gps'  # Path to the binary TM1B file
    csv_file_path = 'tm1b.csv'      # Path to the output CSV file

    records = parse_tm1b_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
