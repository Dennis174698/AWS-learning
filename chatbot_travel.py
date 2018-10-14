import boto3
import json
comprehend = boto3.client(service_name='comprehend',region_name='us-east-1')

def pmt2(count_p,count_n):
    if count_p == 1:
        prompt = "That sounds like you had a great time"
    elif count_n == 1:
        prompt = "I am sorry to hear that"
    else :
        prompt = "That sounds ineresting"
    return prompt

def pmt(location,person,date):
    prompt=""
    if location>=1:
        pass
    if person>=1:
        pass
    if date>=1:
        prompt = "What do you think about this trip?"
    elif location<1:
        prompt = "Where are you going?"
    elif person<1:
        prompt = "who is travelling?"
    elif date<1:
        prompt = "What date will you be travelling?"
    else:
        prompt = "Tell me your trip"
    return prompt

message = ""
prompt = ""
location = 0
person = 0
date = 0
print("Tell me your trip, enter'quit'to exit")
while message !='quit':
    message = input(prompt)
    reply_1 = json.dumps(comprehend.detect_entities(Text=message,LanguageCode='en'),sort_keys=True,indent=4)
    count_l=reply_1.count('LOCATION')
    location = location + count_l
    count_p = reply_1.count('PERSON')
    person = person + count_p
    count_d = reply_1.count('DATE')
    date = date + count_d
    prompt = pmt(location,person,date)
    if prompt == 'What do you think about this trip?':
        message = input(prompt)
        reply_2 = json.dumps(comprehend.detect_sentiment(Text=message,LanguageCode='en'),sort_keys=True,indent=4)
        count_p=reply_2.count('POSITIVE')
        count_n = reply_2.count('NEGATIVE')
        prompt= pmt2(count_p,count_n)
        





                  
                  
