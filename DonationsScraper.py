import requests
import json
import math
s = requests.Session()
#list of intl schools: ()
FEC_key = 'vYPKUmsd6xZNfsOafhXj7Q9mb9jseNtWv7h2PEZJ'
EmpNoP = ''
EmP = EmpNoP.replace(' ', "+")
Ecycle = '2020' #2019-2020

partDict = {
    'ACTBLUE': 'DEM',
    'WINRED': 'REP',
    'BIDEN FOR PRESIDENT': 'DEM',
    'JAIME HARRISON FOR US SENATE': 'DEM',
    'WARREN FOR PRESIDENT, INC.': 'DEM',
    'BERNIE 2020': 'DEM',
    'KAMALA HARRIS FOR THE PEOPLE': 'DEM',
    'REPUBLICAN NATIONAL COMMITTEE': 'REP',
    'NRSC': 'REP',
    'BERNIE 2016': 'DEM',
    'MOVEON.ORG POLITICAL ACTION': 'DEM',
    'AELEA FOR CONGRESS': 'DEM',
    'OBAMA FOR AMERICA': 'DEM',
    'DEAN FOR AMERICA': 'DEM',
    '': '',
    '': '',
    '': '',
    '': '',
}

getByEmployerLink = f'https://api.open.fec.gov/v1/schedules/schedule_a/?api_key={FEC_key}&sort_hide_null=false&sort_nulls_last=false&contributor_employer={EmP}&sort=-contribution_receipt_date&per_page=50&is_individual=true'
getByEmployer = s.get(getByEmployerLink, headers={
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}, timeout=50)

if "contributor_street_2" not in getByEmployer.text:
    print("error, either no school or no donations")
    exit()

else:
    pass

with open(f'{EmpNoP} - {Ecycle}.json', 'wb') as outf:
    outf.write(getByEmployer.content)

demtotal = []
reptotal = []
EmpJson = getByEmployer.json()
pages = (EmpJson['pagination']['pages'])
currPage = 1

for xxloop in range(pages):
    if currPage == 1:
        for i in range(len(EmpJson['results'])):
            committeDonated = (EmpJson['results'][i]['committee']['name'])
            personName = (EmpJson['results'][i]['contributor_name'])
            dAmnt = (EmpJson['results'][i]['contribution_receipt_amount'])
            donatedAmnt = round(dAmnt, 2)
            dDate = (EmpJson['results'][i]['contribution_receipt_date'])
            donatedDate = dDate.split('T')[0]
            memoText = (EmpJson['results'][i]['memo_text'])
            toParty = partDict[committeDonated]
            if toParty == 'DEM':
                demtotal.append(donatedAmnt)
            if toParty == 'REP':
                reptotal.append(donatedAmnt)
            print(f"{donatedDate} - {toParty} - ${donatedAmnt}")
            with open(f'{EmpNoP} - Donations.txt', 'a') as outf2:
                outf2.writelines(f"{donatedDate} - {toParty} - ${donatedAmnt}")
        LIndex = (EmpJson['pagination']['last_indexes']['last_index'])
        LDate = (EmpJson['pagination']['last_indexes']['last_contribution_receipt_date'])
        currPage += 1
    else:
        MultiEmpLink = f'https://api.open.fec.gov/v1/schedules/schedule_a/?api_key={FEC_key}&sort_hide_null=false&sort_nulls_last=false&contributor_employer={EmP}&sort=-contribution_receipt_date&per_page=50&last_index={LIndex}&last_contribution_receipt_date={LDate}&is_individual=true'
        MultiEmp = s.get(MultiEmpLink, headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }, timeout=50)
        EmpJson2 = MultiEmp.json()
        for i in range(len(EmpJson2['results'])):
            committeDonated = (EmpJson2['results'][i]['committee']['name'])
            personName = (EmpJson2['results'][i]['contributor_name'])
            dAmnt = (EmpJson2['results'][i]['contribution_receipt_amount'])
            donatedAmnt = round(dAmnt, 2)
            dDate = (EmpJson2['results'][i]['contribution_receipt_date'])
            donatedDate = dDate.split('T')[0]
            memoText = (EmpJson2['results'][i]['memo_text'])
            toParty = partDict[committeDonated]
            if toParty == 'DEM':
                demtotal.append(donatedAmnt)
            if toParty == 'REP':
                reptotal.append(donatedAmnt)
            print(f"{donatedDate} - {toParty} - ${donatedAmnt}")
            with open(f'{EmpNoP} - Donations.txt', 'a') as outf3:
                outf3.writelines(f"{donatedDate} - {toParty} - ${donatedAmnt}")
        LIndex = (EmpJson2['pagination']['last_indexes']['last_index'])
        LDate = (EmpJson2['pagination']['last_indexes']['last_contribution_receipt_date'])
        currPage += 1