Hello, welcome to my API deployment attempt in order to fulfill Binar's Gold Level Challenge.
Instructions
    main script to run: app.py

        1. "Hello World" Basic API, to show how basic flask API work
        2. "Text Processing" API, to process inputted text in provided field in the API
        3. "File Processing" API, to process inputted CSV file* in provided field in the API (it will takes time based on how much data in the CSV)
            you can access processed file in "http://127.0.0.1:5000/output", the output will also be in .json format
        4. "File Output", to show the output while still on the page of API.

What does "Text Processing" and "File Processing" do?
    the API will process the inputted text/file so that there are no more unnecessary character in the text so the text will look more tidier, 
    moreover, the API also will also replace non-formal word to formal (in Bahasa) word that already provided in "new_kamusalay.csv". It also removes stem and stopwords (Indonesian stopwords)

Processed data will be inputted to our "api_database" database for documentation porpuse


*Data should be in the first column of the CSV