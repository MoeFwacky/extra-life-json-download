# Download Extra Life Data to JSON Files
A python3 script to download team, participant and donor data from the Extra Life API and store as JSON files.

## How to Use
- Download files into desired folder
- Edit the TeamID variable in the extra-life-config.py file to match the number at the end of the "Your Team" URL
- Run the script in a terminal or command line with python3.

## What it Does
On first run, the script will download team data, team donations data and team participants data into three JSON files. After that, it sleeps for the number of seconds defined in the rateLimit value of the config file (default 15 seconds). On each loop, it checks each endpoint's etag value for changes. If no changes are found, it sleeps again. If the value has changed, it indicates an update in data, and a new JSON is downloaded to the file.

## What use does this have?
You can parse the downloaded data with another script, and use the data to populate your livestream overlay, webpage or whatever else you can think to do with JSON data.
