#!/usr/bin/env python
import pandas as pd
import csv

data = pd.read_csv('/home/ubuntu/BPI Challenge 2017.csv')

data_category_range = data['case:concept:name'].unique()
data_category_range = data_category_range.tolist()
count = 1
hundcount = 0
data.head(0).to_csv(str(hundcount) + 'log.csv', index = False)

for i,value in enumerate(data_category_range):
    print(hundcount)
    count += 1
    if count > 2000:
        break
    if (count%200) == 0:
        hundcount += 1
        data.head(0).to_csv(str(hundcount) + 'log.csv', index = False)
        
    data[data['case:concept:name'] == value].to_csv(str(hundcount) + 'log.csv', mode='a', index = False, header=False)

for i in range(0, hundcount):
    df = pd.read_csv(str(i) + 'log.csv')
    df.columns = df.columns.str.replace(':', '')
    df[~df.conceptname.str.contains("O_")].to_csv(str(i) + '_2log.csv')

    dfnew = pd.read_csv(str(i) + '_2log.csv')
    dfnew[~dfnew.conceptname.str.contains("W_")].to_csv(str(i) + 'LAPlog.csv')


for i in range(0, hundcount):
    cpath = "/home/ubuntu/splitlog/" + str(i) + "LAPlog.csv"
    cfile = open(cpath)
    creader = csv.reader((x.replace('\0', '') for x in cfile), delimiter=',')
    cnew_lines = list(creader)

    writer = csv.writer(open('%s_transactions.csv' % str(i), 'w'))
    writer.writerow(["funcname","empid","id","status","amount","goal"])
    

    for i in range(1, len(cnew_lines)):
        empid=cnew_lines[i][4]
        status=cnew_lines[i][5]
        appid=cnew_lines[i][12]
        amount=cnew_lines[i][13]
        goal=cnew_lines[i][10]

        if cnew_lines[i][5] == "A_Create Application" or  cnew_lines[i][5] == "A_Submitted":
            funcname="SubmitApplication"
            writer.writerow([funcname,empid,appid,status,amount,goal])

        else : 
            funcname=cnew_lines[i][5]
            writer.writerow([funcname,empid,appid,status])

#        if cnew_lines[i][5] == "A_Complete" or  cnew_lines[i][5] == "A_Incomplete":
#            writer.writerow(["ReadApplicationStatus",empid,appid])
#            writer.writerow(["SendDocumentation",empid,appid,status])

#        if cnew_lines[i][5] == "A_Pending" or  cnew_lines[i][5] == "A_Denied" or  cnew_lines[i][5] == "A_Cancelled":
#            writer.writerow(["ReadApplicationStatus",empid,appid])
