import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SPREADSHEET_ID="1LT94_hr_NUEtmMs4zzbnwjTF4TcaWC1rZ0wyhdtpowg"
SCOPES=["https://www.googleapis.com/auth/spreadsheets"]

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Folha1!A1:C12').execute()
    values = result.get('values', [])
    print(values)

    valores_adicionar = [
        ["Dezembro", "R$ 70.000,00"],
        ["Janeiro/22", "R$80.000,00"],
        ["Fevereiro/22", "R$127.352,00"],
    ]
    sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Round1!A1', valueInputOption="RAW",
                        body={"values": valores_adicionar}).execute()
except HttpError as err:
    print(err)