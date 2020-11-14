# FilmFinder
# Requirement
* Python 3.6+
* Git LFS



## Create virtual environment
Type in the command prompt
``` bash
$ python3 -m venv ./venv
```
To activate environment, type in command prompt
``` bash
$ source ./venv/bin/activate
```



## Installation
Type in the command prompt
``` bash
$ cd server
```

``` bash
$ pip3 install -r requirements.txt
```

``` bash
$ python3 -m nltk.downloader stopwords
```

``` bash
$ python3 -m nltk.downloader punkt
```


``` bash
$ python3 db_init.py
```
## Run
``` bash
$ python3 server.py
```
