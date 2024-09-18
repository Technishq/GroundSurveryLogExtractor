import csv

def parse_dopa_line(line):
    # Remove the leading '$DOPA' and the checksum at the end
    line = line.strip()
    if line.startswith('$DOPA'):
        line = line[6:]
    if '*' in line:
        line = line.split('*')[0]
    
    # Split the line by commas
    parts = line.split(',')
    
    # Extract fields
    week = int(parts[0])
    seconds = float(parts[1])
    gdop = float(parts[2])
    pdop = float(parts[3])
    htdop = float(parts[4])
    hdop = float(parts[5])
    tdop = float(parts[6])
    num_sats = int(parts[7])
    prns = list(map(int, parts[8:8+num_sats]))
    
    return [week, seconds, gdop, pdop, htdop, hdop, tdop, num_sats, *prns]

def read_dopa_file(file_path):
    records = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('$DOPA'):
                record = parse_dopa_line(line)
                records.append(record)
    return records

def write_to_csv(records, csv_path):
    headers = [
        'Week', 'Seconds', 'GDOP', 'PDOP', 'HTDOP', 'HDOP', 'TDOP', 'Number of Satellites'
    ]
    max_sats = max(len(record) - len(headers) for record in records)
    for i in range(max_sats):
        headers.append(f'Satellite PRN {i+1}')

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(records)

def main():
    ascii_file_path = 'dopa_data.txt'  # Path to the ASCII DOPA file
    csv_file_path = 'dopa_data.csv'    # Path to the output CSV file

    records = read_dopa_file(ascii_file_path)
    write_to_csv(records, csv_file_path)

    print(f"Data successfully converted from {ascii_file_path} to {csv_file_path}")

if __name__ == '__main__':
    main()
