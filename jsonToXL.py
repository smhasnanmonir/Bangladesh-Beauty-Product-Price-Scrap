import pandas as pd
import json

def json_to_excel(json_file, excel_file):
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Convert JSON data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to an Excel file
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Data successfully saved to {excel_file}")

# Call the function after JSON file is created
json_file = 'kmartAll.json'
excel_file = 'kmartAll.xlsx'
json_to_excel(json_file, excel_file)