import requests
from time import sleep as wait
from os import path

def upload(author):
    while path.isfile("log.txt") == False:
        wait(.5)
    with open('log.txt') as f: s = f.read()
    title = f'{author}\'s log'
    payload = {'sections':[{'name':title, 'syntax':'autodetect','contents':s}]}
    headers = {'X-Auth-Token': 'avW54hSqZ6sKJV6WQwaOMot70JUoEgvQdkoduj7LB'}
    post_response = requests.post(url='https://api.paste.ee/v1/pastes', json=payload, headers=headers)
    with open('pastelog.txt', "a") as f: f.write(author + ": " + post_response.text)
    return post_response.text