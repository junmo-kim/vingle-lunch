# Vingle Lunch

## Requirement
  * Python 3
  * virtualenv
  * pip
  * npm
  * nodejs
  * bower
  * ruby
  * sass

## Getting Started
1. Clone sources
  ```
  $ git clone https://github.com/lupinogle/vingle-lunch.git
  ```
  
2. Setting Python 3 virtual environment
  ```
  $ cd vingle-lunch
  $ virtualenv env -p /usr/bin/python3	# python 3 path
  ```
  
3. Activate virtual environment
  ```
  $ source env/bin/activate
  or
  $ . env/bin/activate
  ```
  ```
  $ (env)
  ```
  
4. Install python packages.
  ```
  $ (env) pip install -r requirements.txt
  ```
  
5. Install bower
  ```
  $ npm install -g bower
  ```
  
6. Install bower packages
  ```
  $ bower install
  ```
  
7. Install sass
  ```
  $ sudo gem install sass
  ```
  
8. Create db
  ```
  $ (env) python db_create.py
  $ (env) python add_legacy.py	# optional
  ```
  
9. Run development server
  ```
  $ (env) python run.py
  ```
  http://localhost:5000
