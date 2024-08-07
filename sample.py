from google.cloud import bigquery

def print_column_names(project_id, dataset_id, table_id):
    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Construct a fully-qualified table ID
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    # Get the table schema
    table = client.get_table(table_ref)
    schema = table.schema
    
    # Print the column names
    print(f"Column names in table {table_id}:")
    for field in schema:
        print(field.name)

# Example usage
project_id = 'your-project-id'
dataset_id = 'your-dataset-id'
table_id = 'your-table-id'

print_column_names(project_id, dataset_id, table_id)
