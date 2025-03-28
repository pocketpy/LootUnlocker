import requests

root_url = 'http://localhost:6282/api'

print('Creating a new project')
resp = requests.post(f'{root_url}/project', json={
    "name": "brogue-rpg",
    "description": "A Ticket to the Past of RPG2 World",
    "extras": {}
    })
assert (resp.status_code == 200), resp.text

project_id = resp.json()['id']
print(f'Project ID: {project_id}')

print('Creating a new player')
resp = requests.post(f'{root_url}/player', json={
    "project_id": project_id,
    "channel": "unknown",
    "project_version": 0,
    "extras": {}
    })

assert (resp.status_code == 200), resp.text
player_id = resp.json()['id']
player_passwd = resp.json()['passwd']

print(f'Player ID: {player_id}')
print(f'Player Password: {player_passwd}')

# save player info to player.json
import json

with open('tests/player.json', 'w') as f:
    json.dump({
        'id': player_id,
        'passwd': player_passwd,
    }, f)
