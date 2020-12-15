Website status check service

Services:
- webistecheck.py - service that check website and produce message to Apache Kafka topic
- logsave.py - service that store results into postgresql database

Configuration in config.json file

Example setup and run
```
docker build -f Dockerfile -t websitecheck .
docker build -f Dockerfile.logsave -t logsave .
docker run -it -d -p 5432:5432 -e POSTGRES_PASSWORD=krzysztof --name=postgres postgres
docker create --name=kafka -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST="127.0.0.1" --env ADVERTISED_PORT=9092 spotify/kafka && docker start kafka
docker run --net=host --rm -d --name=websitecheck websitecheck 
docker run --net=host --rm -d --name=logsave logsave
```
