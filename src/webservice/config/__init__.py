#coding:utf-8
import json

config = None
ENV = None

def set_config(evn):
    global config
    global EVN
    EVN = evn
    if EVN == 'development':
        config = json.load(file('config/development.json'))
    elif EVN == 'testing':
        config = json.load(file('config/testing.json'))
    elif EVN == 'production':
        config = json.load(file('config/production.json'))
    else:
        raise NameError

def get_config():
    global config
    if config is None:
        raise AttributeError
    return config
