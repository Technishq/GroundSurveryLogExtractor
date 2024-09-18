import struct
import csv

def parse_eats_binary(file_path):
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

def write_to_csv(records, csv_path):
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

def main():
    binary_file_path = 'bin.gps'  # Path to the binary SATB file
    csv_file_path = 'satb.csv'     # Path to the output CSV file

    records = parse_eats_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
