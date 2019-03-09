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


    trigger_words = trigger_words
    back = 0
    lag = lag
    ret_dict = {}
    start_time = datetime.datetime.fromtimestamp(round(response['events'][0]['timestamp']/1000))
    for each in response['events']:
        try:
            Alexa_s = re.findall(r'<speak>([\s\S]*?)<\/speak>',each['message'])[0]
            if back == 1:
                t_converted = datetime.datetime.fromtimestamp(round(each['timestamp'] / 1000))
                timestamp_1 = t_converted-start_time+datetime.timedelta(seconds=lag)
                ret_dict[key] = str(timestamp_1)
                back = 0
            for t_word in trigger_words:
                if t_word in Alexa_s:
                    each['timestamp']
                    t_converted = datetime.datetime.fromtimestamp(round(each['timestamp'] / 1000))
                    timestamp_1 = t_converted-start_time+datetime.timedelta(seconds=lag)
                    ret_dict[str(timestamp_1)]=None
                    key = str(timestamp_1)
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
