import pickle
import os


def persist_dict(mapping, filename):
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, 'wb') as file:
        for key, value in mapping.items():
            json_str = pickle.dumps([key, value])
            file.write(json_str)


def persist_object(object, filename):
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename, 'wb') as file:
        pickle.dump(object, file)


def parse_object(filename):
    print(filename)
    with open(filename, 'rb') as file:
        obj = pickle.load(file)

    return obj
