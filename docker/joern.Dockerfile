FROM alpine

RUN apk update && apk upgrade
RUN apk add --no-cache openjdk17-jdk python3 git curl gnupg bash nss ncurses php graphviz xdg-utils

RUN wget https://github.com/joernio/joern/releases/latest/download/joern-install.sh
RUN chmod +x ./joern-install.sh
RUN ./joern-install.sh

ENV PATH="${PATH}:/opt/joern/joern-cli"
WORKDIR /home
