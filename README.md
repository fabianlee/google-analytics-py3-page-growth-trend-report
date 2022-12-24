# Generates pagecount growth/trend report using Google Analytics Reporting API v4

[Google Analytics](https://analytics.google.com/) makes it easy to view your page counts for an arbitrary date range, but what is more difficult is comparing these results to an older window of data to see:

* Which pages have grown/lost in absolute counts
* Which pages are trending growth/loss in terms of their percent (up-and-comers)

The [CalculateAnalyticsPageGrowth.py3](CalculateAnalyticsPageGrowth.py3) script gathers the latest window of UA data (default=30 days), and compares it to the 30 days preceding it to show you which pages have grown/lost in absolute terms as well as percent.

This can help you fine-tune your content creation, and invest in content that is showing the largest potential.

# Google Analytics UA turned off June 2023

This script uses the deprecated [Google Analytics Reporting API v4](https://developers.google.com/analytics/devguides/reporting/core/v4) (UA using viewId), which is scheduled to be turned off in June 2023.

The newer [Google Analytics Data API v1](https://developers.google.com/analytics/devguides/reporting/data/v1) (GA4 using propertyId), is the way forward for generating Google Analytics reports.  This can be done via the Python [Analytics Data API](https://googleapis.dev/python/analyticsdata/latest/index.html)


## Prerequisites

* Google GCP
  * [Create GCP Project](https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py)
  * [Enable project for Analytics API](https://console.cloud.google.com/start/api?id=analyticsreporting.googleapis.com&credential=client_key)
  * Create Google Service Account (GSA), download json key for auth later
* Google Analytics
  * Link Google Analytics to your web site, decorate site pages with tracker
  * Admin > "Property" > View Settings, copy down your View ID for reporting later
  * Admin > Account Access Management, add GSA in 'Viewer' role so it can query data


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

# width of report window can be changed (default=30 days)
./CalculateAnalyticsPageGrowth.py3 <jsonKeyFile> <analyticsViewID> -d 14
```



## REFERENCES

shows service account method of auth
https://itheo.tech/get-google-analytics-pageviews-with-python
https://medium.com/@tmmylo1021/extract-google-analytics-data-with-python-221626ed8975

shows expression building for pageviews
https://www.byperth.com/2017/06/11/google-analytics-api-python/

docs on reporting apiv4
https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet
