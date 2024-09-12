import asyncio
import aiohttp
import os
import time
import json

# Define the folder containing the request files
folder_path = './requests'  # Replace with your folder path

# Function to read files that start with 'request_' from the specified folder
def get_request_files(folder):
    return [os.path.join(folder, file) for file in os.listdir(folder) if file.startswith('request_')]

# Asynchronous function to make an API call
async def make_api_call(session, url, payload):
    try:
        start_time = time.time()
        async with session.post(url, json=payload) as response:
            elapsed_time = time.time() - start_time
            status = response.status
            response_text = await response.text()
            print(f"Response Status: {status}, Time Taken: {elapsed_time:.2f} seconds, Response: {response_text}")
    except Exception as e:
        print(f"Error making request: {e}")

# Asynchronous function to process request files and make API calls
async def process_request_files():
    url = 'http://localhost:5000/your-api-endpoint'  # Replace with your API endpoint
    request_files = get_request_files(folder_path)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for file_path in request_files:
            with open(file_path, 'r') as file:
                payload = json.load(file)  # Assuming each file contains a JSON payload
                tasks.append(make_api_call(session, url, payload))
        
        await asyncio.gather(*tasks)  # Run all tasks concurrently

# Main function to run the asynchronous tasks
async def main():
    await process_request_files()

# Run the main function
asyncio.run(main())
