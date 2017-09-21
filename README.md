Demo Platform

Features:

- API to display (filter) items from db
- Upload and decode barcodes
- auto-logging

Installing deps (Ubuntu tested):

- sudo apt-get install libzbar-dev

- sudo apt-get install mongodb

- pip install pipenv

- add ~/.local/bin to PATH

Deploy server:

- pipenv install

- pipenv run python gogo.py

Usage:

    - http://localhost:5000

    - Feed Data (feeding some data to db)

    - http://localhost:5000/items/{name}/{value} - filter items by name and value

            eg. http://localhost:5000/items/error/-45
    
    - CRUD operations (Content-Type: application/json)

            eg. POST http://localhost:5000/items/ {"name": 500, "error": -1000, "order": 10, "status": 0, "processed": 9}

            eg. PUT http://localhost:5000/items/ {"name":500,"error":200}

            eg. DELETE http://localhost:5000/items/name/500

    - Upload a barcode (some ex in assets/uploads folder) will decode into a string

    - All operations are logged

    - Plot Error/Order