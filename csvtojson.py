import pandas as pd
import json
import ast

def convert_social_csv_to_json(csv_file_path, json_file_path):
    """
    Convert the social connections CSV to a clean JSON format.
    
    Args:
        csv_file_path (str): Path to the input CSV file
        json_file_path (str): Path to the output JSON file
    """
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Process the data
    processed_data = []
    
    for _, row in df.iterrows():
        # Parse the groups string safely
        groups = []
        try:
            groups_string = row['Friend Group / Known Associations']
            if pd.notna(groups_string) and groups_string.strip():
                # Convert string representation of list to actual list
                groups = ast.literal_eval(groups_string)
        except (ValueError, SyntaxError) as e:
            print(f"Warning: Could not parse groups for {row['Name']}: {e}")
            groups = []
        
        # Handle notable person (convert NaN to None)
        notable_person = row['Any Notable Person in Common']
        if pd.isna(notable_person):
            notable_person = None
        
        # Create the person object
        person = {
            "name": row['Name'],
            "groups": groups,
            "FSize": float(row['Node Size']) if pd.notna(row['Node Size']) else 0.0,
            "notablePerson": notable_person,
            "groupCount": int(row['Group Count']) if pd.notna(row['Group Count']) else 0
        }
        
        processed_data.append(person)
    
    # Write to JSON file with pretty formatting
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {len(processed_data)} records from {csv_file_path} to {json_file_path}")
    

# Example usage
if __name__ == "__main__":
    # Convert the CSV to JSON
    #convert_social_csv_to_json('Data/processed_social_connections.csv', 'social_network_data.json')
    convert_social_csv_to_json('Data/anonymized_social_connections.csv', 'hidden_social_network_data.json')
    
    # Optional: Validate the JSON by reading it back
    try:
        with open('hidden_social_network_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"\nValidation: Successfully loaded {len(data)} records from JSON file")
    except Exception as e:
        print(f"Error validating JSON file: {e}")