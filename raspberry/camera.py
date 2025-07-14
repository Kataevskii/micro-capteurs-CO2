import requests

default_url = "http://10.42.0.85/photo"

def save_image(url=default_url, filename='image.jpg'):
    try:
        response = requests.get(url, timeout=10)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename

    except requests.RequestException as e:
        print(e)
        return None