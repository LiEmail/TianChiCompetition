# -*- coding: utf-8 -*-
import csv
import time

#数据读入
ref_time_start = '2014-12-12 00' 
ref_time_end = '2014-12-12 23'
input_data_file = 'D:\\TianChi\\tianchi_mobile_recommend_train_user.csv'
output_data_file = 'D:\\TianChi\\reference1212.csv'
time_stramp_start = int(time.mktime(time.strptime(ref_time_start,"%Y-%m-%d %H")) /(3600*24))
time_stramp_end = int(time.mktime(time.strptime(ref_time_end,"%Y-%m-%d %H")) /(3600*24))

#tianchi_mobile_recommend_train_user
user_good_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典
user_dic = {}  #用户词典
test_user_dic = {}
with open(input_data_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user_id = row['user_id']
        item_id = row['item_id']
        behavior_type = row['behavior_type']
        b_time = row['time']
        item_category = row['item_category']
        
        time_array = time.strptime(b_time,"%Y-%m-%d %H")
        time_stamp = int(time.mktime(time_array))
        b_time = int(time_stamp/3600)
        b_time = int(b_time/24)
       
        #存储用户商品信息
        if b_time <= time_stramp_end and b_time >= time_stramp_start :
            if test_user_dic.has_key(user_id) == True:
                good = test_user_dic[user_id]
                if good.has_key(item_id) == True:
                    one_user_one_good = good[item_id]
                    one_user_one_good[behavior_type] = 1
                else:
                    good[item_id] = {behavior_type:1}
            else:
                test_user_dic[user_id] = {item_id:{behavior_type:1}}
csvfile.close()

#特征提取
import csv
csvfile = file(output_data_file,'wb')
features = [('user_id','iterm_id')]
writer = csv.writer(csvfile)
writer.writerows(features)
for user in test_user_dic:
    test_user = test_user_dic[user]
    for good in test_user:
        features = []
        if test_user[good].has_key('4'):
            features = features + [user]
            features = features + [good]
            writer.writerows([features])

print "end"
csvfile.close()