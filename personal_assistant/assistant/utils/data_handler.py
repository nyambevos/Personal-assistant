import pickle


def save_data_to_file(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    print(f'Data saved to {filename} successfully.')


def load_data_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        print(f'Data loaded from {filename} successfully.')
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f'File {filename} not found.') from e
