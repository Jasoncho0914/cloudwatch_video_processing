# Retrieving logs from Cloudwatch

__get_logs.py__: Retrieves last "N" logs of blackjack prototype, parse the logs and finds timestamps when Alexa utters "trigger words", which in this cases are "You bet, you stand, you hit", and saves those timestamps as a json in 'logs' folder. A json file produced by the code will look something like this.

{'00:00:00':'00:00:05',
'00:00:10':'00:00:32',
...}

the __key__ represents the start time of Alexa saying the "trigger words" and the __value__ represents the time Alexa answers the next command the user gave.

__get_logs_label.py__: Same as __get_logs.py__ but also outputs label. A json file produced by this code will look something like this.

{'Mistake Made-00:00:00':'00:00:05',
'No Mistake Made-00:00:10':'00:00:32',
...}

Example) Parsing 10 latest logs from Cloudwatch
```
python get_logs.py 10 
or
python get_logs_label.py 10 #this will also output labels 
```




# Clipping videos with FFMPEG

(working on it..)
