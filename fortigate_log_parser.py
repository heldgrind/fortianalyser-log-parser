import csv
import pandas as pd
import argparse


FIELDS = ["srcip", "srcport", "dstip", "dstport", "service", "app", "action", "date"]

# Function to read logs from CSV file and sort them
def convert_csv_dict(input_file):
    """
    Convert a CSV file from Fortianalyser to a dictionary containing keys defined in FIELDS
    """
    try:
        # Open the CSV file for reading
        with open(input_file, 'r') as csvfile:

            reader = csv.reader(csvfile)

            # Empty list to store the new record
            data = []
            # Loop throug CSV file
            for row in reader:
                # Create new dict to store result based on the fields defined in FIELDS
                record = {}
                # Loop through every element in every row and parse out data based on the defined fields
                for element in row:
                    if element:
                        values = element.split("=")
                    if values[0] in FIELDS:
                        record[values[0]] = values[1]
                data.append(record)
            
            return data

    except FileNotFoundError:
        print("[!] Input file not found.")
        quit()
    except Exception as e:
        print("[!] An error occurred:", str(e))


def get_unique_hits(parsed_data, sort_key):
    """
    Function to filter the duplicate hits, i.e., same srcip, dstport and dstip
    Sort the final record based on argument sort_key. Only args that matches FIELDS will work.
    """
    record = []
    # Set to check unique entries
    unique_entries = set()
    # Index counter
    i = 0
    # loop through the parsed data and create variables for the fields
    for data in parsed_data:
          
        data["hitcount"] = 0 # Add new key to count times the entry has been hit
        if data.keys in FIELDS:
            date = data["date"]
            app = data.get("app", "N/A")
            dstip = data.get("dstip","N/A")
            dstport = data["dstport"]
            service = data.get("service", "N/A")
            srcip = data.get("srcip","N/A")
            action = data["action"]        

        # the keys to check in unique_entries
        entry_key = (data.get("srcip","N/A"), data.get("service", "N/A"), data.get("dstip","N/A"))
        if entry_key not in unique_entries:
            # First hitcount
            data["hitcount"] += 1
            unique_entries.add(entry_key)
            record.append(data)
            # Increase index counter
            i += 1
        else:
            # If not unique, increase hitcount
            record[i - 1]["hitcount"] += 1
        
    # sort the record based on sort_key argument
    sorted_record = sort_list_of_dicts_by_key(record, sort_key)
    return sorted_record


def sort_list_of_dicts_by_key(entries_list, key_name):
    """
    Sort a list of dictionaries based on a specific key in descending order.

    Args:
        entries_list (list): A list of dictionaries.
        key_name (str): The key in each dictionary to use for sorting.

    Returns:
        list: The sorted list of dictionaries.
    """

    if key_name == 'hitcount':
        new_list = sorted(entries_list, key=lambda x: x[key_name], reverse=True)
    else:
        new_list = sorted(entries_list, key=lambda x: x[key_name]) # Sort the list based on the key_name
    return new_list


def create_output(data, output_excel):
    """
    Create output table with Pandas
    ToDo: add options to output in Excel file
    """

    df = pd.DataFrame(data)
    print('[+] Exporting .csv to .xlsx')
    if output_excel != 'false':
        df.to_excel(output_excel)
        print('[+] Output written to Excel sheet.')
    else:
        print(df.to_string())


def log_to_csv(input_file):
    """
    Convert a .log file downloaded from Fortigate to .csv
    """
    try:
        print('[+] Converting .log to .csv')
        with open(input_file, 'r') as log_file:
            with open(input_file[:-4:] + ".csv", 'w') as csv_file:
                for line in log_file:
                    # Replace spaces with commas and write to the CSV file
                    csv_line = line.replace(' ', ',')
                    csv_file.write(csv_line)

        return str(input_file[:-4:] + ".csv")

    except FileNotFoundError:
        print("[!] Input file not found.")
        quit()
    except Exception as e:
        print("[!] An error occurred:", str(e))
        quit()


if __name__ == "__main__":
    """
    Main logic to get arguments and pass it to the functions
    """

    # Arguments parser
    parser = argparse.ArgumentParser(prog='Fortianalyzer/Fortigate log parser',
                                     description='Script to parse out duplicate entries (i.e., same srcip, dstport and dstip), create a hitcounter and sort the output based on srcip, srcport, dstip, dstport, service, app or hitcount.',)
    parser.add_argument('filename', help='Filename in .CSV format or .log format')
    parser.add_argument('-s', '--sort', default=False, help='Sort by field srcip, srcport, dstip, dstport, service, app or hitcount')
    parser.add_argument('-oe', '--output_excel', default='false', help='Output Excel file name (optional)')

    args = parser.parse_args()
    input_file = args.filename
    sort_key = str(args.sort)
    output_excel = str(args.output_excel)

    # If input file is .log convert it to .csv
    if input_file[-4::] == ".log":
        input_file = log_to_csv(input_file)

    # Convert the CSV file to dict
    parsed_data = convert_csv_dict(input_file)
    # Sort and filter duplicate entries
    data = get_unique_hits(parsed_data, sort_key)
    # Display the output
    create_output(data, output_excel)

