#!/bin/env python
#-*- coding: utf-8 -*-
import argparse
import datetime
import json
import os
import requests
import sys
import configparser

CONFIG_PATH = '/etc/cloud_reporter.conf'


def generatePassword(length=20):
  import random
  import string
  random.seed(os.urandom(4096))
  chars = string.ascii_letters + string.digits + '"«»()@+-/*=%`°≠×÷−±@)[><—$,;.:…’'
  return ''.join(random.choice(chars) for i in range(length))

def getConfigParser():
  parser = configparser.ConfigParser()
  parser.read(CONFIG_PATH)
  return parser

def getCredential():
  section_name = 'credential'
  parser = getConfigParser()
  return {
    'username': parser.get(section_name, 'username'),
    'password': parser.get(section_name, 'password'),
  }

def subscribe():
  import socket
  data = {
    'username': socket.gethostname(),
    'password': generatePassword(),
  }
  response = requests.post('%s/createAccount/' % parser.get('server', 'base_url') , data=data)
  if response.status_code == requests.codes.ok:
    feed_id = json.loads(response.text)['feed_id']
    parser = getConfigParser()
    parser.add_section('feed')
    parser.set('feed', 'id', feed_id)
    parser.set('feed', 'username', data['username'])
    parser.set('feed', 'password', data['password'])
    with open(CONFIG_PATH, 'w') as config_file:
      parser.write(config_file)
  else:
    sys.exit('Bad status returned by PubSub server')

def __getActionReport():
  from collections import deque
  content_list = deque()

  with open('/var/log/ansible', 'r') as log:
    log_line_list = log.readlines()
    log_line_list.reverse()
    for line in log_line_list:
      content_list.appendleft(line)
      if line.startswith('HEAD is now at'):
        break

  content_list.appendleft('\n\n-------\n\n')

  with open('/var/log/aptitude', 'r') as log:
    log_line_list = log.readlines()
    log_line_list.reverse()
    for line in log_line_list:
      content_list.appendleft(line)
      if line.startswith('Aptitude') and line.endswith(': log report\n'):
        break

  return '<pre>%s</pre>' % (''.join(content_list),)

def post():
  parser = getConfigParser()
  data = {
    'username': parser.get('feed', 'username'),
    'password': parser.get('feed', 'password'),
    'link': 'http://exemple.com',
    'description': __getActionReport(),
    'pubDate': datetime.datetime.now().isoformat(),
  }
  data['title'] = 'Status Report for %s, %s' % (parser.get('feed', 'username'), data['pubDate'][:10])
  response = requests.post(
    '%s/%s/postItem/' % (parser.get('server', 'base_url'), parser.get('feed', 'id')),
    data=data
  )
  print(response.status_code)


def createBaseConfig(**kw):
  parser = ConfigParser.ConfigParser()
  parser.add_section('server')
  parser.set('server', 'base_url', 'https://me.wavrant.xyz/feed')
  with open(CONFIG_PATH, 'w') as config_file:
      parser.write(config_file)

def parseArguments():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def main():
  if not os.path.exists(CONFIG_PATH):
    createBaseConfig()

  command_list = {
    'subscribe': subscribe,
    'post': post,
  }

  command_list[sys.argv[1]]()

if __name__ == '__main__':
  main()
