#!/bin/bash


function help
{
    echo "Usage: deploy [ -d | --db-path ]
               [ -r | --file-repo ]
               [ -p | --port ]
               [ -h | --help  ]"
    echo " -d | --db-path   Existing empty folder with rw permission. To store persistant DB"
    echo " -r | --file-repo Existing empty folder with rw permission. To monitor for log files"
    echo " -p | --port      Available host port to map frontend access"
    echo " -h | --help      Print this help"

    exit 2
}

SHORT=d:,r:,p
LONG=db-path:,file-repo:,port:,help
OPTS=$(getopt -a -n deploy --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

while :
do
  case "$1" in
    -d | --db-path )
      dp="$2"
      shift 2
      ;;
    -r | --file-repo )
      fr="$2"
      shift 2
      ;;
    -p | --port )
      port="$2"
      shift 2
      ;;
    -h | --help )
      help
      exit 2
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      help
      ;;
  esac
done


if [ -d "$dp" ] && [ -d  "$fr" ]; then
         echo "dbpath=$dp" > .env
         echo "file_repo=$fr" >> .env
         echo "file_repo1=$fr" >> .env
        else
             echo "Folder do not exists...\n\n"
             help
             exit 2
fi


if  [ "$port" -gt 4999 ] && [ "$port" -lt 65535 ]; then
    echo "uiport=$port" >> .env
else 
    echo "Incorrect port number..."
    help
fi


#Creaqte pii network 
docker network create --driver=bridge --subnet=192.168.10.0/24 piinet-private
docker network create --driver=bridge --subnet=192.168.20.0/24 piinet-public

docker compose up -d --build --force-recreate --no-deps
