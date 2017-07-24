import os
import json
from flask import Flask, request, jsonify
import twitter

app = Flask(__name__)

intro_message = """Welcome to Nexmo's talking Twitter. 
Please select from the following options. To hear the latest breaking 
news press 1. For showbiz gossip press 2. If you'd like to hear the latest
#API tweets press 3. Or for tweets by Aaron Bassett press 4."""

event_url = "https://<YOUR SERVER URL>/ivr/"

@app.route('/')
def start_call():
    return jsonify([
        {
            'action': 'talk',
            'text': intro_message,
            'voice_name': 'Amy',
            'bargeIn': 'true'
        },
        {
            'action': 'input',
            'maxDigits': 1,
            "eventUrl": [event_url]
        }
    ])


@app.route('/ivr/', methods=['POST'])
def ivr():
    inbound = json.loads(request.data)

    twitter_client = twitter.Api(
        os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET'],
        os.environ['TWITTER_ACCESS_KEY'],
        os.environ['TWITTER_ACCESS_SECRET']
    )

    if inbound['dtmf'] == '1':
        statuses = twitter_client.GetUserTimeline(
            screen_name='washingtonpost'
        )
    elif inbound['dtmf'] == '2':
        statuses = twitter_client.GetUserTimeline(
            screen_name='FakeShowbizNews'
        )
    elif inbound['dtmf'] == '3':
        statuses = twitter_client.GetSearch('#API')
    elif inbound['dtmf'] == '4':
        statuses = twitter_client.GetUserTimeline(
            screen_name='aaronbassett'
        )
    else:
        statuses = None
    
    if statuses:
        ncco = []

        for status in statuses:
            ncco.append({
                'action': 'talk',
                'text': status.text,
                'voice_name': 'Joey'
            })
    else:
        ncco = [
            {
                'action': 'talk',
                'text': 'Sorry I did not understand that. Please try again',
                'voice_name': 'Chipmunk'
            },
            {
                'action': 'talk',
                'text': intro_message,
                'voice_name': 'Amy',
                'bargeIn': 'true'
            },
            {
                'action': 'input',
                'maxDigits': 1,
                "eventUrl": [event_url]
            }
        ]

    return jsonify(ncco)