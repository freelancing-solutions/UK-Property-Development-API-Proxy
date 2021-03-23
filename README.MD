### UK-Property-Development-API-Proxy

#### Developed to ease the use of UK Property Development API
--
#### Features
    Improved API Performance
    Cached API Results, enabling you to save on Costs
    Improved Security Key by Storing Your API Key in environment Variables
    Sentry Error Reporting and Performance Monitoring
    

#### Upgrade Path
    Support for redis caching


#### Setup Instructions
    1. clone this repo
    2. run pip install -r requirements.txt, inside the root of repo
    3. create .env file with the following keys
        - API_KEY
        - SECRET
        - API_ENDPOINT
        - SENTRY_DSN
    4. create app.yaml file if you intend to deploy to google cloud platform 
       see instructions @ https://cloud.google.com
    5. deploy your API
        
                