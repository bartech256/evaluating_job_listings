import json
import os
import pandas as pd
import glob
from typing import List, Dict, Any

def remove_duplicates_from_json(input_file, output_file):
    try:
        # Load the JSON file with explicit encoding
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Check if the data is a list (common for JSON arrays)
        if isinstance(data, list):
            # Create a DataFrame to drop duplicates
            df = pd.DataFrame(data)
            df_cleaned = df.drop_duplicates()

            # Convert back to a list of dictionaries
            cleaned_data = df_cleaned.to_dict(orient='records')

            # Count the number of records in the cleaned data
            record_count = len(cleaned_data)
            print(f"Number of records in the cleaned JSON: {record_count}")
        else:
            print("The JSON structure is not a list. No duplicates to remove.")
            return

        # Save the cleaned data to a new JSON file with explicit encoding
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, indent=4)

        print(f"Duplicates removed. Cleaned data saved to '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


def consolidate_json_files(directory_path: str, output_file: str) -> None:
    """
    Consolidates all JSON files in the given directory into a single JSON file,
    removing any duplicates.

    Args:
        directory_path: Path to directory containing JSON files
        output_file: Path where the consolidated JSON file will be saved
    """
    # Ensure the directory path ends with a slash
    directory_path = os.path.join(directory_path, '')

    # Get all JSON files in the directory
    json_files = glob.glob(directory_path + "*.json")

    if not json_files:
        print(f"No JSON files found in {directory_path}")
        return

    # List to store all JSON data
    all_data: List[Dict[str, Any]] = []

    # Read each JSON file
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # Handle both single objects and lists of objects
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)

        except json.JSONDecodeError:
            print(f"Error reading {file_path}: Invalid JSON format")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    # Remove duplicates by converting to string representation
    unique_data = []
    seen = set()

    for item in all_data:
        item_string = json.dumps(item, sort_keys=True)
        if item_string not in seen:
            seen.add(item_string)
            unique_data.append(item)

    # Write consolidated data to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(unique_data, file, indent=4)
        print(f"Successfully consolidated {len(json_files)} files into {output_file}")
        print(f"Found {len(all_data)} total records")
        print(f"Removed {len(all_data) - len(unique_data)} duplicates")
        print(f"Final unique records: {len(unique_data)}")
    except Exception as e:
        print(f"Error writing output file: {str(e)}")




# Usage example
if __name__ == "__main__":
    # input_file = input("Enter the path to the input JSON file: ").strip()
    # output_file = input("Enter the path to save the output JSON file: ").strip()
    # remove_duplicates_from_json(input_file, output_file)

    consolidate_json_files("/data", "/data")


