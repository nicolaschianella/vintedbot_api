# vintedbot
This repo contains all the resources for our own Vinted bot project.

The project is an API made to be used with the **streamlit_sales** frontend.



# Prerequisites

- AWS machine (guysmachine)
- Python 3.11



# Installation & Usage

- Run whatever **run/run_*.sh** file to install the required **venv** and run the API in background. Associated log file is **vinted_bot_*.log** (UTC timezone)
- The API will then start on **HOST**=127.0.0.1, **PORT**=8000 for prod, 5000 for dev, 5001 for hugo, 5002 for nico
- Useful command to kill the API: $ps -aux | grep 'backend' to retrieve **PID**, then $kill -9 PID



# Deployment

To deploy the project on **guysmachine**, you will first need to own an authorized SSH key. Then, you can run the **rsync/rsync_*.sh** file related to the target remote directory:

- **rsync/rsync_prod**: you need to be on branch **main**, the project will be sent to **guysmachine:~/vintedbot/vintedbot_prod**
- **rsync/rsync_dev:** you need to be on branch **dev**, the project will be sent to **guysmachine:~/vintedbot/vintedbot_dev**
- **rsync/rsync_nico:** you need to be on neither branch **main** nor **dev**, the project will be sent to **guysmachine:~/vintedbot/tests/nico**
- **rsync/rsync_hugo:** you need to be on neither branch **main** nor **dev**, the project will be sent to **guysmachine:~/vintedbot/tests/hugo**



# Available routes

- **HOST:PORT/api/health/backend**: checks if API is alive. To check if the API is alive using **PORT**=8000, you can run **requests/health.sh**
  - No input parameters
  - Returns: **backend.models.models.CustomResponse**
- **HOST:PORT/api/operations/get_clothes**: retrieves Vinted clothes based on input filters
  - Input parameters: **backend.models.models.InputGetClothes**, the specified filters to apply (one search)
  - Returns: **backend.models.models.CustomResponse**, found and reformatted clothes in **data** key
- **HOST:PORT/api/operations/get_requests**: retrieves all the requests stored in MongoDB
  - No input parameters
  - Returns: **backend.models.models.CustomResponse**, found and reformatted clothes in **data** dict, **requests** key
