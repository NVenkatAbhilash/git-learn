import pandas as pd
import math

# Function to split a CSV file into smaller files
def split_csv(input_file, rows_per_file=500):
    # Read the input CSV file
    df = pd.read_csv(input_file)
    total_rows = len(df)
    
    # Calculate the number of files needed
    num_files = math.ceil(total_rows / rows_per_file)
    
    # Split the DataFrame and save smaller CSV files
    for i in range(num_files):
        start_row = i * rows_per_file
        end_row = start_row + rows_per_file
        chunk = df[start_row:end_row]
        
        # Save each chunk as a new CSV file
        output_file = f"{input_file.split('.')[0]}_part{i + 1}.csv"
        chunk.to_csv(output_file, index=False)
        print(f"Created: {output_file}")

# Example usage
input_file = "large_file.csv"  # Replace with your CSV file
split_csv(input_file, rows_per_file=500)
