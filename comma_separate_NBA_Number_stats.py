import pandas as pd

def separate_player_number(line):
    """
    Manually separate player name and number from a string.
    """
    # Removing any leading/trailing whitespace
    line = line.strip()

    # Find the index where the last digit sequence starts
    idx = len(line)
    while idx > 0 and line[idx-1].isdigit():
        idx -= 1

    # Split the line into name and number
    name = line[:idx].strip()
    number = line[idx:].strip()

    return name, number

def process_csv(input_file, output_file):
    """
    Process the CSV file to separate player names and numbers.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            # Skip header
            next(infile)

            # Write new header
            outfile.write('Player,Number\n')

            # Process each line
            for line in infile:
                name, number = separate_player_number(line)
                outfile.write(f'{name},{number}\n')

        print(f"Processed CSV has been saved as '{output_file}'")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv = 'NBAstats_concat.csv'  # Replace with your input file path
    output_csv = 'NBAstats.csv' # Replace with your desired output file path
    process_csv(input_csv, output_csv)
