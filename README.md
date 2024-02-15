# vintedbot_api
This repo contains all the resources for our own Vinted API project.



# Prerequisites

- AWS machine (guysmachine)
- Python 3.11



# Installation & Usage

- Run whatever **run/run_*.sh** file to install the required **venv** and run the API in background. Associated log file is **vintedbot_api_*.log** (UTC timezone)
- The API will then start on **HOST**=127.0.0.1, **PORT**=8000 for prod, 5000 for dev, 5001 for hugo, 5002 for nico
- Useful command to kill the API: $ps -aux | grep 'backend' to retrieve **PID**, then $kill -9 PID
- Swagger UI is accessible at **HOST:PORT/docs**



# Deployment

To deploy the project on **guysmachine**, you will first need to own an authorized SSH key. Then, you can run the **rsync/rsync_*.sh** file related to the target remote directory:

- **rsync/rsync_prod**: you need to be on branch **main**, the project will be sent to **guysmachine:~/vintedbot_api/vintedbot_prod**
- **rsync/rsync_dev:** you need to be on branch **dev**, the project will be sent to **guysmachine:~/vintedbot_api/vintedbot_dev**
- **rsync/rsync_nico:** you need to be on neither branch **main** nor **dev**, the project will be sent to **guysmachine:~/vintedbot_api/tests/nico**
- **rsync/rsync_hugo:** you need to be on neither branch **main** nor **dev**, the project will be sent to **guysmachine:~/vintedbot_api/tests/hugo**



# Available routes

All routes are documented in the Swagger UI



# Database

The API interacts with a local MongoDB instance (**guysvinted**)

Available collections:

- **requests**: saves information about clothes searches
- **associations**: saves information about relationships between clothes requests and Discord channels
- **stock**: saves information about stock (items in_stock and sold)
- **relay**: saves information about pickup points
- **cookies**: saves information about session cookies
