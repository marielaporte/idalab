# ICUZen Application
This is a sample project for an ICUZen application. The application is designed to read vital sign data from a hospital API, make predictions using a simple model, and notify clinicians if a patient needs assistance. The application consists of several modules, which are described below.

## Modules
### api.py
This module contains a Flask API that receives vital sign data from the hospital API, makes predictions, and publishes the results to a Kafka topic.

### consume.py
This module subscribes to a Kafka topic, receives alarm data from the API module, processes the data for each patient, and prints the results.

###  hospital_api_client.py
This module is used to connect to the hospital API and retrieve patient data.

###  model.py
This module contains the ICUZen class, which is used to make predictions based on vital sign data.

###  main.py
This module is the main entry point for the application. It initializes the dashboard, reads data from the hospital API, makes predictions, and saves the results to a CSV file.

### raw_data.csv
This file contains patient data in CSV format.

### predictions.csv
This file contains prediction results in CSV format.

## Getting started
To run the application, follow these steps:

- Clone the repository to your local machine.

- Install the required libraries using the command ```pip install -r requirements.txt```.

- Start the Kafka server using the command ```bin/kafka-server-start.shconfig/server.properties```.

- **Note:** The API and consumer modules are not yet implemented and are not currently functional, so there is no need to start them.

- Start the main application ```main.py```.

The script will retrieve patient data from the hospital API, make predictions using the ICUZen model, and save the results to the ```predictions.csv``` file. 

**Note:** With full implementation, if any patient requires assistance, an alarm will be sent to the API, which will publish the data to the Kafka topic. The consumer will then process the alarm data and print the results.
