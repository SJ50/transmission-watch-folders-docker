#!/usr/bin/python

import time
import os, sys, linecache
import os.path as path
import transmissionrpc
import datetime
import base64

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
print(timestamp +  ' ' + 'Started watch script.', file=log)
print('Current watch directories:', file=log)
print('     TV_HD: ' + watch_tv_hd, file=log)
print('    TV_UHD: ' + watch_tv_uhd, file=log)
print(' Movies_HD: ' + watch_movie_hd, file=log)
print('Movies_UHD: ' + watch_movie_uhd, file=log)
print('     Music: ' + watch_music, file=log)
print('Current download directories:', file=log)
print('     TV_HD: ' + download_dir_tv_hd, file=log)
print('    TV_UHD: ' + download_dir_tv_uhd, file=log)
print(' Movies_HD: ' + download_dir_movie_hd, file=log)
print('Movies_UHD: ' + download_dir_movie_uhd, file=log)
print('     Music: ' + download_dir_music, file=log)
log.close()


#Print the exception handling with the line number 
def PrintException(logfile):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj),file=logfile)


def add(watch_dir, download_dir):
    for entry in os.scandir(watch_dir):
        if entry.name.lower().endswith('.torrent') and entry.is_file():
            log = open('/var/log/python-rpc-folders.txt', 'a')
            timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
            try:
                print(timestamp + ' ' + 'Adding torrent: ' + entry.name, file=log)
                with open(watch_dir + '/' + entry.name, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode('utf-8')
                newTorrent = client.add_torrent(encoded, download_dir=download_dir)
                time.sleep(1)
                newTorrent.start()
                os.remove(watch_dir + '/' + entry.name)
            except Exception as e:
                print(timestamp + ' ' + 'Error encountered for directory ('+ watch_dir + ') : ' + str(e), file=log)
                PrintException(log)
            log.close()
            time.sleep(1)
        else: 
            log = open('/var/log/python-rpc-folders.txt', 'a')
            timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
            print(timestamp + ' ' + 'No torrent file found for directory ('+ watch_dir + ') : ' + entry.name, file=log)
            

while True:
    log = open('/var/log/python-rpc-folders.txt', 'a')
    timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
    print(timestamp + ' ' + 'Searching directories.', file=log)
    add(watch_tv_hd, download_dir_tv_hd)
    add(watch_tv_uhd, download_dir_tv_uhd)
    add(watch_movie_hd, download_dir_movie_hd)
    add(watch_movie_uhd, download_dir_movie_uhd)
    add(watch_music, download_dir_music)
    log.close()
    time.sleep(30)
