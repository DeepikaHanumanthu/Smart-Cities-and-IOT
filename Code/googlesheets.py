from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

#import sensortag_v1

import socket
import datetime

mySSID = "1SFpD_hsCB7QHluVPIU4IxNRzR4Wxg0M0hRt_OAg1Czs"

def init_auth():
    
    SCOPES = "https://www.googleapis.com/auth/spreadsheets"
    creds=None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    #creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', SCOPES)
    #creds= ServiceAccountCredentials.from_json_keyfile_name('My_First_Project.json', SCOPES)
    #service = build('sheets', 'v4', http=creds.authorize(Http()))
    service = build('sheets', 'v4', credentials=creds)
    return service

def update_sheet(service,sheetname, dataDict):

    #values = [[str(datetime.datetime.now()), 'Piezo data', piezo, 'Gas', gasSensor,
    #          'Humidity', '', 'Gyro x', '', 'Gyro y', '', 'Gyro z', '', 'Motion',
    #          '', 'Flame', '']]
    
    values = [[dataDict["timeStamp"],dataDict["Piezo_Data"], dataDict["MQ2_Data"], dataDict["imu"], '1', '2']]
    body = {'values':values}
    
    result = service.spreadsheets().values().append(
        spreadsheetId=mySSID,
        range=sheetname + '!A1:F1',
        valueInputOption='RAW',body=body).execute()
        #insertDataOption='INSERT_ROWS',"""
    

def main():
    service=init_auth()
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 10000
    serv.bind(("", port))
    serv.listen(2)
    print("listening for 1 client!!!")
    dataDict = {}

    while True:
        
        (conn, address) = serv.accept()
        dataDict["timeStamp"] = str(datetime.datetime.now())
        
        try:
        
            print("connection from: "+ str(address))
            while (True):
                data = conn.recv(4096).decode('utf-8')
                if data:
                    print(data)
                    data = data.split(" : ")
                    dataDict[data[0]] = data[1]
                    if len(dataDict.keys()) == 4:
                        update_sheet(service,"syndata", dataDict)
                        dataDict = {}
                    conn.sendall('recieved it!!!'.encode('utf-8'))
                    
                else:
                    #print ('no data!!')
                    break
                
                
                
        finally:
            #print("connection didnt happen!!")
            conn.close()
            
    serv.close()
            
if __name__ == "__main__":
    main()