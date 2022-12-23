# Generates pagecount growth/trend report from Google Analytics

[Google Analytics](https://analytics.google.com/) makes it easy to view your page counts for an arbitrary date range, but what is more difficult is comparing these results to an older window of data to see:

* Which pages have grown/lost in absolute counts
* Which pages are trending growth/loss in terms of their percent (up-and-comers)

The [CalculateAnalyticsPageGrowth.py3](CalculateAnalyticsPageGrowth.py3) script gathers the latest window of data (default=30 days), and compares it to the 30 days preceding it to show you which pages have grown/lost in absolute terms as well as percent.

This can help you fine-tune your content, and invest in content that is showing the largest potential.


## Prerequisites

* Google GCP Project
  * Project enabled for Analytics API
  * Google Service account created, download json key for auth later
* Google Analytics
  * Property tracking your web site
  * View belonging to Property, copy down viewID to be used for reporting later
  * Google Service account added to 'Account access management' in 'Viewer' role


Follow these instructions to create GCP project
https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

Enable API from link
https://console.cloud.google.com/start/api?id=analyticsreporting.googleapis.com&credential=client_key

create GSA 'analytics1' and download json key for auth by report.

## Run report against Google Analytics

### Prepare environment

```
# make sure python3 venv is installed
sudo apt-get update
sudo apt-get install software-properties-common python3 python3-dev python3-pip python3-venv curl git -y

git clone https://github.com/fabianlee/google-analytics-py3-page-growth-trend-report.git
cd google-analytics-py3-page-growth-trend-report

# create virtual env for isolated libs
python3 -m venv .
source bin/activate

# install module dependencies into virtual env
pip3 install -r requirements.txt
```

### Invoke Script

```
# place json key into this directory

# invoke report generator
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
