# Campus Texter
Sends graded assignments from Infinite Campus with SMS

## Requirements
* Infinite Campus Account
* Twilio Account
* Python 3.4
* Cron or a similar schedular

## Installation
After cloning the repository, fill out *example_settings.py* and rename it to *settings.py*. Then install the dependencies:
```
pip install requests beautifulsoap4 twilio
```

Next, add a cron job to run the script every hour
```
0 * * * * cd location/of/campus-texter && python3 main.py
```
