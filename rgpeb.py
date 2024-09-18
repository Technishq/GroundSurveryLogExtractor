import struct
import csv

def read_binary_gps_file(file_path):
    with open(file_path, 'rb') as bin_file:
        data = bin_file.read()
    return data

def parse_rgeb_field(binary_data):
    # Define the format of the header and the individual satellite data for $RGEB
    header_format = '3s1s4i2d2i'
    satellite_format = 'i d f d f f f f i'
    
    header_size = struct.calcsize(header_format)
    satellite_size = struct.calcsize(satellite_format)
    
    offset = 0
    rgeb_data = []

    # Iterate through the binary data to find and parse $RGEB fields
    while offset < len(binary_data):
        if binary_data[offset:offset+3] == b'RGB':
            # Unpack the header
            sync, checksum, msg_id, msg_byte_count, week, seconds, num_obs, receiver_status = struct.unpack_from(header_format, binary_data, offset)
            offset += header_size

            # Extract each observation
            for _ in range(num_obs):
                prn, pseudorange, stddev_pseudorange, carrier_phase, stddev_carrier_phase, doppler_freq, cn0, locktime, channel_status = struct.unpack_from(satellite_format, binary_data, offset)
                rgeb_data.append([week, seconds, receiver_status, prn, pseudorange, stddev_pseudorange, carrier_phase, stddev_carrier_phase, doppler_freq, cn0, locktime, channel_status])
                offset += satellite_size
        else:
            offset += 1

    return rgeb_data

def write_to_csv(data, output_file):
    header = ['week', 'seconds', 'receiver_status', 'prn', 'pseudorange', 'stddev_pseudorange', 'carrier_phase', 'stddev_carrier_phase', 'doppler_freq', 'cn0', 'locktime', 'channel_status']
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

def convert_bin_to_csv(input_file, output_file):
    binary_data = read_binary_gps_file(input_file)
    rgeb_data = parse_rgeb_field(binary_data)
    write_to_csv(rgeb_data, output_file)

# Example usage
input_file = 'bin.gps'
output_file = 'gps_data.csv'
convert_bin_to_csv(input_file, output_file)
