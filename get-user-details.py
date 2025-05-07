from fastapi import FastAPI
from fastapi.responses import JSONResponse
import csv

app = FastAPI()

# Path to your CSV file
CSV_FILE_PATH = 'ADNIC_Dummy_Customer_Data.csv'

# Function to read CSV and return data as a dictionary using 'mobile_number' as key
def read_csv_as_dict():
    data_dict = {}
    try:
        with open(CSV_FILE_PATH, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                key = row.get("Phone Number")
                if key:
                    data_dict[key] = row
    except FileNotFoundError:
        return {"error": "CSV file not found."}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

    return data_dict

# Endpoint to return the CSV data
@app.get("/data")
async def get_csv_data(mobile_number: str):
    data = read_csv_as_dict()
    customer_data = data.get(mobile_number)

    if customer_data:
        customer_name = customer_data["Customer Name"]
        greeting = (
            f"Hello {customer_name}! I am an ADNIC bot and I am here to assist you. I can see you have {customer_data['Policy Type']} policy and it has a validity from {customer_data['Validity']}. How may I assist you?"
        )
        return JSONResponse(content={
            "payload": customer_data,
            "greeting_message": greeting
        })
    else:
        greeting = (
            "Hello there! Welocme to ADNIC. I couldn’t find any active policy linked to your number. How may I assist you?"
        )
        return JSONResponse(content={
            "payload": {},
            "greeting_message": greeting
        })
