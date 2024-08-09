import csv
from srp import irvings_algorithm


def read_preferences(input_file):
    preferences = {}
    with open(input_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            student_id = row[0]
            preference_list = row[1].split(', ')
            preferences[student_id] = preference_list
    return preferences


def write_output(output_file, matches):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['student_id', 'assigned_roommate'])
        for student_id, roommate in matches.items():
            writer.writerow([student_id, roommate])


def main():
    # Path to your input CSV file
    input_file = '/Users/dee/Desktop/5800final_project/input.csv'
    # Path to your output CSV file
    output_file = '/Users/dee/Desktop/5800final_project/output.csv'

    # Read preferences from input file
    preferences = read_preferences(input_file)

    # Perform stable roommate matching
    matches = irvings_algorithm(preferences)

    # Write the results to output file
    write_output(output_file, matches)


if __name__ == '__main__':
    main()
