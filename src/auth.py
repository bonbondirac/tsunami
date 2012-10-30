'''
Created on 2012-8-9

@author: diracfang
'''

import cPickle
import settings
import constants
import time
import logging

logger = logging.getLogger(__name__)


class User(object):
    
    def __init__(self, db, redis_ins, access_token):
        self.db = db
        self.redis_ins = redis_ins
        self.access_token = access_token
    
    def get_user(self):
        if not hasattr(self, '_user'):
            if self.access_token:
                key = constants.KEY_ACCESS_TOKEN_CACHE % (settings.ENV_TAG, self.access_token)
                result = self.redis_ins.get(key)
                if result is not None:
                    row = cPickle.loads(result)
                else:
                    row = None
                if row is None:
                    qs = "select * from account_access where access_token = %s"
                    try:
                        row = self.db.get(qs, self.access_token)
                    except Exception, exc:
                        logger.warning('idle time: %s' % (time.time() - self.db._last_use_time))
                        raise exc
                    if row:
                        self.redis_ins.set(key, cPickle.dumps(row))
                        self.redis_ins.expire(key, constants.ACCESS_TOKEN_CACHE_TIMEOUT)
                self._user = row
            else:
                self._user = None
        
        return self._user
    
    def get_user_id(self):
        user = self.get_user()
        if user:
            user_id = user.user_id
        else:
            user_id = None
        
        return user_id
