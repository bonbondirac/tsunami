'''
Created on 2012-8-1

@author: diracfang
'''

import requests


def main():
    r = requests.get('http://localhost:8888')
    
    print 'request successfully sent, waiting for response...'
    
    for line in r.iter_lines(chunk_size=10):
        print line


if __name__ == '__main__':
    main()