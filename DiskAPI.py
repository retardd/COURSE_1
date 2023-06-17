import requests

URL = 'https://cloud-api.yandex.net/'

class YaUploader:
    def __init__(self, token):
        self.token = token

    def upload(self, file_path, remote_file_path, name, log):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
        temp_check = requests.get(f'{URL}v1/disk/resources?path={remote_file_path}',
                                   headers=headers).json()
        if temp_check.get('error') == 'DiskNotFoundError':
            res = requests.put(f'{URL}v1/disk/resources?path={remote_file_path}', headers=headers)
        with open(file_path, 'rb') as f:
            try:
                res = requests.get(f'{URL}v1/disk/resources/upload?path={remote_file_path}/{name}&overwrite=false',
                                   headers=headers).json()
                res = requests.put(res['href'], files={'file': f})
                log.info(f'Ответ API Диска - {res}')
            except KeyError:
                log.error(f'Ответ API Диска - {res}')