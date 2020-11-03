# Augusto BYOD helper v0.1

from helper import *
import requests
import time
TOTAL_COUNT="total_count"
META ="meta"
OBJECT = "objects"
EMAIL = "email"
RISK = "risk"
NAME = "name"
CHKP_RISK_HIGH = "3"
CHKP_RISK_MEDIUM = "2"
NOBLOCKED = 0
YESBLOCKED = 1
UPDATEOK = "204"


url_sbm = "https://amoralesintune.mt2.locsec.net/external_api/v1/device_status/?status_in=1"
payload_sbm = {}
headers_sbm = {
    'Authorization': 'ADD API KEY HERE'
}

url_ms = "https://graph.microsoft.com/v1.0/users/alice@onchkp.onmicrosoft.com"

payload_ms = "{\n  \"businessPhones\": [\n    \"businessPhones-value\"\n  ],\n  \"officeLocation\": \"LOCALIZATIONAUGUSTOCASA\",\n  \"accountEnabled\": false\n}\n"
headers_ms = {
  'SdkVersion': 'postman-graph/v1.0',
  'Content-Type': 'application/json',
    'Authorization': 'ADD AUTHORIZATION HEADER HERE'
}

class devicesbm():

    def __init__(self,email,risk,name,isblockedtmp):
        self.email = email
        self.name = name
        self.risk = risk

    def setemail(email):
        email = email

    def setrisk (risk):
        risk = risk

    def getemail(self):
        return self.email

    def getrisk(self):
        return self.risk

    def getname(self):
        return self.name

class metadatasbm():

    def __init__(self,total_count):
        self.total_count = total_count
        pass


    def get_total_count(self):
        return self.total_count


def getallstatuses():
    "Automatic"
    print("SBM - Getting status from Active Devices ... status (1)...")
    response = requests.request("GET", url_sbm, headers=headers_sbm, data=payload_sbm)
    #print(response.text.encode('utf8'))
    jsonResponse = response.json()
    #print("Print each key-value pair from JSON response")
    listofdevices = []
    counter = 0
    for key, value in jsonResponse.items():
        #print(key, ":", value)

        if key == OBJECT:
            for element in value:
                #print("Device Element: " + str(counter))
                #print("element[EMAIL]:  "+element[EMAIL])
                # AQUI ES DONDE AGREGO MAS CARACTERISTICAS
                aux = devicesbm(element[EMAIL], element[RISK],element[NAME],NOBLOCKED)
                listofdevices.append(aux)
                counter=+counter
            return listofdevices

        if key == META:
            pass
            #print("Creating metadata object... ")
            #metaobject = metadatasbm(value[TOTAL_COUNT])
            #print("Metaobject has # objects:  " + metaobject.get_total_count())


def getseveralstatus(*parameters):
    "Manual status"


def getonlyonestatus(user):
    "Getonlyone status"

#To implement... example of swith
def getspecificstatuses(mode,users):
    "mode can several statuses of specific users 1, or only one 2, return jsoninobject"
    switcher = {
        1: getseveralstatus(),
        2: getonlyonestatus(users)
    }
    func = switcher.get(users)
    return func

def updatestatus(user,flag):
    "User is the user to update, flag is ENABLE or DISABLE"
    print("To implement...")

def initialize():
    print("BYOD helper v0.1 cc Augusto Morales")

    mode = input("Automatic (1),  Manual (2)... : ")
    if mode == 1:
        print("Automatic mode selected...")
    else:
        if mode==2:
            print("To implement...")
    interval = input("Selecting check interval (10s default): ")
    print("Initializing...  ")
    return

def singletest():
    """Single test with Alice enabling account"""
    #print("Single test with alice")
    payload_ms = "{\n \"accountEnabled\": true\n}\n"
    url_ms = "https://graph.microsoft.com/v1.0/users/alice@onchkp.onmicrosoft.com"
    response = requests.request("PATCH", url_ms, headers=headers_ms, data=payload_ms)
    code = str(response.status_code)
    if str(response.status_code) == "204":
        print("MS - API working ok! ...code: "+code)
    else:
        print("Shit shit :-( ... saliendo")
        print("Error: "+code)
        print("Specific: "+str(response.content))
        #To implement generate new API key and try again

        exit(0)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    mode = initialize()
    singletest()
    #print("You have selected: "+mode)
    counter = 0
    listofblockedaccounts = []
    while (True):
        #break
        print("--------------------------")
        listofdevices = getallstatuses()
        time.sleep(5)
        print("Analyzing risk status ... default: CHKP_RISK_HIGH")
        time.sleep(5)

        for element in listofdevices:
            rstatus = element.getrisk()
            currentemail = str(element.getemail())
            if rstatus == CHKP_RISK_HIGH:
                    if  (currentemail not in listofblockedaccounts):
                        print("***************************************************")
                        print("MS - DISABLING ACCOUNT: "+element.getemail())
                        print("***************************************************")
                        payload_ms = "{\n \"accountEnabled\": false\n}\n"
                        url_ms="https://graph.microsoft.com/v1.0/users/"+currentemail
                        response = requests.request("PATCH", url_ms, headers=headers_ms, data=payload_ms)
                        if str(response.status_code) == UPDATEOK:
                            print("Blocked Correctly!... ")

                            listofblockedaccounts.append(currentemail)
                            #print("variable2: " + str(element.isblocked))
                        else:

                            print("Problem disabling account ")
                            print(str(response.content))
                    else:
                        print("MS - DISABLED Account: "+str(currentemail)+"-- Device Name: "+element.getname() )
                        #print("is blocked? "+str(element.isblocked))

            else:
                print("MS - ENABLED Account: "+currentemail+" -- Device Name: "+element.getname())
                #print("IS BLOCKED? 1 SI, 0 NO: "+str(element.isblocked))

                if currentemail in listofblockedaccounts:
                #if element.isblocked == YESBLOCKED:
                    print("Unlocking account: " + currentemail)
                    payload_ms = "{\n \"accountEnabled\": true\n}\n"
                    url_ms = "https://graph.microsoft.com/v1.0/users/" + currentemail
                    response = requests.request("PATCH", url_ms, headers=headers_ms, data=payload_ms)
                    if str(response.status_code) == UPDATEOK:
                        print("Enabled Correctly... ")
                        #element.isblocked = NOBLOCKED
                        listofblockedaccounts.remove(currentemail)

                    else:
                        print("Problem enabling account: ")

