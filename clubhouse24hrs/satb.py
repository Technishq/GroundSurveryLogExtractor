import struct
import csv

def read_gps_file(input_file, output_file):
    # Define the format for the header
    header_format = '3s B I I I d I I'
    header_size = struct.calcsize(header_format)

    # Define the format for the observations with little-endian byte order
    observation_format = '<I d d d I'
    observation_size = struct.calcsize(observation_format)

    # Open the binary file for reading and CSV file for writing
    with open(input_file, 'rb') as bin_file, open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write CSV header
        csv_writer.writerow(['Week Number', 'Seconds of Week', 'Solution Status', 'Number of Observations', 
                             'PRN', 'Azimuth', 'Elevation', 'Residual', 'Reject Code'])

        while True:
            # Read the header
            header_data = bin_file.read(header_size)
            if len(header_data) < header_size:
                break  # End of file or incomplete header

            try:
                # Unpack the header
                sync, checksum, message_id, byte_count, week_number, seconds_of_week, \
                solution_status, num_observations = struct.unpack(header_format, header_data)

                # Debug print for the header
                #print(f"Header - Sync: {sync}, Checksum: {checksum}, Message ID: {message_id}, Byte Count: {byte_count}, Week Number: {week_number}, Seconds of Week: {seconds_of_week}, Solution Status: {solution_status}, Number of Observations: {num_observations}")

                # Validate the data
                if message_id != 12:
                    #print(f"Unexpected message ID: {message_id}")
                    # Skip to the next header based on byte_count
                    bin_file.seek(byte_count - header_size, 1)
                    continue

                for _ in range(num_observations):
                    observation_data = bin_file.read(observation_size)
                    if len(observation_data) < observation_size:
                        #print("Incomplete observation data")
                        break  # End of observations or incomplete observation

                    try:
                        # Unpack the observation
                        prn, azimuth, elevation, residual, reject_code = struct.unpack(observation_format, observation_data)

                        # Debug print for the observation
                        #print(f"Observation - PRN: {prn}, Azimuth: {azimuth}, Elevation: {elevation}, Residual: {residual}, Reject Code: {reject_code}")

                        # Write the data to the CSV file
                        csv_writer.writerow([week_number, seconds_of_week, solution_status, num_observations, 
                                             prn, azimuth, elevation, residual, reject_code])
                    except struct.error as e:
                        #print(f"Error unpacking observation: {e}")
                        continue  # Skip to the next observation
            except struct.error as e:
                #print(f"Error unpacking header: {e}")
                continue  # Skip to the next header

if __name__ == "__main__":
    input_file = 'rawdata/NDB24hrs.gps'  # Update the path to your input file
    output_file = 'testsatb.csv'  # Update the path to your output file
    read_gps_file(input_file, output_file)
