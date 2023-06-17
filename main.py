import requests
from DiskAPI import YaUploader
from JsonWriter import json_writing
from Logger import MainLogger
from config import vk_token, yadisk_token


def main_process(list_id, vk_token, log, max_pictures=5):
    try:
        uploader = YaUploader(yadisk_token)
        json_result_file = {}
        log.info('Начинаю обработку id')
        for id in list_id:
            json_result_file[str(id)] = []
            vk_url = 'https://api.vk.com/method/photos.get'
            params = {'access_token': vk_token, 'owner_id': id, 'album_id': 'profile', 'rev': 1, 'extended': 1, 'count': max_pictures, 'v': '5.131'}
            resp = requests.get(vk_url, params=params)
            resp_data = resp.json()['response']['items']
            temp_data = []
            log.info(f'Получено {max_pictures} фотографий профиля {id}')
            log.info('Начинаю обработку фотографий')
            count = 1
            for picture in resp_data:
                hd_pic = sorted(picture['sizes'], key=lambda d: d['width'], reverse=True)
                pic_url = hd_pic[0]['url']
                pic_type = hd_pic[0]['type']
                name = str(picture['likes']['count'])
                log.info(f'На фотографии №{count} {name} лайков')
                if name in temp_data:
                    name = name + '_' + str(temp_data.count(name) + 1)
                    log.info(f'Для фотографии №{count} создано новое имя')
                temp_data.append(name)
                with open(f'temp/{name}.jpg', 'wb') as f:
                    resp = requests.get(pic_url)
                    f.write(resp.content)
                    log.info(f'Фотография №{count} сохранена по пути temp/{name}.jpg')
                uploader.upload(f'temp/{name}.jpg', f'netology/{id}', name, log)
                json_result_file[str(id)].append({'file_name': f'{name}.jpg', 'size': pic_type})
                log.info(f'Фотография №{count} сохранена на Диск')
                count += 1
        json_writing('jsons', 'results', json_result_file, log)
        log.info('JSON-файл с данными о файлах сохранен')
    except Exception as ex:
        log.error(ex)


if __name__ == '__main__':
    log = MainLogger()
    log.info('Запуск программы')
    main_process([1], vk_token, log, 4)

