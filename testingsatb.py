import struct
import csv

def parse_gps_binary(file_path):
    records = []
    
    observation_format = '<I d d d I'  # Explicitly specify little-endian byte order
    observation_size = struct.calcsize(observation_format)
    
    with open(file_path, 'rb') as bin_file:
        while True:
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break
            
            message_id, = struct.unpack('I', sync_header)
            if message_id != 12:
                continue
            
            message_byte_count, = struct.unpack('I', bin_file.read(4))
        
            week_number, = struct.unpack('<I', bin_file.read(4))  # Specify little-endian byte order
            seconds_of_week, = struct.unpack('<d', bin_file.read(8))  # Specify little-endian byte order
            solution_status, = struct.unpack('<I', bin_file.read(4))  # Specify little-endian byte order
            no_of_obs, = struct.unpack('<I', bin_file.read(4))  # Specify little-endian byte order
            
            observation_data = bin_file.read(observation_size)
            prn, azimuth, elevation, residual, reject_code = struct.unpack(observation_format, observation_data)
        
            records.append([
                week_number, seconds_of_week, solution_status, no_of_obs, prn, azimuth, elevation, residual, reject_code
            ])
    
    return records

def write_to_csv(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'Solution Status', 'Number of Observations', 'PRN', 'Azimuth', 'Elevation', 'Residual', 'Reject Code'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    binary_file_path = 'rawdata/NDB24hrs.gps'  # Path to the binary GPS file
    csv_file_path = 'testingobservations.csv'     # Path to the output CSV file

    records = parse_gps_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
