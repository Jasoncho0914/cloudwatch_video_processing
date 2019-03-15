import boto3
import datetime
import re
import numpy as np
import sys
import json


def get_response_list(N_interactions):
    cloudwatch = boto3.client('logs',region_name='us-east-1')
    response = cloudwatch.describe_log_streams(
        logGroupName='/aws/lambda/blackjack_prototype',
        orderBy='LastEventTime',
        descending=True,
        limit=N_interactions
    )
    response_list = [i['logStreamName'] for i in response['logStreams']]

    return response_list


def get_timestamps(logStreamName,
                   trigger_words = ["You bet","you bet","You hit","you hit","You stand","you stand"],
                   logGroupName='/aws/lambda/blackjack_prototype',
                   lag=0):
    cloudwatch = boto3.client('logs',region_name='us-east-1')

    response = cloudwatch.get_log_events(
        logGroupName='/aws/lambda/blackjack_prototype',
        logStreamName=logStreamName,
        startFromHead=True
    )

    M_flag = 0
    you_bet = ["You bet","you bet"]
    back = 0
    ret_dict={}
    lag=0
    start_time = datetime.datetime.fromtimestamp(round(response['events'][0]['timestamp']/1000))
    for each in response['events']:
        try:

            if "Mistake made" in each['message']:
                M_flag = 1

            Alexa_s = re.findall(r'<speak>([\s\S]*?)<\/speak>',each['message'])[0]
            t_converted = datetime.datetime.fromtimestamp(round(each['timestamp'] / 1000))
            timestamp_1 = t_converted-start_time+datetime.timedelta(seconds=lag)

            if back == 1:
                ret_dict[key] = str(timestamp_1)
                back = 0

            for t_word in trigger_words:
                if t_word in Alexa_s:
                    if M_flag == 1:
                        key = str("Mistake made"+"-"+str(timestamp_1))
                        M_flag = 0
                    else:
                        key = str("No Mistake made"+"-"+str(timestamp_1))
                    
                    if t_word in you_bet:
                        new_p = re.findall(r'(?<=<say-as interpret-as=\\"cardinal\\">)(.*)(?=<\/say-as> <break time=\\"100ms\\"\/>)',Alexa_s)[0]
                        key = new_p+"-"+key
                    else:
                        key = t_word+"-"+ key
                    
                    ret_dict[key]=None    
                    back = 1

        except IndexError:
            continue
    return ret_dict



if "__main__":
    counter = 0
    for i in get_response_list(int(sys.argv[1])):
        output = get_timestamps(logStreamName=i,lag=8)
        return_name = i[:11].replace('/','_')+i[-8:]+'.json'
        with open('logs/'+return_name, 'w') as outfile:
            json.dump(output, outfile)
