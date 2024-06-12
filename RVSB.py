import struct
import csv

def parse_rvsb_binary(file_path):
    records = []

    # Open the binary file in read mode
    with open(file_path, 'rb') as bin_file:
        while True:
            # Read the sync header
            sync_header = bin_file.read(4)
            if len(sync_header) < 4:
                break  # End of file reached

            message_id, = struct.unpack('I', sync_header)
            if message_id != 56:
                continue  # Not an RVSB message, skip

            # Read the message byte count
            message_byte_count, = struct.unpack('I', bin_file.read(4))

            # Read the fixed part of the message
            week_number, = struct.unpack('I', bin_file.read(4))
            seconds_of_week, = struct.unpack('d', bin_file.read(8))
            num_satellite_channels, = struct.unpack('B', bin_file.read(1))
            num_signal_channels, = struct.unpack('B', bin_file.read(1))
            num_cards, = struct.unpack('B', bin_file.read(1))
            reserved, = struct.unpack('B', bin_file.read(1))
            cpu_idle_time, = struct.unpack('f', bin_file.read(4))
            self_test_status, = struct.unpack('I', bin_file.read(4))

            # There should be additional card-specific data here based on num_cards,
            # but it's not specified in the format, so we just process the fixed data.
            records.append([
                week_number, seconds_of_week, num_satellite_channels, num_signal_channels,
                num_cards, reserved, cpu_idle_time, self_test_status
            ])

    return records

def write_to_csv(records, csv_path):
    headers = [
        'Week Number', 'Seconds of Week', 'Number of Satellite Channels', 'Number of Signal Channels',
        'Number of Cards', 'Reserved', 'CPU Idle Time', 'Self-Test Status'
    ]

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    binary_file_path = 'bin.gps'  # Path to the binary RVSB file
    csv_file_path = 'rvsb.csv'     # Path to the output CSV file

    records = parse_rvsb_binary(binary_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {binary_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
