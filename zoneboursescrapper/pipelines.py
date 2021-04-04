# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

from itemadapter import ItemAdapter

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from scrapy.utils.project import get_project_settings


class JsonWriterPipeline:
    output_sheet = None
    service = None

    def open_spider(self, spider):
        creds = None
        settings = get_project_settings()

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', settings.get('SCOPES'))
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', settings.get('SCOPES'))
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)
        self.output_sheet = self.service.spreadsheets()

    def process_item(self, item, spider):
        settings = get_project_settings()
        # values = []
        # result = self.output_sheet.values().get(spreadsheetId=settings.get('SPREADSHEET_ID'),
        #                                         range=settings.get('COMPANIES_RANGE')).execute()
        return item


class ZoneboursescrapperPipeline:
    def process_item(self, item, spider):
        return item
