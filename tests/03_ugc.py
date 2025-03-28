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
print('Uploading a ugc')


resp = requests.post(f'{root_url}/ugc', headers=headers, json={
    'type': 'default',
    'text': 'Hello, World!',
    'extras': {}
})
assert (resp.status_code == 200), resp.text
ugc_id = resp.json()['id']

# download ugc
print('Downloading a ugc')
resp = requests.get(f'{root_url}/ugc/{ugc_id}', headers=headers)
assert (resp.status_code == 200), resp.text

print(resp.json())
assert (resp.json()['text'] == 'Hello, World!')

# update ugc
print('Updating a ugc')
resp = requests.put(f'{root_url}/ugc/{ugc_id}', headers=headers, json={
    'type': 'default',
    'text': 'Hello, World! Updated',
    'extras': {}
})
assert (resp.status_code == 200), resp.text

# list ugc
resp = requests.get(f'{root_url}/ugc', headers=headers)
assert (resp.status_code == 200), resp.text

print(resp.json())
items = resp.json()['items']
assert len(items) == 1
assert items[0]['text'] == 'Hello, World! Updated'

# delete ugc
print('Deleting a ugc')
ugc_id = items[0]['id']
resp = requests.delete(f'{root_url}/ugc/{ugc_id}', headers=headers)
assert (resp.status_code == 200), resp.text

resp = requests.delete(f'{root_url}/ugc/3333', headers=headers)
assert (resp.status_code == 404)
