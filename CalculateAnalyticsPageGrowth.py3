#!/usr/bin/env python3
"""
 Calculates growth and trends for unique page counts from Analytics Reporting API V4 (UA).
 Google will turn off UA on June 2031, in favor of GA4
 
 Starter attribution:
 https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
"""

#
# this is how requirements.txt was constructed:
# pip3 install google-api-python-client
# pip3 install --upgrade oauth2client
# pip3 freeze | tee requirements.txt
#
import sys
import traceback
import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def initialize_analyticsreporting(jsonKeyFilePath):
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      jsonKeyFilePath, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_unique_pagecount_report(analytics,googleViewID,startDateStr,endDateStr):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """

  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': googleViewID,
          'dateRanges': [{'startDate': startDateStr, 'endDate': endDateStr}],
          'metrics': [
             {'expression': 'ga:uniquePageviews'}
             ],
          'dimensions': [{'name': 'ga:pagePath'}],
          'orderBys': [
              {"fieldName": "ga:uniquePageviews", "sortOrder":"ASCENDING" }
            ]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ', dimension)

      for i, values in enumerate(dateRangeValues):
        print('Date range:', str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print(metricHeader.get('name') + ':', value)

def print_pagecount_response_csv(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      # show page count and page path
      pageCount = dateRangeValues[0].get('values')[0]
      print(f"{pageCount},{dimensions[0]}")

def build_pagecount_dict(response):
  """Parses Analytics Reporting API V4 response and creates dict of pagepath->page counts

  Args:
    response: An Analytics Reporting API V4 response.
  """
  result = {}
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      # show page count and page path
      pageCount = dateRangeValues[0].get('values')[0]
      # remove pages we have no interest in counting
      valid_path = not(
        "?" in dimensions[0] or 
        "&" in dimensions[0] or 
        "/category/" in dimensions[0] or 
        "/page/" in dimensions[0] or 
        "/tag/" in dimensions[0] or
        len(dimensions[0]) < 16 # eliminates spam requests and ones pointing to just dates
        )
      if valid_path:
        result[dimensions[0]] = pageCount
        #print(f"{pageCount},{dimensions[0]}")

  return result


def main():

  examples = '''USAGE:
 jsonKeyFile googleViewID [reportingDays=30]

 jsonKeyFile is the Google service account json key file
 googleViewID can be seen by going to Google Analytics, Admin>View Settings)
 reportingDays is the number of days to rollup into reporting block (today-reportingDays)


 EXAMPLES:
 my.json 123456789
 my.json 123456789 14
'''

  # define arguments
  ap = argparse.ArgumentParser(description="Calculate growth/trends from Analytics",epilog=examples,formatter_class=argparse.RawDescriptionHelpFormatter)
  ap.add_argument('key', help="json key of Google service account")
  ap.add_argument('viewid', help="viewID from Google Analytics (Admin>View Settings)")
  ap.add_argument('-d', '--days', default="30",help="number of days in reporting window")
  args = ap.parse_args()

  print(f"service account json={args.key}, Google Analytics viewID={args.viewid}, reporting window={args.days} days")
  analytics = initialize_analyticsreporting(args.key)

  # get unique page counts per reporting day width
  ndays=int(args.days)
  response_latest = get_unique_pagecount_report(analytics, args.viewid, startDateStr=f"{ndays}daysAgo", endDateStr="0daysAgo")
  response_older  = get_unique_pagecount_report(analytics, args.viewid, startDateStr=f"{ndays*2}daysAgo", endDateStr=f"{ndays+1}daysAgo")
  print(f"lastest reporting window: 0daysAgo -> {ndays}daysAgo")
  print(f"older   reporting window: {ndays+1}daysAgo -> {ndays*2}daysAgo")
  print()

  # build dictionary of page->count
  pagecounts_latest = build_pagecount_dict(response_latest)
  pagecounts_older  = build_pagecount_dict(response_older)

  # build dictionary for page->delta count, page->delta percent
  pagecounts_delta = {}
  pagecounts_delta_percent = {}
  for path in pagecounts_latest:
    try:
      count_latest = pagecounts_latest[path]
      if path in pagecounts_older:
        count_older  = pagecounts_older[path]

        # calculate absolute difference between timeframes
        delta = int(count_latest) - int(count_older)
        # calculate percent change in terms of total count
        delta_percent = float(delta)/float(count_latest)

        # save results
        pagecounts_delta[path] = int(delta)
        pagecounts_delta_percent[path] = float(delta_percent)
        #print(f"{count_latest},{count_older},{delta},{delta_percent},{path}")
      else:
        #print(f"OLDERKEYMISSING does not exist {path} newer count was {count_latest}")
        pass
    except KeyError:
      print(f"KEYERROR {path}")
      traceback.print_exc()

  # sort absolute deltas and percent so we can see trends
  # array of tuples
  sorted_deltas = sorted(pagecounts_delta.items(), key=lambda x:x[1])
  sorted_deltas_percent = sorted(pagecounts_delta_percent.items(), key=lambda x:x[1])
  #for row in sorted_deltas:
  #  print(f"{row[1]},{row[0]}")

  # how many losers/winners to display
  nrows=25

  # show losers and winners in terms of absolute hits
  print("====BIGGEST LOSERS======")
  print("delta,count,path")
  for row in sorted_deltas[:nrows]:
    delta=row[1]
    path=row[0]
    totalcount=pagecounts_latest[path]
    print(f"{delta},{totalcount},{path}")

  print("====BIGGEST WINNERS======")
  print("delta,count,path")
  for row in sorted_deltas[-nrows:]:
    delta=row[1]
    path=row[0]
    totalcount=pagecounts_latest[path]
    print(f"{delta},{totalcount},{path}")

  # show losers and winners in terms of percent growth (% of total)
  print("====TRENDING DOWN======")
  print("growth%,newcount,oldcount,path")
  for row in sorted_deltas_percent[:nrows]:
    percent=row[1]
    path=row[0]
    totalcount=pagecounts_latest[path]
    oldcount=pagecounts_older[path]
    print(f"{percent*100:.0f}%,{totalcount},{oldcount},{path}")

  print("====TRENDING UP======")
  print("growth%,newcount,oldcount,path")
  for row in sorted_deltas_percent[-nrows:]:
    percent=row[1]
    path=row[0]
    totalcount=pagecounts_latest[path]
    oldcount=pagecounts_older[path]
    print(f"{percent*100:.0f}%,{totalcount},{oldcount},{path}")

if __name__ == '__main__':
  main()
