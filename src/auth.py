'''
Created on 2012-8-9

@author: diracfang
'''

class User(object):
    
    def __init__(self, db, access_token):
        self.db = db
        access_token = '19a77650b9b829caa401ed219726410277928eac'
        self.access_token = access_token
    
    def get_user(self):
        if not hasattr(self, '_user'):
            qs = "select * from account_access where access_token = '%s'" % self.access_token
            result = self.db.get(qs)
            if result:
                self._user = result
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