import struct

def parse_posb_binary(input_file):
    records = []

    print("Opening binary file:", input_file)
    # Open the binary file in read mode
    with open(input_file, 'rb') as bin_file:
        print("Binary file opened successfully")
        while True:
            # Read the sync header
            sync_header = bin_file.read(3)
            if len(sync_header) < 3:
                break  # End of file reached

            # Check if it's a POSB message
            if sync_header == b'$PO':
                print("Found $PO sync header")
                # Read the rest of the POSB message
                message_id, message_byte_count = struct.unpack('BI', bin_file.read(5))
                print(f"Message ID: {message_id}, Message Byte Count: {message_byte_count}")
                
                # Read the data fields
                week_number, seconds_of_week, latitude, longitude, height, datum_id, \
                    lat_std_dev, lon_std_dev, height_std_dev, solution_status = struct.unpack('Id3d4Id3dI', bin_file.read(84))
                print(f"Week Number: {week_number}, Seconds of Week: {seconds_of_week}, Latitude: {latitude}, Longitude: {longitude}, Height: {height}, Datum ID: {datum_id}, Lat Std Dev: {lat_std_dev}, Lon Std Dev: {lon_std_dev}, Height Std Dev: {height_std_dev}, Solution Status: {solution_status}")

                records.append((week_number, seconds_of_week, latitude, longitude, height, datum_id, \
                    lat_std_dev, lon_std_dev, height_std_dev, solution_status))
                print("Record appended")

    return records

def write_to_ascii(records, ascii_file):
    with open(ascii_file, 'w') as ascii_out:
        for record in records:
            week_number, seconds_of_week, latitude, longitude, height, datum_id, \
                lat_std_dev, lon_std_dev, height_std_dev, solution_status = record

            ascii_out.write(f"$POSB,{week_number},{seconds_of_week},{latitude},{longitude},{height},{datum_id},"
                            f"{lat_std_dev},{lon_std_dev},{height_std_dev},{solution_status}\n")

def main():
    input_file = 'bin.gps'  # Path to the input binary file
    ascii_file = 'posb_output_ascii.txt'  # Path to the output ASCII file

    records = parse_posb_binary(input_file)
    write_to_ascii(records, ascii_file)

    print(f"Data successfully converted from {input_file} to ASCII file: {ascii_file}")

if __name__ == '__main__':
    main()
