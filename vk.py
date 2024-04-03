import requests


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        try:
            response = requests.get(url, params={**self.params, **params})
        except Exception as e:
            return {'error': e}
        return response.json()

    def photos_get(self, owner_id, extended=1, photo_sizes=1,
                   album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id,
                  'extended': extended, 'photo_sizes': photo_sizes,
                  'album_id': album_id}
        try:
            response = requests.get(url, params={**self.params, **params})
        except Exception as e:
            return {'error': e}
        return response.json()
