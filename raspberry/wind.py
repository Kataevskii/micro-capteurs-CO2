import requests

def get_wind(url='http://10.42.0.86/wind'):
    try:
        response = requests.get(url, timeout=10)
        return response.text

    except requests.RequestException as e:
        return e