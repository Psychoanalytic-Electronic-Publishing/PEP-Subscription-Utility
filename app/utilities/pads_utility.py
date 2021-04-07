import boto3
import requests
import json
import os

secretsmanager_client = boto3.client('secretsmanager')


def get_pads_token():
    try:
        response = secretsmanager_client.get_secret_value(
            SecretId=os.environ.get('PADS_AUTH_TOKEN_SECRET'))
        return response['SecretString']
    except Exception as err:
        print(f'Error getting pads token from secrets manager: {err}')
        raise


def get_pads_users():
    try:
        token = get_pads_token()
        response = requests.get(
            os.environ.get('PADS_USERALERTS_URL'), headers={'UserAlertSecurityKey': token})
        # TODO temporarily converting to json twice as UserAlertInfo is currently returned as a string
        json_response = json.loads(response.text)
        return json.loads(json_response['UserAlertInfo'])['UserAlerts']
    except Exception as err:
        print(f'Error getting pads users: {err}')
        raise

