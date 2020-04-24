<!-- README.md --- 
;; 
;; Filename: README.md
;; Author: Louise <louise>
;; Created: Sat Apr 18 18:42:21 2020 (+0200)
;; Last-Updated: Fri Apr 24 15:19:19 2020 (+0200)
;;           By: Louise <louise>
 -->
# Readme

## Install
Installing the package is done thusly: 

 - Create a virtual environment by running `virtualenv -p python3 env && . env/bin/activate`
 - Install the package by running `pip install .`

## Use in debug mode
To use the program in development mode, it's easy, just run the program (note that you
have to export the API_KEY for the program to work) :

```bash
export GMAPS_API_KEY=<your_key_here>
FLASK_APP=grandma FLASK_ENV=development flask run
```

## Use with heroku
To use with heroku, you can just push it to Heroku. If you want to run it in local, you
have to install everything in the requirements.txt, then run Heroku.

```bash
pip install -r requirements.txt
heroku local web
```

## Testing
To run the tests, you have to install `pytest`.

```bash
pip install pytest
pytest
```

You can also test test coverage by running:

```bash
pip install coverage 
coverage --source=grandma -m pytest # The actual testing
coverage report # Getting the results
```
