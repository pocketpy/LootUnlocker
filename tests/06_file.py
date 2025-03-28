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

file = b'Hello, World!'

# upload file
print('Uploading a file')

resp = requests.post(f'{root_url}/file', headers=headers, files={
    'file': ('test.txt', file)
})
assert (resp.status_code == 200), resp.text
file_token = resp.json()['token']

# download file
print('Downloading a file')
resp = requests.get(f'{root_url}/file/{file_token}', headers=headers)
assert resp.status_code == 200

print(resp.content, file)
assert resp.content == file