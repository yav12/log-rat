import requests
from time import sleep as wait
from os import path
from tokens import pastetoken

token = pastetoken
def upload(author):
    while path.isfile("log.txt") == False:
        wait(.5)
    with open('log.txt') as f: s = f.read()
    title = f'{author}\'s log'
    payload = {'sections':[{'name':title, 'syntax':'autodetect','contents':s}]}
    headers = {'X-Auth-Token': token}
    post_response = requests.post(url='https://api.paste.ee/v1/pastes', json=payload, headers=headers)
    with open('pastelog.txt', "a") as f: f.write(str(author) + ": " + post_response.text + '\n')
    return post_response.text
