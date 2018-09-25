import yaml
from lookerapi import LookerApi
from datetime import datetime
from pprint import pprint


look_to_get = 3
host = 'universityofcalgary'

f = open('config.yml')
params = yaml.load(f)
f.close()

my_host = params['hosts'][host]['host']
my_secret = params['hosts'][host]['secret']
my_token = params['hosts'][host]['token']

looker = LookerApi(host=my_host,
                 token=my_token,
                 secret = my_secret)


data = looker.get_look(look_to_get)

pprint(data)