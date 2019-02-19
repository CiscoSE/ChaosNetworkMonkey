#!/usr/bin/python
# -*- coding: utf-8 -*-

# import Flask

from flask import Flask, request

# import  custom-made modules

import resolveUser
import servicenow
import settings
import sparkmessages
import apicem
import device
import host
import path
from chatterbot import ChatBot
from chatterbot.training.trainers import ChatterBotCorpusTrainer
from chatterbot.training.trainers import ListTrainer
# Create an instance of Flask

app = Flask(__name__)

chatbot = ChatBot("APIC-EM", output_adapter="chatterbot.adapters.output.OutputFormatAdapter", format='text', input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter", logic_adapters=["chatterbot.adapters.logic.ClosestMatchAdapter", "chatterbot.adapters.logic.MathematicalEvaluation"])
    

trainlist = [
    'Hello',
    'Hello',
    'What is your name?',
    'My name is APIC-EM',
    'Whats the weather like?',
    'Cloudy ;-)',
    'Tell me a joke',
    'I could tell you a joke about UDP, but you might not get it',
    'What is the meaning of life?',
    '42',
    ]
chatbot.set_trainer(ListTrainer)    
chatbot.train(trainlist)


#chatbot = ChatBot('APIC-EM',
#                  logic_adapters=['chatterbot.adapters.logic.EvaluateMathematically',
#                  'chatterbot.adapters.logic.ClosestMatchAdapter',
#                  'chatterbot.adapters.logic.TimeLogicAdapter',
#                  'chatterbot.adapters.logic.ClosestMeaningAdapter'])
chatbot.set_trainer(ChatterBotCorpusTrainer)                  

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")

# Train based on english greetings corpus
#chatbot.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
chatbot.train("chatterbot.corpus.english.conversations")


# Index page will trigger index() function

@app.route('/')
def index():
    return 'Nothing to see here'


# Webhook page will trigger webhooks() function

@app.route('/webhook/', methods=['POST'])
def webhooks():
    print 'Lets go!'

    # Get the json data

    json = request.json

    # parse the message id, person id, person email, and room id

    message_id = json['data']['id']
    person_id = json['data']['personId']
    person_email = json['data']['personEmail']
    room_id = json['data']['roomId']

    apic_person_id = settings.apic_person_id
    apic_person_email = settings.apic_person_email
    print message_id

    # convert the message id into readable text

    spark = sparkmessages.Message()
    (message, sender) = spark.get_message(message_id)

    print 'Message... \n'

    # message = getmessage.main(message_id)

    print message

    # check if the message is the command to get hosts

    message = message.lower()
    if message == 'get hosts':
        apic_host = host.Host()
        response = apic_host.get_all_hosts()
        spark.post_message(apic_person_id, apic_person_email, room_id,
                           response)
        del apic_host
    elif message.startswith('get host'):
        name = message.rsplit(None, 1)[-1]
        apic_host = host.Host()
        message = apic_host.get_individual_host(name)
        spark.post_message(apic_person_id, apic_person_email, room_id,
                           message)
        del apic_host
    elif message.startswith('get path'):
        apic_path = path.Path()
        response = apic_path.path_trace(message)
        spark.post_message(apic_person_id, apic_person_email, room_id,
                           response)
        del apic_path
    elif message.startswith('get network health'):
        apic_device = device.Device()
        message = apic_device.get_health_all()
        spark.post_message(apic_person_id, apic_person_email, room_id,
                           message)
        del apic_device
    elif message.startswith('raise'):
        servicenow.raise_case(message)
    elif message.startswith('devices in'):
        location = message.split()[2]
        print location
        apic_device = device.Device()
        response = apic_device.get_devices_location(location)
        spark.post_message(apic_person_id, apic_person_email, room_id,
                           response)
        del apic_device
    else:
        if sender != settings.apic_person_email:
            returntext = chatbot.get_response(message)
            text = returntext.__str__()
            print 'chatbot response: %s' % text
            spark.post_message(apic_person_id, apic_person_email, room_id, text)
            print 'calling output'

# run the application

if __name__ == '__main__':
    app.run(host='172.31.63.81')
