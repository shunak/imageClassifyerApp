from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

# API KEYS info
key = "yourAPIkey"
secret = "yourAPIsecret"
wait_time = 1

# Save Folder
animalname = sys.argv[1]
savedir = "./" + animalname

flickr = FlickrAPI(key,secret,format='parsed-json') # get flicker data formed by json
result = flickr.photos.search(
    text = animalname,
    per_page=400,
    media = 'photos',
    sort = 'relevance', # search relation sort
    safe_search = 1,
    extras='url_q, licence'  # select params what you want to url_q
)

photos = result['photos']
# print return data
# pprint(photos)
# pprint(photos['photo'])



for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']  # set img url path
    filepath = savedir + '/' + photo['id'] + '.jpg' # set save file path to filepath 
    if os.path.exists(filepath): continue # skip same img
    urlretrieve(url_q,filepath) # get flicker image url 
    time.sleep(wait_time) # for prevent flicker server's pressure, set interval time










