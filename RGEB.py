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
            
            
            message_id=struct.unpack('B',  bin_file.read(1) )

            
            if message_id != 32:
                continue  # Not a RGEB message, skip
            
            # Read the rest of the RGEB message
            week_number, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            num_observations, = struct.unpack('I', bin_file.read(4))
            receiver_self_test_status, = struct.unpack('I', bin_file.read(4))
            prn= struct.unpack('I', bin_file.read(4))
            pseudorange= struct.unpack('d', bin_file.read(8))
            std_dev_pseudorange= struct.unpack('d', bin_file.read(8))
            carrier_phase = struct.unpack('d', bin_file.read(8))
            std_dev_doppler=struct.unpack('f', bin_file.read(4))
            doppler_freq=struct.unpack('f', bin_file.read(4))
            c_n0=struct.unpack('f', bin_file.read(4))
            locktime=struct.unpack('f', bin_file.read(4))
            channel_tracking_status = struct.unpack('I', bin_file.read(4))
                


            records.append([
                    week_number, seconds_of_week, num_observations, receiver_self_test_status,
                    prn, pseudorange, std_dev_pseudorange, carrier_phase, std_dev_doppler, doppler_freq,
                    c_n0, locktime, channel_tracking_status
                ])
            
            #for _ in range(num_observations):
                
                
    
    return records

def write_to_csv(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'Number of Observations', 'Receiver Self-Test Status',
        'PRN', 'Pseudorange', 'StdDev Pseudorange', 'Carrier Phase', 'StdDev Doppler',
        'Doppler Frequency', 'C/N0', 'Locktime', 'Channel Tracking Status'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    binary_file_path = 'bin.gps'  # Path to the binary EATS file
    csv_file_path = 'eats_data.csv'  # Path to the output CSV file

    records = parse_eats_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
