import json
from dotenv import load_dotenv
import requests
import os


load_dotenv()

url = "https://api.symbl.ai/v1/process/audio"

payload = None
numberOfBytes = 0

try:
    # Assuming the audio file is in the same directory as your script
    audio_file_path = 'audio\meeting with Tom part 1.mp3'
    audio_file = open(audio_file_path, 'rb')
    payload = audio_file.read()
    numberOfBytes = len(payload)
except FileNotFoundError:
    print(f"Could not read the file provided at {audio_file_path}.")
    exit()


# set your access token here. See https://docs.symbl.ai/docs/developer-tools/authentication
access_token = os.getenv("symbl_api")


headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Length': str(numberOfBytes),  # This should correctly indicate the length of the request body in bytes.
    'Content-Type': 'audio/mp3'
}

params = {
  'name': "Shopify Shahar",
  'languageCode':'en-US',
  'confidenceThreshold': 0.5,
  'detectPhrases':'true',
  'enableSpeakerDiarization':'true',
  'diarizationSpeakerCount':2
};

responses = {
    400: 'Bad Request! Please refer docs for correct input fields.',
    401: 'Unauthorized. Please generate a new access token.',
    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
    429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
    500: 'Something went wrong! Please contact support@symbl.ai'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 201:
    # Successful API execution
    conversation_id = response.json()['conversationId']  # Save to variable
    job_id = response.json()['jobId']  # Save to variable
    print("conversationId => " + response.json()['conversationId'])  # ID to be used with Conversation API.
    print("jobId => " + response.json()['jobId'])  # ID to be used with Job API.
elif response.status_code in responses.keys():
    print(responses[response.status_code])  # Expected error occurred
else:
    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

exit()