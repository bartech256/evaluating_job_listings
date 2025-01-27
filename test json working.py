import pandas as pd

import json

# Load the JSON file
file_path = 'C:/Users/bar25/Downloads/8368.json'
import json

# Correctly specify the encoding while opening the file
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Inspect the data
print(data[:5])  # Print the first 5 records to verify loading



# Define the desired structure with default values
# Define the desired structure with default values
template = {
    "title": None,
    "company": None,
    "location": None,
    "applicants": None,
    "time_posted": None,
    "seniority_level": None,
    "employment_type": None,
    "job_function": None,
    "industries": None,
    "description": None
}

# Normalize the data
normalized_data = []
for record in data:
    # Ensure the record is a dictionary
    if isinstance(record, dict):
        normalized_record = {key: record.get(key, template[key]) for key in template}
        normalized_data.append(normalized_record)
    else:
        print(f"Skipping invalid record: {record}")  # Log invalid entries for debugging
        # print(record)
for i, record in enumerate(data):
    if not isinstance(record, dict):
        print(f"Invalid record at index {i}: {record}")

# Verify normalization
# print(normalized_data[:5])



for record in normalized_data:
    # Example: Convert "applicants" to an integer if it's a string
    if record["applicants"] and isinstance(record["applicants"], str):
        try:
            record["applicants"] = int(record["applicants"])
        except ValueError:
            record["applicants"] = None  # Handle invalid formats


import pandas as pd

# Create a DataFrame
df = pd.DataFrame(normalized_data)

# Display the first few rows
print(df.head())


# Display the DataFrame
# print(df)


# Save normalized data to a new JSON file
output_file = 'normalized_data.json'
with open(output_file, 'w') as f:
    json.dump(normalized_data, f, indent=4)


# Load the JSON file and retrieve the record at index 2660
file_path = 'C:/Users/bar25/Downloads/8368.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Assuming 'data' is a list of dictionaries, print the record at index 2660
index = 2660

# Check if the index is within the bounds of the data list
if index < len(data):
    record_2660 = data[index]
    print(record_2660)  # Print the entire record at index 2660
else:
    print(f"Record at index {index} does not exist.")