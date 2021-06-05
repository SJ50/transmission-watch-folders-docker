#!/usr/bin/python

import time
import os, sys
import os.path as path
import transmissionrpc
import datetime

# Watch directories
watch_tv_hd = os.environ['RPC_WATCH_TV_HD_FOLDER']
watch_tv_uhd = os.environ['RPC_WATCH_TV_UHD_FOLDER']
watch_movie_hd = os.environ['RPC_WATCH_MOVIES_HD_FOLDER']
watch_movie_uhd = os.environ['RPC_WATCH_MOVIES_UHD_FOLDER']
watch_music = os.environ['RPC_WATCH_MUSIC_FOLDER']

# Complete download directories
download_dir_tv_hd = os.environ['RPC_DOWNLOAD_TV_HD_FOLDER']
download_dir_tv_uhd = os.environ['RPC_DOWNLOAD_TV_UHD_FOLDER']
download_dir_movie_hd = os.environ['RPC_DOWNLOAD_MOVIES_HD_FOLDER']
download_dir_movie_uhd = os.environ['RPC_DOWNLOAD_MOVIES_UHD_FOLDER']
download_dir_music = os.environ['RPC_DOWNLOAD_MUSIC_FOLDER']

client = transmissionrpc.Client(
    address=os.environ['RPC_CLIENT_HOST'],
    port=os.environ['RPC_CLIENT_PORT'],
    user=os.environ['RPC_CLIENT_USER'],
    password=os.environ['RPC_CLIENT_PASSWORD']
    )

# Logging
log = open('/var/log/python-rpc-folders.txt', 'a')
timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
print >> log, timestamp +  ' ' + 'Started watch script.'
print >> log, 'Current watch directories:'
print >> log, '     TV_HD: ' + watch_tv_hd
print >> log, '    TV_UHD: ' + watch_tv_uhd
print >> log, ' Movies_HD: ' + watch_movie_hd
print >> log, 'Movies_UHD: ' + watch_tv_uhd
print >> log, '     Music: ' + watch_music
print >> log, 'Current download directories:'
print >> log, '     TV_hd: ' + download_dir_tv_hd
print >> log, '    TV_uhd: ' + download_dir_tv_uhd
print >> log, ' Movies_hd: ' + download_dir_movie_hd
print >> log, 'Movies_uhd: ' + download_dir_movie_uhd
print >> log, '     Music: ' + download_dir_music
log.close()

def add(watch_dir, download_dir):
    directory = os.listdir(watch_dir)
    files = next(os.walk(watch_dir))[2]
    if files: # files exist in directory
        for file in files:
            if file.lower().endswith('.torrent') and not file.lower().startswith('.'):
                log = open('/var/log/python-rpc-folders.txt', 'a')
                timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())

                try:
                    print >> log, timestamp + ' ' + 'Adding torrent: ' + file
                    with open(watch_dir + '/' + file, "rb") as f:
                        encoded = base64.b64encode(f.read())
                    newTorrent = client.add_torrent(encoded, download_dir=download_dir)
                    time.sleep(1)
                    newTorrent.start()
                    os.remove(watch_dir + '/' + file)
                except Exception as e:
                      print >> log, timestamp + ' ' + 'Error encountered: ' + str(e)

                log.close()
                time.sleep(1)

while True:
    log = open('/var/log/python-rpc-folders.txt', 'a')
    timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
    print >> log, timestamp + ' ' + 'Searching directories.'
    add(watch_tv_hd, download_dir_tv_hd)
    add(watch_tv_uhd, download_dir_tv_uhd)
    add(watch_movie_hd, download_dir_movie_hd)
    add(watch_movie_uhd, download_dir_movie_uhd)
    add(watch_music, download_dir_music)
    log.close()
    time.sleep(30)
