def log_to_csv(input_file, output_file):
    with open(input_file, 'r') as log_file:
        with open(output_file, 'w') as csv_file:
            for line in log_file:
                # Replace spaces with commas and write to the CSV file
                csv_line = line.replace(' ', ',')
                csv_file.write(csv_line)

if __name__ == "__main__":
    input_file = "deze_vlan_a.log"
    output_file = "output.csv"
    log_to_csv(input_file, output_file)