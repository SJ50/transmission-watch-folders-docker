FROM python:3.6-alpine
#LABEL maintainer="dev@soflane.ovh"
#LABEL url="https://github.com/soflane"


ARG S6_OVERLAY_RELEASE=https://github.com/just-containers/s6-overlay/releases/latest/download/s6-overlay-amd64.tar.gz
ENV S6_OVERLAY_RELEASE=${S6_OVERLAY_RELEASE}

ENV RPC_WATCH_TV_HD_FOLDER=/torrents/TV_HD
ENV RPC_WATCH_TV_UHD_FOLDER=/torrents/TV_UHD
ENV RPC_WATCH_MOVIES_HD_FOLDER=/torrents/Movies_HD
ENV RPC_WATCH_MOVIES_UHD_FOLDER=/torrents/Movies_UHD
ENV RPC_WATCH_MUSIC_FOLDER==/torrents/Music
ENV RPC_CLIENT_HOST=transmission
ENV RPC_CLIENT_PORT=9091


ADD ${S6_OVERLAY_RELEASE} /tmp/s6overlay.tar.gz
RUN apk update \
    && apk add py-pip \
    && pip install transmissionrpc \
	&& tar xzf /tmp/s6overlay.tar.gz -C / \
    && rm /tmp/s6overlay.tar.gz \
    && rm -rf /var/lib/apt/lists/* 
ADD root/ /

ENTRYPOINT ["/init"]
CMD python /app/main.py



