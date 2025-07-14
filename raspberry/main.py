import store_data
from app import app

def main():
    store_data.init()
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    main()