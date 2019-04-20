# coding: utf-8
import argparse
import livechanapi
import config
import requests
import websocket
import threading
import time
import json

tripmap = {}
for l in requests.get('https://kotchan.org/js/tripflags.js').text.splitlines():
    if l.startswith('flags_image_table'):
        tripmap[l.split('"')[1]] = l.split('"')[3].split('.')[0]

api = livechanapi.LiveChanApi(config.url, 'int', config.password_livechan)
ownposts = list()

def process_chat(api, data):
    print data
    if data['country']+data['body']+data.get('image_filename', '') in ownposts:
        return
    newdata = data
    files = {}
    if 'image' in data:
        file = data['image'].split('/')[-1]
        exp = file.split('.')[-1]
        localfile = 'tmp/file.%s' % exp
        with open(localfile, 'wb') as f:
            f.write(requests.get('https://kotchan.org/tmp/uploads/%s' % file).content)
        files = {'file': (data['image_filename'], open(localfile))}
    if 'trip' in data:
        newdata['icon'] = tripmap.get(data['trip'])
    ownposts.append(data['country']+data['body']+data.get('image_filename', ''))
    res = requests.post('%s/post' % config.kotch_url, data=newdata, files=files)
    print res.text

def watch_livechan():
    api.on_chat(process_chat)
    api.wait()

def on_message(ws, message):
    file = ''
    data = json.loads(message)
    if data['type'] == 'message':
        data = data['data']
        data['country'] = data['location']['country']
        if data['location'].get('region'):
            data['country'] += '-'+data['location']['region']
        data['country_name'] = data['location']['country_name']
        if data['file']:
            file = data['file']['file']
            with open('tmp/'+file, 'wb') as f:
                f.write(requests.get('%s/static/uploads/%s' % (config.kotch_url, file)).content)

        if data['country']+data['body']+file in ownposts:
            return
        ownposts.append(data['country']+data['body']+file)
        api.post(data['body'], data['name'], file='tmp/'+file, country=data['country'])



def watch_kotch():
    ws = websocket.WebSocketApp("ws://%s/ws?no_history=1"%config.kotch_url.split('/')[-1], on_message = on_message)
    ws.run_forever()


def main():
    t = threading.Thread(target=watch_livechan, args=())
    t.daemon = True
    t.start()
    t2 = threading.Thread(target=watch_kotch, args=())
    t2.daemon = True
    t2.start()
    import time
    while True:
        time.sleep(1)



if __name__ == '__main__':
    main()
