import json
import requests
from main import conversation_id, job_id
import os
from dotenv import load_dotenv

load_dotenv()

baseUrl = 'https://api.symbl.ai/v1/job/1ebb5424-52c9-4785-82dc-0af568b1606f'

url = baseUrl.format(conversationId=5463337979871232)

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
    print("status => " + str(response.json()['status']))
elif response.status_code in responses.keys():
    print(responses[response.status_code])  # Expected error occurred
else:
    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

exit()
