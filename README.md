# Stock crawler

`Note: It's just for practicing, don't use it in any businese logic.`

## Installation


This is an installation example in MacOS, and python version is 3.6.8 .

Clone project
```sh
git clone https://github.com/tonyjhang/Stock-Crawler.git
```

Install tesseract

```sh
brew install tesseract
```
Download your driver for selenium, then overwrite file in web_driver folder.
[Ref](https://pypi.org/project/selenium/) (`See Drivers part`)

Install python depedency(remember to use virtualenv is better)
```sh
pip install requirements.txt
```

This tools also provide easy DB demo for testing, here is postgres example.
```sh
docker run --rm --name {container_name} -e POSTGRES_PASSWORD={your_password} -p 5432:5432 -d postgre
```
Initialize DB and table
```sh
python setup.py
```
Configure your settings
```sh
vi settings.py
```
## Run Demo
```sh
python main.py
```