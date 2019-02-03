import os
import json
import csv
import pandas as pd
from pandas.io.json import json_normalize
import time

MYNAME = 'Matthew Filipovich'
def import_messages():
    DF_list = list() #list of DataFrame objects
    friends = list() #list of friends
    list_of_messages = os.listdir('messages/inbox') #list of folders as strings

    for i in range(len(list_of_messages)): #iterate through each folder and append to DF_list
        try:
            file = 'messages/inbox/' + list_of_messages[i] +'/message.json'
            num = sum(1 for line in open(file)) 
            if num > 40: #check for bad files
                with open(file, 'r') as json_data:
                    dt = json.load(json_data)
                name = dt['participants']
                if(len(name) == 2 and name[0]['name'] != MYNAME):
                    friends.append(name[0]['name'])
                else:
                    friends.append('GROUP')
                DF_list.append(pd.DataFrame(json_normalize(dt, 'messages')[['timestamp_ms', 'content', 'sender_name']]))
        except:
            print(':)')
    return DF_list, friends

def best_friend(DF_list, friends): #parameter list of DataFrame objects from import_message
    num_messages = list()
    the_friend = list()

    for i in range(len(DF_list)):
        if(friends[i] == 'GROUP'):
            continue
        num_messages.append(len(DF_list[i].index))
        the_friend.append(friends[i])

    table = pd.DataFrame({'Messages' : num_messages, 'Friend' : the_friend})
    table = table.sort_values(by = 'Messages', ascending=False)
    return table

def table_function(DF_List):
    bigdata = pd.concat(DF_list, ignore_index=True)
    bigdata = bigdata.sort_values(['timestamp_ms', 'content', 'sender_name'], ascending=[True, False, False])
    bigdata['content'] = bigdata['content'].str.replace('â', '\'')
    bigdata_user = bigdata.loc[bigdata['sender_name'] == MYNAME]
    bigdata_user.set_index('timestamp_ms', inplace=True)
    bigdata_user_date = bigdata_user.loc['1514782800000':'1546405200000']
    return bigdata_user_date

def ads():
    interests_list = list()
    advertisers_list = list()
    with open('ads/ads_interests.json', 'r') as file:
        i = json.load(file)
    with open('ads/advertisers_who_uploaded_a_contact_list_with_your_information.json', 'r') as file:
        a = json.load(file)                
    interests_list.append(pd.DataFrame({'Topics' : i['topics']}))
    advertisers_list.append(pd.DataFrame({'Advertisers' : a['custom_audiences']}))
    return interests_list, advertisers_list

def sleepinfo(bigdata_user_date):
    sleeplist = []
    datelist = []
    five_am = 1549015200000
    count = 0

    for i in range(len(bigdata_user_date)):

        j = len(bigdata_user_date) - (i + 1)

        temp = bigdata_user_date.index[j] - bigdata_user_date.index[j - 1]
        if temp > 10800000 and temp < 46800000:
            five_am -= 86400000
            temp = temp / (1000 * 60 * 60)

            temp_0 = bigdata_user_date.index[j] / 1000
            temp_date = time.strftime('%Y-%m-%d', time.localtime(temp_0))

            count += 1
            sleeplist.append(temp)
            datelist.append(temp_date)

    sleep = pd.DataFrame(sleeplist)
    date = pd.DataFrame(datelist)

    table_0 = pd.concat([date, sleep], axis=1)
    table_0.columns = ['date', 'sleep']
    table_0.drop_duplicates('date')
    return table_0

def average_daily_messages(bigdata_user_date):
    average_messages = len(bigdata_user_date) / (397) #replace 397 with number of days you're considering in data
    return average_messages

interests_list, advertisers_list = ads() 
DF_list, friends = import_messages() #ignore
all_messages_list = table_function(DF_list)
bff_list = best_friend(DF_list, friends)
sleep_list = sleepinfo(all_messages_list)
avg_daily = average_daily_messages(all_messages_list)

print(interests_list) #graph
print(advertisers_list) #graph
print(all_messages_list)
print(bff_list) #graph
print(sleep_list) #graph
print(avg_daily) #graph

all_messages_list.to_csv('mes.csv')