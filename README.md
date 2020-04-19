<!-- README.md --- 
;; 
;; Filename: README.md
;; Author: Louise <louise>
;; Created: Sat Apr 18 18:42:21 2020 (+0200)
;; Last-Updated: Sun Apr 19 02:48:45 2020 (+0200)
;;           By: Louise <louise>
 -->
# Readme

## Install

Configurating and running the program is done so: 

 - Create a virtual environment by running `virtualenv -p python3 env && . env/bin/activate`
 - Install the module by running `pip install -e grandma`

## Use

To use the program in development mode, it's easy, just run the program :

	GMAPS_API_KEY=<your_key_here> FLASK_APP=grandma FLASK_DEBUG=1 flask run
