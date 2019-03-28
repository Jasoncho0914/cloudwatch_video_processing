import boto3
import datetime
import re
import numpy as np
import sys
import subprocess
import os
import json

# def get_response(N_interactions):
#     cloudwatch = boto3.client('logs',region_name='us-east-1')
#     response = cloudwatch.describe_log_streams(
#         logGroupName='/aws/lambda/blackjack_prototype',
#         orderBy='LastEventTime',
#         descending=True,
#     )
#     response_list = [i['logStreamName'] for i in response['logStreams']]
#
#     return response_list


def get_timestamps_v2(logStreamName,
                   lag,
                   duration,
                   trigger_words = ["You bet","you bet","You hit","you hit","You stand","you stand"],
                   logGroupName='/aws/lambda/blackjack_prototype'):
    cloudwatch = boto3.client('logs',region_name='us-east-1')

    response = cloudwatch.get_log_events(
        logGroupName='/aws/lambda/blackjack_prototype',
        logStreamName=logStreamName,
        startFromHead=True
    )

    you_bet = ["You bet","you bet"]
    ret_dict={}
    M_flag = 0
    start_time = datetime.datetime.fromtimestamp(round(response['events'][0]['timestamp']/1000))

    for each in response['events']:
        try:
            Alexa_s = re.findall(r'<speak>([\s\S]*?)<\/speak>',each['message'])[0]
            t_converted_start = datetime.datetime.fromtimestamp(round(each['timestamp'] / 1000))
            t_converted_end = datetime.datetime.fromtimestamp(round(each['ingestionTime'] / 1000))
            timestamp_1 = t_converted_start-start_time+datetime.timedelta(seconds=lag)
            timestamp_2 = timestamp_1 +datetime.timedelta(seconds=duration)

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

                    ret_dict[key]=str(timestamp_2)
        except IndexError:
            continue
    return ret_dict

def trimming(videoname,datastore):
    # videoname = "Video/blackjack_demo_run2.MTS"

    # with open('logs/2019_03_05_788a0d23.json', 'r') as f:
    #     datastore = json.load(f)

    # datastore = ret_dict

    path_ = videoname.split('.')[0]
    path_y = path_+"/Y"
    payh_n = path_+"/N"

    if not (os.path.isdir(path_)):
        os.mkdir(path_)

    if not (os.path.isdir(path_y)):
        os.mkdir(path_y)

    if not (os.path.isdir(payh_n)):
        os.mkdir(payh_n)

    name_c = 0
    for key in datastore:
        alexa_said = key.split('-')[0]
        mistakemade = key.split('-')[1]
        start = key.split('-')[2]
        end = datastore[key]

        if mistakemade == "No Mistake made":
            path = path_y
        else:
            path = payh_n


        if end != None:
            start_s = datetime.datetime.strptime(start,'%H:%M:%S')
            end_s = datetime.datetime.strptime(end,'%H:%M:%S')
            dif = end_s-start_s
            dur = "00:00:"+str(dif.seconds)
            command = "ffmpeg"+ " -i "+ videoname +" -ss "+ '0'+start +" -to " + '0'+end + " -c copy " + path + "/"+"0000"+str(name_c)+".MTS"
            name_c += 1
            print(command)
        else:
            command = "ffmpeg"+ " -i "+ videoname +" -ss "+ '0'+start + " -c copy " + path + "/"+"0000"+str(name_c)+".MTS"
            name_c += 1
            print(command)
            continue
        subprocess.call(command, shell=False)

if "__main__":
    output = get_timestamps_v2(logStreamName=sys.argv[1],lag=int(sys.argv[3]),duration=int(sys.argv[4]))
    return_name = sys.argv[2].split('/')[1].split('.')[0]+'.json'

    #Saving the log file
    with open('logs/'+return_name, 'w') as outfile:
        json.dump(output, outfile)

    trimming(sys.argv[2],output)
