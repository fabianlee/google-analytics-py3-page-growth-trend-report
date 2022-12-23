# Generates growth/trend report on page count from Google Analytics

https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

console.cloud.google.com, create project

enable API from link, https://console.cloud.google.com/start/api?id=analyticsreporting.googleapis.com&credential=client_key


create GSA 'analytics1' and download json key

create local python3 project
mkdir google-analytics-py3-report-export
cd $_
python3 -
sudo -s apt-get install python3-venv
python3 -m venv .
source bin/activate
pip3 install --upgrade google-api-python-client
pip3 install --upgrade oauth2client

move json key into directory

# get source code
wget https://developers.google.com/static/analytics/resources/samples/service-py-v4.txt -O HelloAnalytics.py3
# add shebang for execution, make executable
sed -i -e '1i #!/usr/bin/env python' HelloAnalytics.py3
chmod +x *.py3


==shows service account method of auth
https://itheo.tech/get-google-analytics-pageviews-with-python
https://medium.com/@tmmylo1021/extract-google-analytics-data-with-python-221626ed8975

==shows expression building for pageviews
https://www.byperth.com/2017/06/11/google-analytics-api-python/

==docs on reporting apiv4
https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet
