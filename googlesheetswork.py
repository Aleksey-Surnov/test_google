import os
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service_sacc():

    creds_json = "gs_my_credentials.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    try:
        creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
        return build('sheets', 'v4', http=creds_service)
    except FileNotFoundError:
        print(f'ERROR: Вы не создали файл {creds_json} в папке проекта для сервисного аккаунта Google.')
    except Exception as e:
        print(f'ERROR: {e}\n Возможна ошибка в заполнении файла: {creds_json}')


class GoogleSheetWork:
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self, service_result):
        self.service = build('sheets', 'v4', http=service_result)
