set "your_dir=C:\Cryptocurrency_Realtime_Prices_Detection\src_docker\docker-compose"     
pushd %cd%
cd %your_dir%
curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" --data @postgres-sink-binance_bitkub.json http://localhost:8083/connectors
