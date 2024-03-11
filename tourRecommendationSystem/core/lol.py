import csv

def get_unique_cities_from_csv(file_path):
    unique_cities = set()  # Initialize an empty set to store unique city names
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'city' in row:  # Check if 'city' exists in the row
                unique_cities.add(row['city'])
            else:
                print(f"Row with missing 'city' column: {row}")  # Print problematic rows
    
    return unique_cities

# Example usage:
file_path = 'complete_data.csv'  # Replace 'your_file.csv' with the path to your CSV file
unique_cities = get_unique_cities_from_csv(file_path)
print(unique_cities)
