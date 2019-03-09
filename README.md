# cloudwatch_video_processing

get_logs.py: Retrieves last "N" logs of blackjack prototype, parse the logs and parse timestamps when Alexa utters "trigger words", which in this cases are "You bet, you stand, you hit", and saves those timestamps in json format in 'logs' folder. A json file produced by the code will look something like this.

{'00:00:00':'00:00:05',
'00:00:10':'00:00:32',
...}

Key: start time of the video to be clipped
value: end time of the video to be cliiped


Example)
```
python get_logs.py 10 
```

Above command will retrieve latest 10 logs from Cloudwatch. 
