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

# upload image
print('Uploading an image')

from PIL import Image
from io import BytesIO

sample_jpg_image = Image.new('RGB', (500, 100))
data = BytesIO()
sample_jpg_image.save(data, 'JPEG')

resp = requests.post(f'{root_url}/image?max_width=100', headers=headers, data=data.getvalue())
assert (resp.status_code == 200), resp.text
image_token = resp.json()['token']

# download image
print('Downloading an image')
resp = requests.get(f'{root_url}/image/{image_token}', headers=headers)
assert resp.status_code == 200

new_image = Image.open(BytesIO(resp.content))
assert new_image.size == (100, 20)