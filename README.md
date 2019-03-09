# Retrieving logs from Cloudwatch

__get_logs.py__: Retrieves last "N" logs of blackjack prototype, parse the logs and finds timestamps when Alexa utters "trigger words", which in this cases are "You bet, you stand, you hit", and saves those timestamps as a json in 'logs' folder. A json file produced by the code will look something like this.

{'00:00:00':'00:00:05',
'00:00:10':'00:00:32',
...}

the __key__ represents the start time of Alexa saying the "trigger words" and the __value__ represents the time Alexa answers the next command the user gave.

Example)
```
python get_logs.py 10 #10 latest logs of people using the blackjack prototype
```

# Clipping videos with FFMPEG

(working on it..)
