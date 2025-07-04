import time
import store_data
from app import app

def main():
    store_data.init()

if __name__ == "__main__":
    main()
    app.run(debug=True, host='0.0.0.0')