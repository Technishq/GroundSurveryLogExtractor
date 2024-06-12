import struct
import csv

def parse_posb_binary(file_path):
    records = []

    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break  # End of file reached
            
            message_id, = struct.unpack('I', sync_header)
            if message_id != 1:
                continue  # Not a POSB message, skip
            
            # Read the rest of the POSB message
            message_byte_count, = struct.unpack('I', bin_file.read(4))
            
            # Read the data fields
            weeks, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            latitude, = struct.unpack('d', bin_file.read(8))
            longitude, = struct.unpack('d', bin_file.read(8))
            height, = struct.unpack('d', bin_file.read(8))
            datum_id, = struct.unpack('I', bin_file.read(4))
            std_dev_latitude, = struct.unpack('d', bin_file.read(8))
            std_dev_longitude, = struct.unpack('d', bin_file.read(8))
            week_number, = struct.unpack('I', bin_file.read(4))
            undulation, = struct.unpack('d', bin_file.read(8))
            std_dev_height, = struct.unpack('d', bin_file.read(8))
            solution_status, = struct.unpack('I', bin_file.read(4))

            records.append([
                weeks, seconds_of_week, latitude, longitude, height,
                datum_id, std_dev_latitude, std_dev_longitude,
                week_number, undulation, std_dev_height, solution_status
            ])

    return records

def write_to_csv(records, csv_path):
    headers = [
        'Weeks', 'Seconds of Week', 'Latitude', 'Longitude', 'Height',
        'Datum ID', 'StdDev of Latitude', 'StdDev of Longitude',
        'Week Number', 'Undulation', 'StdDev of Height', 'Solution Status'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    binary_file_path = 'bin.gps'  # Path to the binary POSB file
    csv_file_path = 'posb.csv'      # Path to the output CSV file

    records = parse_posb_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
