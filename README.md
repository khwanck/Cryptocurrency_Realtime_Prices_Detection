# Cryptocurrency Realtime Prices Detection
Project for Data Streaming and Realtime Analytics

## Idea & objective:
* Pactical realtime data analytic and configuration sofware tool.
* Simulation realtime data by use crypto prices of BNB CEX from Binance and BitKub.
* Collect data by python scripts and ingest to Kafka for distributed data to another platform. 
* Kafka sink to QuestDB for storage all data by confluent.
* Configuration dashboard on Grafana by monitering prices comparison, percentage changing in 24hrs and currently Thai Bath rate. 
* Analytics prices detection changing by ADWIN algorithm and alert signal to Line Notify.
* Can develop accurecy of ADWIN for apllied to another application in trading.

## Data Flow Diagram:
![image](https://github.com/khwanck/Cryptocurrency_Realtime_Prices_Detection/blob/main/images/Data_Flow_Diagram.PNG)

## Grafana Dashboard:
![image](https://github.com/khwanck/Cryptocurrency_Realtime_Prices_Detection/blob/main/images/Grafana_Dashboard.gif)

## ADWIN Detection and Line Nitify:
![image](https://github.com/khwanck/Cryptocurrency_Realtime_Prices_Detection/blob/main/images/ADWIN_Alert.gif)

## References:
* https://techmark.pk/comparing-influxdb-timescaledb-and-questdb/
* https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html
* https://questdb.io/tutorial/2021/02/05/streaming-heart-rate-data-with-iot-core-and-questdb/#visualizing-data-with-grafana
* https://github.com/UncleEngineer/BitkubAndBinance
* https://github.com/Yitaek/kafka-crypto-questdb
* https://scikit-multiflow.readthedocs.io/en/stable/api/generated/skmultiflow.drift_detection.ADWIN.html


