'''
Created on 2012-8-8

@author: diracfang
'''
import socket

hostname = socket.gethostname()

if hostname in ('diracfang-VAIO', 'ubuntu'):
    ENV_TAG = 'home'
elif hostname in ('diracfang', 'liubida-desktop'):
    ENV_TAG = 'local'
elif hostname in ('tc_69_54',):
    ENV_TAG = 'dev'
elif hostname in ('tc_69_53', 'tc_6_173', 'tc_6_175'):
    ENV_TAG = 'test'
else:
    ENV_TAG = 'prod'