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

# upload log
print('Uploading log')
resp = requests.post(f'{root_url}/log', headers=headers, json={
    'text': '[INFO] Hello, World!',
    'extras': {}
})

assert (resp.status_code == 200), resp.text

# upload log batch
print('Uploading log batch')

logs = []
for i in range(10):
    logs.append({
        'text': f'[INFO] Hello, World! {i}',
        'extras': {'index': i}
    })
resp = requests.post(f'{root_url}/log/batch', headers=headers, json={
    'items': logs
})

assert (resp.status_code == 200), resp.text
