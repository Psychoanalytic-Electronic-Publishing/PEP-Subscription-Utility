# PEP-Subscription-Utility

PEP-Subscription-Utility is a python lambda function which sends email notifications to PEP alert subscribed users. This function is triggered when a new journal data update xml file is stored in the configured AWS S3 bucket. The utility then:
1. Downloads and unzips the data update xml
2. Queries PaDS for subscribed users
3. Sends customized emails to users based on their video or journal preference

## Installation

```
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
