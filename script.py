import json, requests, oauth_hook, sys, utils

print 'Welcome to engager, helping you be a better person'

ids = []
profiles = []
errors = []

'''
Go to https://dev.twitter.com/apps to create a Twitter app,
change the access level to read and write,
create your access token and fill in the following details
'''
consumer_key="XnGHbvMMaDChwjniOeAag"
consumer_secret="4ZbyH7sIBJGGJGSgg7dBnwvETtMXHjRv1dCvAyuQ"
access_token="9436992-9tcWsAUNucjU2GgXo3ZhTMAD3Jh0WzahteMKZp3uo"
access_token_secret="YE8UsZFv7ouSiXoVXGm2BFu4DBmR9TuLTrPSKSjdnl8"

'''false hides native retweets from friends, true shows native retweets from friends'''
want_retweets='false'



if not consumer_key or not consumer_secret or not access_token or not access_token_secret:
    print 'Get Twitter app keys from https://dev.twitter.com/apps and add to script.py'
    sys.exit()

oauth = oauth_hook.OAuthHook(access_token, access_token_secret, consumer_key, consumer_secret, header_auth=True)

# response = requests.get('https://api.twitter.com/1.1/friends/ids.json', params={'status':status}, hooks={'pre_request':oauth})

'''Get a list of ids for the 5000 most recent friends'''
request = requests.get('https://api.twitter.com/1.1/friends/ids.json', params={'stringify_ids': 'true'}, hooks={'pre_request': oauth})

if not request.status_code == 200:
    print 'Error from Twitter getting friends ids'
    print request.text
    sys.exit()

ids = json.loads(request.content)['ids']
print 'Found', len(ids), 'friend ids'

# Disabled as the full profiles don't surface the want_retweets preference
# print 'Getting full profiles'
# for chunk in utils.chunks(ids, 100):
#     print 'Getting', len(profiles), 'to', len(profiles) + len(chunk), 'of', len(ids), 'profiles'
#     request = requests.get('https://api.twitter.com/1.1/friendships/lookup.json?user_id=' + ','.join(chunk), hooks={'pre_request': oauth})
#     if not request.status_code == 200:
#         request = requests.get('https://api.twitter.com/1.1/friendships/lookup.json?user_id=' + ','.join(chunk), hooks={'pre_request': oauth})
#     if not request.status_code == 200:
#         print 'Failed to get profiles', len(profiles), 'to', len(profiles) + len(chunk), 'of', len(ids)
#         sys.exit()
#     profiles = profiles + json.loads(request.content)
# print 'Completed getting', len(profiles), 'of', len(ids), 'profiles'

for id in ids:
    print 'Updating want_retweets to', want_retweets, 'for', id
    request = requests.post('https://api.twitter.com/1.1/friendships/update.json', params={'user_id': id, 'retweets': want_retweets}, hooks={'pre_request': oauth})
    if not request.status_code == 200:
        request = requests.post('https://api.twitter.com/1.1/friendships/update.json', params={'user_id': id, 'retweets': want_retweets}, hooks={'pre_request': oauth})
    if not request.status_code == 200:
        print 'Failed to update want_retweets for', id
        errors.append('Failed to update want_retweets for ' + id)
    
for error in errors:
    print error

print 'Completed updating profiles and printed', len(errors), 'errors'