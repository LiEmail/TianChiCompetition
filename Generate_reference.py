# -*- coding: utf-8 -*-
import csv
import time
print time.time()

#数据读入
start_time = '2014-11-13 00'
cut_time = '2014-12-11 23'
test_time = '2014-12-12 23' 

test_time_array = time.strptime(test_time,"%Y-%m-%d %H")
test_time_stamp = int(time.mktime(test_time_array))
test_time_stamp = int(test_time_stamp/(3600*24))
print 'test time:',
print test_time_stamp
#tianchi_mobile_recommend_train_user
user_good_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典
user_dic = {}  #用户词典
test_user_dic = {}
with open('D:\\pythonCode\\tianchi_mobile_recommend_train_user.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user_id = row['user_id']
        item_id = row['item_id']
        behavior_type = row['behavior_type']
        b_time = row['time']
        item_category = row['item_category']
        
        import time
        time_array = time.strptime(b_time,"%Y-%m-%d %H")
        time_stamp = int(time.mktime(time_array))
        b_time = int(time_stamp/3600)
        b_time = int(b_time/24)
       
        #存储用户商品信息
        if b_time == test_time_stamp:
            if test_user_dic.has_key(user_id) == True:
                good = test_user_dic[user_id]
                if good.has_key(item_id) == True:
                    one_user_one_good = good[item_id]
                    one_user_one_good[behavior_type] = 1
                else:
                    good[item_id] = {behavior_type:1}
            else:
                test_user_dic[user_id] = {item_id:{behavior_type:1}}
print "read ok"
import time
print time.time()
csvfile.close()
#特征提取
import csv
csvfile = file('D:\\pythonCode\\reference.csv','wb')
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
import time
print time.time()

csvfile.close()
