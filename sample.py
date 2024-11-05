def delete_nested_objects(d):
    """Recursively delete all nested objects within a dictionary."""
    # Iterate over each item in the dictionary
    for key, value in list(d.items()):
        if isinstance(value, dict):
            # If value is a nested dictionary, recurse into it
            delete_nested_objects(value)
            d[key].clear()
        elif isinstance(value, list):
            # If value is a list, clear each nested dictionary in the list
            for item in value:
                if isinstance(item, dict):
                    delete_nested_objects(item)
            value.clear()
        # Delete the item in the dictionary itself
        del d[key]
        
    d.clear()  # Finally, clear the outermost dictionary

# Example usage
data = {
    "level1": {
        "level2": {
            "key1": "value1",
            "key2": {"key3": "value3"}
        },
        "level2_list": [
            {"list_key1": "list_value1"},
            {"list_key2": "list_value2"}
        ]
    }
}

delete_nested_objects(data)
print(data)  # Output will be an empty dictionary
