import json

import requests

headers = {}

with open('tests/player.json', 'r') as f:
    player_json = json.load(f)
    headers['x-player-id'] = str(player_json['id'])
    headers['x-player-passwd'] = player_json['passwd']
    headers['x-project-id'] = '1'
    headers['x-project-version'] = '0'

root_url = 'http://localhost:6282/api'

# upload save
print('Uploading a save')

for key in ['a', 'b', 'c']:
    resp = requests.post(f'{root_url}/save', headers=headers, json={
        'key': key,
        'text': 'Hello, World!',
        'extras': {}
    })
    assert (resp.status_code == 200), resp.text

# list save
print('Listing saves')
resp = requests.get(f'{root_url}/save', headers=headers)
assert (resp.status_code == 200), resp.text

print(resp.json())

# download save
print('Downloading a save')

resp = requests.get(f'{root_url}/save/a', headers=headers)
assert (resp.status_code == 200), resp.text
print(resp.json())

assert (resp.json()['text'] == 'Hello, World!')
