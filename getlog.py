#TODO: mkdir csv if it does not exist. If it exists then rm csv/*


#!/usr/bin/env python

import json
import os
import collections
import re
import csv
import sys
import pm4py
import pandas as pd

#log = pm4py.read_xes('/home/ubuntu/BPI Challenge 2017.xes.gz')
#pd = pm4py.convert_to_dataframe(log)
#pd.to_csv('/home/ubuntu/BPI Challenge 2017.csv')
#df = pd.write_csv('/home/ubuntu/hospital_log.csv', delimiter=',')


df = pd.read_csv('/home/ubuntu/BPI Challenge 2017.csv', nrows=10000)
df.to_csv('/home/ubuntu/short_bankbpi.csv')
