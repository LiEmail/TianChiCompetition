import csv
import time
print time.time()

#数据读入
start_time = '2014-11-13 00'
cut_time = '2014-12-11 23'
test_time = '2014-12-18 23'
week_before = '2014-12-11 00' 

start_time_array = time.strptime(start_time,"%Y-%m-%d %H")
start_time_stamp = int(time.mktime(start_time_array))
start_time_stamp = int(start_time_stamp/(3600*24))
print 'start time:',
print start_time_stamp

cut_time_array = time.strptime(cut_time,"%Y-%m-%d %H")
cut_time_stamp = int(time.mktime(cut_time_array))
cut_time_stamp = int(cut_time_stamp/(3600*24))
print 'cut time:',
print cut_time_stamp

test_time_array = time.strptime(test_time,"%Y-%m-%d %H")
test_time_stamp = int(time.mktime(test_time_array))
test_time_stamp = int(test_time_stamp/(3600*24))
print 'test time:',
print test_time_stamp

total_day = float(cut_time_stamp - start_time_stamp)

week_before_array = time.strptime(week_before,"%Y-%m-%d %H")
week_before_stamp = int(time.mktime(week_before_array))
week_before_stamp = int(week_before_stamp/(3600*24))
print 'one week before:',
print week_before_stamp

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
        #存储商品统计信息
        if (b_time >= week_before_stamp) and (b_time <= test_time_stamp):
            if good_dic.has_key(item_id) == True:
                one_good = good_dic[item_id]
                if one_good.has_key(behavior_type) == True:
                    one_good[behavior_type] = one_good[behavior_type] +1
                else:
                    one_good[behavior_type] = 1
            else:
                good_dic[item_id] = {behavior_type:1}
        #存储用户商品信息
        if b_time <= test_time_stamp:
            if user_good_dic.has_key(user_id) == True:
                one_user = user_good_dic[user_id]
                if one_user.has_key(item_id) == True:
                    one_user_one_good = one_user[item_id]
                    if one_user_one_good.has_key(behavior_type) == True:
                        one_user_one_good_one_behavior = one_user_one_good[behavior_type]
                        one_user_one_good_one_behavior = one_user_one_good_one_behavior + [b_time]
                    else:
                        one_user_one_good[behavior_type] = [b_time]
                else:
                    one_user[item_id] = {behavior_type:[b_time]}
            else:
                user_good_dic[user_id] = {item_id:{behavior_type:[b_time]}}
        if b_time <= test_time_stamp:
            if test_user_dic.has_key(user_id) == True:
                good = test_user_dic[user_id]
                if good.has_key(item_id) != True:
                    good[item_id] = 1
            else:
                test_user_dic[user_id] = {item_id:1}
            
print "read ok"
import time
print time.time()
csvfile.close()
#特征提取
import csv
csvfile = file('D:\\pythonCode\\vectors.csv','wb')
features = [('user_id','item_id','feature1','feature2','feature3')]
writer = csv.writer(csvfile)
writer.writerows(features)
for user in test_user_dic:
    if user_good_dic.has_key(user) != True:
        continue
    one_user = user_good_dic[user]
    test_user = test_user_dic[user]
    for good in test_user:
        features = []
        if one_user.has_key(good) != True:
            continue
        one_user_one_good = one_user[good]
        operation1_c = 0
        operation2_c = 0
        operation3_c = 0
        operation4_c = 0
        operation_times = []
        if one_user_one_good.has_key('1') == True:        
            operation1_c = len(one_user_one_good['1'])
        if one_user_one_good.has_key('2') == True:        
            operation2_c = len(one_user_one_good['2'])
        if one_user_one_good.has_key('3') == True:        
            operation3_c = len(one_user_one_good['3'])
            operation_times = operation_times + one_user_one_good['3'] 
        if one_user_one_good.has_key('4') == True:        
            operation4_c = len(one_user_one_good['4'])
            operation_times = operation_times + one_user_one_good['4']                                    
        operation_times = set(operation_times)
        operation_day_count = len(operation_times)
        operation_day_count = float(operation_day_count)
        operation_c = operation1_c + operation2_c + operation3_c + operation4_c
        
        good_all_operation4 = 0
        if good_dic.has_key(good):
            if good_dic[good].has_key('4'):
                good_all_operation4 = good_dic[good]['4']
                
        feature4 = operation_day_count/total_day
        features = features + [user]
        features = features + [good]
        #features = features + [operation4_c]
        features = features + [operation_c] 
        features = features + [good_all_operation4]       
        features = features + [feature4]
        writer.writerows([features])
import time
print time.time()

csvfile.close()
