import pandas as pd
import glob
import os
import datetime
import numpy as np

from google.colab import userdata
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience

app_id = userdata.get('app-id')
app_secret = userdata.get('appsecret')
access_token = userdata.get('access-token')
ad_account_id = 'act_1267382926620452'
ad_pixel_id = '440430812832665'

FacebookAdsApi.init(app_id, app_secret, access_token)

def getCustomAudience():

  fields = [
    'id',
    'name',
    'rule',
    'retention_days',
    'event_sources',
    'subtype',
  ]

  params = {
  }

  return (AdAccount(ad_account_id).get_custom_audiences(
      fields=fields,
      params=params,
  ))

res = getCustomAudience()

#print using pandas dataframe
# df = pd.DataFrame(res)
# print(df)

# print using for loop
for item in res:
    # custom_audience = item['name']
    # print(f'{custom_audience}')
    print(f'{item}')

# save the result on custom_audience.csv
# df.to_csv('custom_audience.csv', index=False, sep='\t', encoding='utf-8')

def createCustomAudience():

  audience_source = "Site"
  audience_type = "Visitou"
  audience_days = [1, 3, 7, 14 ,21 ,30 ,60, 90, 180, 360]

  for day in audience_days:

    audience_name = "[" + audience_source + "] " + audience_type + " - " + str(day) + "D"

    fields = [
    ]

    items_params = {
        'name': str(audience_name),
        'rule': {
            "inclusions": {
                {
                    "operator" : "or",
                    "rules" : {
                        "event_sources": [{
                            "type": "pixel",
                            "id": int(ad_pixel_id),
                        }],
                        "retention_seconds" : int(8400),
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": "\\"
                                }
                            ]
                        },
                    },
                },
            },
        }
    }

    params = {frozenset(i.items()) for i in items_params}
    [dict(i) for i in params]
    print(params)
    
  # print(AdAccount(id).create_custom_audience(
  #   fields=fields,
  #   params=params,
  # ))

createCustomAudience()
