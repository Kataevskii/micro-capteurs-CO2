import requests

def save_image(url='http://your-api-address/photo', filename='image.jpg'):
    try:
        response = requests.get(url, timeout=10)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename

    except requests.RequestException as e:
        return e