from fastapi import FastAPI
from fastapi.responses import JSONResponse
import csv

app = FastAPI()

# Path to your CSV file
CSV_FILE_PATH = 'ADNIC_Dummy_Customer_Data.csv'

# Function to read CSV and return data as a dictionary using 'phonenumber' as key
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
async def get_csv_data(phonenumber: str):
    data = read_csv_as_dict()
    if isinstance(data, dict) and phonenumber in data:
        return JSONResponse(content={"payload": data[phonenumber]})
    else:
        return JSONResponse(content=data, status_code=400)
