import requests


class Yandex:
    def __init__(self, access_token):
        self.token = access_token
        self.headers = {'Accept': 'application/json',
                        'Authorization': self.token}

    def users_info(self):
        url = 'https://cloud-api.yandex.net/v1/disk'
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            return {'error': e}
        return response.json()

    def create_dir(self, path, dir_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': f'{path}/{dir_name}'}
        try:
            response = requests.put(url, headers=self.headers, params=params)
        except Exception as e:
            return {'error': e}
        return response.json()

    # just for example for use with upload_local_file, not used
    def get_url_to_upload_local_file(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': f'{path}'}
        try:
            response = requests.get(url, headers=self.headers, params=params)
        except Exception as e:
            return {'error': e}
        return response.json()

    # just for example, not used
    def upload_local_file(self, file):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        try:
            with open(file, 'rb') as f:
                response = requests.put(url, files={'file': f})
        except Exception as e:
            return {'error': e}
        return response.json()

    def upload_file_by_href(self, href, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': path, 'url': href}
        try:
            response = requests.post(
                url, headers=self.headers, params=params)
        except Exception as e:
            return {'error': e}
        return response.json()

    def get_operation_status(self, operation_id):
        url = 'https://cloud-api.yandex.net/v1/disk/operations/' + operation_id
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            return {'error': e}
        return response.json()
