# -*- coding: cp936 -*-
import csv
import time
print time.time()
def date2days(date,date_type):
    import time
    date_array = time.strptime(date,date_type)
    days = int((time.mktime(date_array))/(3600*24))
    return days
def date2hours(date,date_type):
    import time
    date_array = time.strptime(date,date_type)
    hours = int((time.mktime(date_array))/3600)
    return hours

print 'start generate testing feature'
#数据读入
start_time = '2014-11-13 00'   #设置开始时间
test_time = '2014-12-18 23'  #设置截止时间
week_before = '2014-12-11 00'  #设置截止前一周
day15_before = '2014-12-03 00'
date_type = '%Y-%m-%d %H'
input_data_file = 'E:\\Github\\TianChiCompete\\G2.csv'
output_data_file = 'E:\\Github\\TianChiCompete\\G1_feature.csv'

start_time_stamp = date2days(start_time,date_type)
print 'start time:',
print start_time_stamp

test_time_stamp = date2days(test_time,date_type)
print 'test time:',
print test_time_stamp

total_day = float(test_time_stamp - start_time_stamp)

week_before_stamp = date2days(week_before,date_type)
print 'one week before:',
print week_before_stamp
day15_before_stamp = date2days(day15_before,date_type)

user_good_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典
user_dic = {}  #用户词典
with open(input_data_file) as csvfile:
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
        ##################商品统计信息################
        #商品一周销量
        if (b_time >= week_before_stamp) and (b_time <= test_time_stamp):
            if good_dic.has_key(item_id) == True:
                one_good = good_dic[item_id]
                if one_good.has_key('7d') == True:
                    one_good['7d'] = one_good['7d'] + 1
                else:
                    one_good['7d'] = 1
            else:
                good_dic[item_id] = {'7d':1}
        #商品15天销量
        if (b_time >= day15_before_stamp) and (b_time <= test_time_stamp):
            if good_dic.has_key(item_id) == True:
                one_good = good_dic[item_id]
                if one_good.has_key('15d') == True:
                    one_good['15d'] = one_good['15d'] + 1
                else:
                    one_good['15d'] = 1
            else:
                good_dic[item_id] = {'15d':1}
        if b_time <= test_time_stamp:
            if good_dic.has_key(item_id) == True:
                one_good = good_dic[item_id]
                if one_good.has_key(user_id) != True:
                    one_good[user_id] = 1
        #################用户活跃购买信息#############
        if b_time <= test_time_stamp:
            if user_dic.has_key(user_id) == True:
                user_i = user_dic[user_id]    
                if user_i.has_key(b_time) != True:
                    user_i[b_time] = 1
                if behavior_type == '4':
                    if user_i.has_key('4b'):
                        user_i['4b'] = user_i['4b'] + 1
                    else:
                        user_i['4b'] = 1
            else:
                user_dic[user_id] = {b_time:1}
                if behavior_type == '4':
                    user_dic[user_id]['4b'] = 1
        #################用户商品信息################
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
print "read ok"
import time
print time.time()
csvfile.close()
##################################特征提取，生成训练特征###################
import csv
csvfile = file(output_data_file,'wb')
features = [('user_id','item_id','user_good_buy_count','user_good_view_count','good_sold_7d','good_sold_15d','good_buyer_count','user_day_active_rate','user_buy_average_active_day')]
writer = csv.writer(csvfile)
writer.writerows(features)
for user in user_good_dic:
    one_user = user_good_dic[user]
    for good in one_user:
        features = []
        one_user_one_good = one_user[good]
        operation1_c = 0
        operation2_c = 0
        operation3_c = 0
        operation4_c = 0
        if one_user_one_good.has_key('1') == True:        
            operation1_c = len(one_user_one_good['1'])
        if one_user_one_good.has_key('2') == True:        
            operation2_c = len(one_user_one_good['2'])
        if one_user_one_good.has_key('3') == True:        
            operation3_c = len(one_user_one_good['3']) 
        if one_user_one_good.has_key('4') == True:        
            operation4_c = len(one_user_one_good['4'])                                    
        operation_c = operation1_c + operation2_c + operation3_c + operation4_c

        features = features + [user]   #########user_id,item_id
        features = features + [good]

        features = features + [operation4_c] ##########user_good_buy_count(用户购买该商品次数)
        features = features + [operation_c] ##########user_good_view_count(用户浏览该商品次数，所有操作)
        good_sold_7d = 0                     ########good_sold_7d（商品在7天内售出量）
        good_sold_15d = 0                   ########good_sold_15d（商品在15天内售出量）
        if good_dic.has_key(good) == True:
            good_i = good_dic[good]
            if good_i.has_key('7d') == True:
                good_sold_7d = good_i['7d']
            if good_i.has_key('15d') == True:
                good_sold_15d = good_i['15d']
        features = features + [good_sold_7d]
        features = features + [good_sold_15d]
        good_buyer_count = 0                 ###########good_buyer_count（购买该商品的人数）
        if good_dic.has_key(good):
            good_item = good_dic[good]
            good_buyer_count = len(good_item)
        features = features + [good_buyer_count]
        user_day_active_rate = 0.0            ############user_day_active_rate（用户活跃天数比值）
        user_day_active = len(user_dic[user])
        user_buy = 0
        if user_dic[user].has_key('4b'):
            user_day_active = len(user_dic[user]) - 1
            user_buy = user_dic[user]['4b']
        user_day_active_rate = float(user_day_active)/total_day
        features = features + [user_day_active_rate]
        user_buy_average_active_day = float(user_buy)/user_day_active   ###############user_buy_average_active_day（用户活跃天数平均购买量）
        features = features + [user_buy_average_active_day]
        writer.writerows([features])
import time
print time.time()
csvfile.close()
