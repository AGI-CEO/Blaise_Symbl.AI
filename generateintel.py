import requests
import os
from dotenv import load_dotenv
import csv
from bs4 import BeautifulSoup


load_dotenv()

baseUrl = "https://api.symbl.ai/v1/conversations/6378794823974912/messages?sentiment=true&verbose=true"
conversationId = '6378794823974912'

url = baseUrl.format(conversationId=conversationId)

access_token = os.getenv("symbl_api")

headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

params = {
    'verbose': True,
    'sentiment': True
}

responses = {
    401: 'Unauthorized. Please generate a new access token.',
    404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
    500: 'Something went wrong! Please contact support@symbl.ai'
}

response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    # Successful API execution
    print("messages => " + str(response.json()['messages']))  # messages is a list of id, text, from, startTime, endTime, conversationId, words, phrases, sentiment
    messages = response.json()['messages']
    soup = BeautifulSoup("", 'html.parser')

    # HTML structure
    html = soup.new_tag('html')
    soup.insert(0, html)
    head = soup.new_tag('head')
    html.insert(0, head)
    body = soup.new_tag('body')
    html.insert(1, body)

    # Link to Bootstrap CSS
    bootstrap_link = soup.new_tag('link',
                                  rel='stylesheet',
                                  href='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css')
    head.insert(0, bootstrap_link)

    # Container for conversation
    container = soup.new_tag('div', **{'class': 'container mt-4'})
    body.insert(0, container)

    # Add conversation
    for message in messages:
        text = message['text']
        p = soup.new_tag('p')
        p.string = text
        container.insert(len(container.contents), p)

    # Save HTML to file
    with open('conversation.md', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print("HTML page saved to conversation.md")
elif response.status_code in responses.keys():
    print(responses[response.status_code])  # Expected error occurred
else:
    print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

exit()