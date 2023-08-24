import json
import requests
from main import conversation_id, job_id
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

baseUrl = 'https://api.symbl.ai/v1/conversations/{conversationID}/summary?refresh=true}'

url = baseUrl.format(conversationId=6378794823974912)

access_token = os.getenv("symbl_api")

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

responses = {
    401: 'Unauthorized. Please generate a new access token.',
    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
    500: 'Something went wrong! Please contact support@symbl.ai'
}

response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    print("topics => " + str(response.json()['summary']))
elif response.status_code in responses.keys():
    print(responses[response.status_code])  # Expected error occurred
else:
    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

exit()
