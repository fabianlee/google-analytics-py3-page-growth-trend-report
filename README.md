# Generates pagecount growth/trend report from Google Analytics

[Google Analytics](https://analytics.google.com/) makes it easy to view your page counts for an arbitrary date range, but what is more difficult is comparing these results to an older window of data to see what pages have grown in terms of absolute numbers but also trends of "up-and-comers".


## Prerequisites

* Google GCP Project
  * Project enabled for Analytics API
  * Google Service account created, download json key for auth later
* Google Analytics
  * Property tracking your web site
  * View belonging to Property, copy down viewID to be used for reporting later
  * Google Service account added to 'Account access management' in 'Viewer' role


https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
console.cloud.google.com, create project

enable API from link, https://console.cloud.google.com/start/api?id=analyticsreporting.googleapis.com&credential=client_key

create GSA 'analytics1' and download json key

## Run report against Google Analytics

### Prepare environment

```
# make sure python3 venv is installed
sudo -s apt-get install python3-venv

git clone https://github.com/fabianlee/google-analytics-py3-page-growth-trend-report.git
cd google-analytics-py3-page-growth-trend-report

# create virtual env for isolated libs
python3 -m venv .
source bin/activate

# install module dependencies into virtual env
pip3 install -r requirements.txt
```

### Move json key into directory

### Invoke Script

```
./CalculateAnalyticsPageGrowth.py3 <jsonKeyFile> <analyticsViewID>
```



## REFERENCES

==shows service account method of auth
https://itheo.tech/get-google-analytics-pageviews-with-python
https://medium.com/@tmmylo1021/extract-google-analytics-data-with-python-221626ed8975

==shows expression building for pageviews
https://www.byperth.com/2017/06/11/google-analytics-api-python/

==docs on reporting apiv4
https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet
