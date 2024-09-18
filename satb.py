import struct

def read_first_observation(input_file):
    # Define the format for the header
    header_format = '3s B I I I d I I'
    header_size = struct.calcsize(header_format)
    print (header_size)
    # Define the format for the observations with little-endian byte order
    observation_format = '<I d d d I'
    observation_size = struct.calcsize(observation_format)

    # Open the binary file for reading
    with open(input_file, 'rb') as bin_file:
        # Read the header
        header_data = bin_file.read(header_size)
        if len(header_data) < header_size:
            print("Incomplete header")
            return

        try:
            # Unpack the header
            sync, checksum, message_id, byte_count, week_number, seconds_of_week, \
            solution_status, num_observations = struct.unpack(header_format, header_data)

            # Print the header
            print(f"Sync: {sync}")
            print(f"Checksum: {checksum}")
            print(f"Message ID: {message_id}")
            print(f"Message byte count: {byte_count}")
            print(f"Week number: {week_number}")
            print(f"Seconds of week: {seconds_of_week}")
            print(f"Solution status: {solution_status}")
            print(f"Number of observations: {num_observations}")

            # Validate the data
            if message_id != 12:
                print(f"Unexpected message ID: {message_id}")
                return

            # Read the first observation
            observation_data = bin_file.read(observation_size)
            if len(observation_data) < observation_size:
                print("Incomplete observation data")
                return

            try:
                # Unpack the observation
                prn, azimuth, elevation, residual, reject_code = struct.unpack(observation_format, observation_data)

                # Print the first observation
                print(f"PRN: {prn}")
                print(f"Azimuth: {azimuth}")
                print(f"Elevation: {elevation}")
                print(f"Residual: {residual}")
                print(f"Reject code: {reject_code}")
            except struct.error as e:
                print(f"Error unpacking observation: {e}")
        except structx.error as e:
            print(f"Error unpacking header: {e}")

if __name__ == "__main__":
    input_file = 'rawdata/clubhouse24hrs.gps'  # Update the path to your input file
    read_first_observation(input_file)
