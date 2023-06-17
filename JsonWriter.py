import json
import os


def json_writing(local_path, file_name, data, log):
    try:
        counter = 1
        path = f'{local_path}/{file_name}'
        if os.path.isfile(path + '.json'):
            while os.path.isfile(path + f'_{counter}.json'):
                counter += 1
            path = path + f'_{counter}.json'
        else:
            path = path + '.json'
        with open(path, 'w') as f:
            json.dump(data, f)
    except Exception as ex:
        log.error(ex)