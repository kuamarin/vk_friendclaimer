import vk_api
import os
import time
import random
import json

'''
### Config ###
Param "token" - put your VK Auth token to make this thing work
Param "mode" - put here "new" for accepting only new friend requests or whatever you want to make it add any of your subscribers
Param "idling_delay" - how much time we need to wait after checking and accepting friend requests
Param "random_range" - controls delay between friend claims with random range [a to b]
'''
def _config():
    with open(os.getcwd() + '/config.json', "r") as f:
        j = json.loads(f.read())
        return j

class vk:
    _vk_session = None
    _vk = None
    def auth():
        vk._vk_session = vk_api.VkApi(token=_config()["token"])
        vk._vk = vk._vk_session.get_api()
vk.auth()

while True:
    print("Getting friend requests...")
    if _config()["mode"] == "new":
        friendlist = vk._vk.friends.getRequests(out=0, need_viewed=0)["items"]
    else:
        friendlist = vk._vk.friends.getRequests(out=0, need_viewed=1)["items"]
    if len(friendlist)>0:
        for friend in friendlist:
            response = vk._vk.friends.add(user_id=friend)
            if response == 2:
                print(f"Added user id{friend} successfully!")
            else:
                print(f"Response code: {response}")
            time.sleep(random.uniform(*_config()['random_range']))
    else:
        print(f"No friend requests found.")
    print(f"Sleeping {_config()['idling_delay']} seconds")
    time.sleep(_config()['idling_delay'])