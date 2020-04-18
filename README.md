<!-- README.md --- 
;; 
;; Filename: README.md
;; Author: Louise <louise>
;; Created: Sat Apr 18 18:42:21 2020 (+0200)
;; Last-Updated: Sat Apr 18 20:56:30 2020 (+0200)
;;           By: Louise <louise>
 -->
# Readme

## Install

Configurating and running the program is done so: 

 - Create a virtual environment by running `virtualenv -p python3 env && . env/bin/activate`
 - Install the dependencies by running `pip install -r requirements.txt`

## Use

To use the program in development mode, it's easy, just run the program :

	FLASK_APP=grandma FLASK_DEBUG=true flask run
