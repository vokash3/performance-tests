#!/bin/bash

echo "Приступаю к сборке и запуску"

docker build -f Dockerfile.example -t docker-example .

echo "*****Вывод из контейнера:*****"

docker run docker-example

echo "*************************"

CONTAINER_ID=$(docker ps -a -q --filter "ancestor=docker-example")

if [ -n "$CONTAINER_ID" ]; then
    echo "Удаляю контейнер: $CONTAINER_ID"
    docker rm "$CONTAINER_ID" --force
else
    echo "Контейнер не найден."
fi

# echo "Удаляю образ: docker-example"
# docker rmi docker-example

