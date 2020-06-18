# Transmission Watch Folders

A docker and Python3 version of 

[taylorthurlow/transmission-multiple-watch-folders]: https://github.com/taylorthurlow/transmission-multiple-watch-folders	"taylorthurlow/transmission-multiple-watch-folders"

The goal is to add as "addon" in a torrent download docker stack. 
My personnal plan is to use it together with some sync folder on my OneDrive or other sync service (but that would be used with another container)

## What is Transmission-multiple-watch-folders

A small Python script which provides a way to automate multiple watch directories when using `TransmissionRPC`, an API version of the popular Transmission torrent client. This should work remotly as the torrent is send as base64 encoded file throught the API. 

The script runs in the background and searches the specified watch directories for torrent files, every 1 minute by default.

### Getting Started

#### Prerequisites
* `Docker`
* `Transmission`

## Usage

Here are some example snippets to help you get started creating a container.

### Docker

```
docker run \
  --name=Transmission-folders \
  -e RPC_DOWNLOAD_TV_FOLDER=/downloads/TV \
  -e RPC_DOWNLOAD_MOVIES_FOLDER=/downloads/MOVIES \
  -e RPC_DOWNLOAD_MUSIC_FOLDER=/downloads/MUSIC \
  -e RPC_CLIENT_USER=user \
  -e RPC_CLIENT_PASSWORD=PASSWORD \
  -v path to torrents folder:/torrents \
  --restart unless-stopped \
  soflane/transmission-watch-folders
```

#### Docker

```
version: "3"
services:
  Transmission-folders:
    image: mysql:5
    container_name: Transmission-folders
    restart: unless-stopped
    volumes:
      - path to torrents folder:/torrents
    environment:
      - RPC_DOWNLOAD_TV_FOLDER=/downloads/TV
      - RPC_DOWNLOAD_MOVIES_FOLDER=/downloads/MOVIES
      - RPC_DOWNLOAD_MUSIC_FOLDER=/downloads/MUSIC 
      - RPC_CLIENT_USER=user
      - RPC_CLIENT_PASSWORD=PASSWORD
```

#### Working with environment variables 

All fields below are required, but some of them have already a default value, making the docker-compose file or command less bulky. 

| Variable                   | Use                                         |    Default value |
| -------------------------- | :------------------------------------------ | ---------------: |
| RPC_WATCH_TV_FOLDER        | Folder to watch .torrent files (TV shows)   |     /torrents/TV |
| RPC_WATCH_MOVIES_FOLDER    | Folder to watch .torrent files (Movies)     | /torrents/Movies |
| RPC_WATCH_TV_FOLDER        | Folder to watch .torrent files (Music)      |  /torrents/Music |
| RPC_DOWNLOAD_TV_FOLDER     | Where Transmission should download TV shows |                  |
| RPC_DOWNLOAD_MOVIES_FOLDER | Where Transmission should download Movies   |                  |
| RPC_DOWNLOAD_MUSIC_FOLDER  | Where Transmission should download Music    |                  |
| RPC_CLIENT_HOST            | Transmission Web UI host                    |      transmision |
| RPC_CLIENT_PORT            | Transmission Web UI port                    |             9091 |
| RPC_CLIENT_USER            | Transmission Web UI username                |                  |
| RPC_CLIENT_PASSWORD        | Transmission Web UI password                |                  |

####  Logs

For now, the logs will come in this folder so feel free to make a volume. 

```
/opt/logs
```

It is not my priority, but best would be to access it via docker logs also 

#### Configuration


#### Adding Or Removing Directories
Because this is a pretty quick-and-dirty solution, there is only 3 watchfolders. 
But as open source is open, don't hesitate to pull requests. 


