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
async def get_csv_data(mobile_number: str, language: str):
    mobile_number = mobile_number[-10:]
    language = language.lower()
    data = read_csv_as_dict()
    customer_data = data.get(mobile_number)

    if customer_data:
        if language == "arabic":
             greeting = {
                "native_script": f"""مرحبًا {customer_data['Customer Name']}! أنا روبوت ADNIC هنا لمساعدتك. أرى أن لديك بوليصة {customer_data['Policy Type']} وصلاحيتها من {customer_data['Validity']}. كيف يمكنني مساعدتك؟""",
                "latin_script": f"""Marhaban {customer_data['Customer Name']}! Ana robot ADNIC huna limusa'adatik. Ara annaka ladayka bolisa {customer_data['Policy Type']} wa salahiyatuha min {customer_data['Validity']}. Kaifa yumkinuni musa'adatuk?"""
            }
                    
        else:
            greeting = f"Hello {customer_data['Customer Name']}! I am an ADNIC bot and I am here to assist you. I can see you have {customer_data['Policy Type']} policy and it has a validity from {customer_data['Validity']}. How may I assist you?"

        return JSONResponse(content={
            "payload": customer_data,
            "greeting_message": greeting
        })
    else:
        if language == "arabic":
            greeting = {
                "native_script": "مرحبًا! لم أتمكن من العثور على أي بوليصة نشطة مرتبطة برقمك. كيف يمكنني مساعدتك؟",
                "latin_script": "Marhaban! Lam atamakkan min aleuthur ealaa ayyi bolisa nashita murtabita biraqmuk. Kaifa yumkinuni musa'adatuk?"
            }
        else:
            greeting = "Hello there! Welcome to ADNIC. I couldn’t find any active policy linked to your number. How may I assist you?"

        return JSONResponse(content={
            "payload": {},
            "greeting_message": greeting
        })


knowledge_base = [
    {
        "question": "When was ADNIC founded and where is its headquarters located?",
        "answer": "ADNIC was founded in 1972 and is headquartered in Abu Dhabi, United Arab Emirates."
    },
    {
        "question": "What types of insurance products and services does ADNIC offer?",
        "answer": "ADNIC offers a wide range of insurance products including health, motor, travel, property, marine, aviation, and engineering insurance for both individuals and businesses."
    },
    {
        "question": "Is ADNIC a publicly listed company, and on which stock exchange does it trade?",
        "answer": "Yes, ADNIC is a publicly listed company and trades on the Abu Dhabi Securities Exchange (ADX) under the ticker symbol 'ADNIC'."
    },
    {
        "question": "In which regions does ADNIC operate, and how extensive is its network?",
        "answer": "ADNIC operates primarily in the UAE, but also serves the wider MENA region, with clients in Asia and Europe. It has branches and service centers across major UAE cities."
    },
    {
        "question": "Who are the major shareholders or key people associated with ADNIC?",
        "answer": "ADNIC's CEO is Charalampos Mylonas. While individual major shareholders are not publicly listed, the company is publicly traded and regulated by the Central Bank of the UAE."
    },
    {
        "question": "What are the main business segments of ADNIC?",
        "answer": "ADNIC operates in both consumer and commercial insurance segments, offering health, motor, property, engineering, marine, and specialty insurance."
    },
    {
        "question": "What regions does ADNIC serve?",
        "answer": "ADNIC primarily serves the UAE but also provides insurance solutions across the Middle East and North Africa (MENA) region, with services extending to Asia and Europe."
    },
    {
        "question": "Where is ADNIC headquartered, and where are its branches located?",
        "answer": "ADNIC is headquartered in Abu Dhabi, UAE, and has branches and service centers in Dubai, Sharjah, Al Ain, and other major UAE cities."
    }
]

@app.get("/knowledge-base")
async def get_knowledge_base():
    return JSONResponse(content={"knowledge_base": knowledge_base})
