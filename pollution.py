import smtplib
from email.mime.text import MIMEText

import bs4
import requests
import os

# Pobranie strony ARMAAG
import sys

print(sys.argv)
try:
    data = sys.argv[1]
    r = requests.get('http://armaag.gda.pl/komunikat.htm?data=' + data)
    html = r.text
except IndexError:
    data = None
    print('Nie ma daty, biore biezaca date')
    r = requests.get('http://armaag.gda.pl/komunikat.htm')
    html = r.text
print(data)


# Sparsowanie strony i wyszukanie tabeli z jakoscia powietrza

soup = bs4.BeautifulSoup(html, 'html.parser')
tabela = soup.find('table', class_='jakoscpowietrza')

# Sprawdzenie, czy w tabeli znajduja sie informacje o poziomie zoltym lub czerwonym
#print(tabela)
# print(str(tabela))

cities = []

for row in tabela.find_all('tr')[0].find_all('th'):
    if row.a is not None:
        cities.append(row.a.contents)

pollutions = []

text = "<table>"

for row in tabela.find_all('th'):
    if row.attrs.get('title') is not None:
        pollutions.append(row.attrs.get('title'))

for i in range(1,len(cities)+1):
    row = tabela.find_all('tr')[i].find_all('td')
    text += "<tr>"
    for j in range(1,len(pollutions)+1):
        cell = row[j-1].img.attrs.get('src')
        if 'czerwony' in cell:
            text += "<td>" + str(cities[i-1][0]) + " " + str(pollutions[j-1]) + ' ' \
                    '<span style="background-color: #FF0000">czerwony</span> poziom zanieczyszczenia</td>'
        elif 'zolty' in cell:
            text += "<td>" + str(cities[i - 1][0]) + " " + str(pollutions[j - 1]) + ' ' \
                    '<span style="background-color: #FFFF00">zolty poziom zanieczyszczenia</td>'
        elif 'zielony' in cell:
            text += "<td>" + str(cities[i - 1][0]) + " " + str(pollutions[j - 1]) + ' ' \
                    '<span style="background-color: #00FF00">zielony</span> poziom zanieczyszczenia</td>'
    text += "</tr>"

text += "</table>"

print(text)

message = MIMEText(text, 'html')
message['From'] = 'Automato <projekt_smog@wp.pl>'
message['To'] = 'klaudia.kosiek@gmail.com'
message['Subject'] = 'Ostrzeżenie'

smtp = smtplib.SMTP_SSL('smtp.wp.pl', 465)
smtp.ehlo()
smtp.login('projekt_smog', os.environ.get('POLLUTION_PASS'))
smtp.sendmail(message['From'], message['To'], message.as_string())
smtp.quit()
