# Retrieving logs from Cloudwatch

__get_logs.py__: Retrieves last "N" logs of blackjack prototype, parse the logs and finds timestamps when Alexa utters "trigger words", which in this cases are "You bet, you stand, you hit", and saves those timestamps as a json in 'logs' folder. A json file produced by the code will look something like this.

{'00:00:00':'00:00:05',
'00:00:10':'00:00:32',
...}

the __key__ represents the start time of Alexa saying the "trigger words" and the __value__ represents the time Alexa answers the next command the user gave.

__get_logs_label.py__: Same as __get_logs.py__ but also outputs label. A json file produced by this code will look something like this.

{'10-Mistake Made-00:00:00':'00:00:05',
'You hit-No Mistake Made-00:00:10':'00:00:32',
...}

Example) Parsing 10 latest logs from Cloudwatch
```
python get_logs.py 10 
or
python get_logs_label.py 10 #this will also output labels 
```




# Clipping videos with FFMPEG

__auto_trim_1.py__: auto trim __one__ video. Syntax: python auto_trim_1.py LOGNAME VIDEONAME VIDEO_DELAY DURATION_OF_EACh_VIDEO

Example)
```
python auto_trim_1.py 2019/03/05/[$LATEST]df74413a62cb47cf923cf8a8788a0d23 Video/blackjack_demo_run2.MTS 9 5
```
This will produce short 5 second clips based on the log on Cloudwatch named 2019/03/05/[$LATEST]df74413a62cb47cf923cf8a8788a0d23. 
Based on correctness of Alexa's response, a clip will be either saved on Video/blackjack_demo_run2/Y or Video/blackjack_demo_run2/N. Each video will have 9 second lag. This assumes that Alexa started talking 9 seconds after we start recording.

Things to do:
1) Batch process (Multiple videos, multiple logs)
2) automatic Lag detection.
