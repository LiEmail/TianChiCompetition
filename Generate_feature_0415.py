# -*- coding: cp936 -*-
import csv
import time

#数据模块
start_time = '2014-11-13 00'
cut_time = '2014-12-18 00'
test_time = '2014-12-19 00'
dir = 'E:\\天池_移动推荐\\'
input_user_file = dir + 'row_record_no1212.csv'
input_item_file = dir + 'tianchi_mobile_recommend_train_item.csv'
#input_user_file = dir + 'G2.csv'
#input_item_file = dir + 'G1.csv'
output_train_file = dir + 'TrainSet.csv'
output_vec_file = dir + 'PredictVector.csv'

#V1.0 - 用户的活跃度 && 商品总的购买量等
days_feature = (3, 7, 15)  #前3, 7, 15天的数据
days_featureName = ("Sales_3","Sales_7","Sales_15")
behavior = ("","click","store","shopcar","buy")     #用户行为的title
user_feature_name  = ("active_ratio","buy_ratio","buy_day")  #用户特征的title
#train_title  = ['target',behavior[4],behavior[3],days_featureName[0],user_feature_name[0],user_feature_name[1]] #trainSet的title row
#predict_title  = ['user_id','item_id',behavior[4],behavior[3],days_featureName[0],user_feature_name[0],user_feature_name[1]] #PredictSet的title row
ratio = 30 # 百分比型的特征归一化的参数

#V2.0 - 前3天的 点击/收藏/加购物车/购买 && 前7天的点击/收藏/加购物车/购买
user_good_days_feature_name = ("3days","7days","15days")
user_good_feature_3days = ("","3days_click","3days_store","3days_shopcar","3days_buy")
user_good_feature_7days = ("","7days_click","7days_store","7days_shopcar","7days_buy")
train_title    = ['target',user_good_feature_3days[1], user_good_feature_3days[2], user_good_feature_3days[3], user_good_feature_3days[4], user_good_feature_7days[1], user_good_feature_7days[2], user_good_feature_7days[3], user_good_feature_7days[4]]
predict_title  = ['user_id', 'item_id', user_good_feature_3days[1], user_good_feature_3days[2], user_good_feature_3days[3], user_good_feature_3days[4], user_good_feature_7days[1], user_good_feature_7days[2], user_good_feature_7days[3], user_good_feature_7days[4]]

#########################################################################################
#时间戳转化成天数
def date2days(date):
    test_time_array = time.strptime(date,'%Y-%m-%d %H')
    days_i = int((time.mktime(test_time_array))/(3600*24))
    days_f = float((time.mktime(test_time_array))/(3600*24))
    if(days_f - days_i) > 0.66 : 
        return days_i + 1
    else:
        return days_i

#形成 userid_itemid串，用于匹配target
def AppendUseItemString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item
	
#清除一些明显不符合的样本
def clearNagetiveSample(user_good_item):
    if user_good_item[behavior[4]] == 0:
        if user_good_item[behavior[3]] == 0 and (user_good_item[behavior[1]] + user_good_item[behavior[2]]) < 4:
            return True
        if user_good_item[behavior[3]] > 9:
            return True
    return False
	
start_time_stamp = date2days(start_time)
cut_time_stamp   = date2days(cut_time)
print  cut_time_stamp
#print date2days('2014-12-17 23')
test_time_stamp  = date2days(test_time)
user_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典  
user_good = {}  #用户-品牌词典
use_item_result = {} # 用户-商品购买情况(二类结果)
test_user_dic = {}

#生成需要的带特征向量的文件
# out_put_type取值 
#0-trainSet;
#1-PredictVector
#2-refenceSet(有待扩展) 
def GenerateFeature(out_put_type) :
    #商品信息的统计
    with open(input_item_file) as item_csv_file:
        item_reader = csv.DictReader(item_csv_file)
        for row in item_reader :
            good_dic[row['item_id']] = {'category': row['item_category'],\
                                        'geohash': row['item_geohash'],\
                                        behavior[1]: 0,\
                                        behavior[2]: 0,\
                                        behavior[3]: 0,\
                                        behavior[4]: 0,\
                                        days_featureName[0]: 0,\
                                        days_featureName[1]: 0,\
                                        days_featureName[2]: 0\
                                        }
    #用户 && 用户-品牌 信息的统计
    user_count = 0
    whole_count = 0
    tag_count = 0
    with open(input_user_file) as csvfile :
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            item_id = row['item_id']

            #只统计出现在子集中的商品
            if good_dic.has_key(item_id) is False:
                continue

            behavior_type = behavior[int(row['behavior_type'])]
            b_time = date2days(row['time'])
            item_category = row['item_category']
            user_count = user_count + 1
            if user_count %100000 == 0:
                print user_count
            whole_count = whole_count + 1
            
            #如果out_put_type  == 1（PredictVectors）,test_time之前的都要加入
            #如果out_put_type  == 0（trainSet）,cut_time之前的都要加入
            #统一用 time_stamp表示
            time_stamp = 0
            if out_put_type == 1 :
                time_stamp = test_time_stamp
            elif out_put_type == 0 :
                time_stamp = cut_time_stamp

            if  b_time < time_stamp :
                #更新商品统计词典
                one_good = good_dic[item_id]
                one_good[behavior_type] = one_good[behavior_type] + 1
                # 更新火爆程度 时间差值可能有12小时的误差
                if time_stamp - b_time <= days_feature[0] :
                    one_good[days_featureName[0]] = one_good[days_featureName[0]] + 1
                if time_stamp - b_time <= days_feature[1] :
                    one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
                if time_stamp - b_time <= days_feature[2] :
                    one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
                
                #更新用户统计词典
                if user_dic.has_key(user_id) is False :  #如果不存在键值，先创建一个键值
                    user_dic[user_id] = { behavior[1]: 0,\
                                          behavior[2]: 0,\
                                          behavior[3]: 0,\
                                          behavior[4]: 0,\
                                          AppendUseItemString(behavior[1], 'days'): set(),\
                                          AppendUseItemString(behavior[2], 'days'): set(),\
                                          AppendUseItemString(behavior[3], 'days'): set(),\
                                          AppendUseItemString(behavior[4], 'days'): set()
                                        }
			    
		#更新用户特征
                one_user = user_dic[user_id]
                one_user[behavior_type] = one_user[behavior_type] + 1   #更新行为
                one_user[AppendUseItemString(behavior_type,'days')].add(b_time) #更新活跃度
                      
                #更新用户-品牌特征 （等待添加）
                use_good_id = AppendUseItemString(user_id, item_id)
                if user_good.has_key(use_good_id) is False :   #如果不存在键值，先创建一个键值
                    user_good[use_good_id] = {    behavior[1]: 0,\
                                                  behavior[2]: 0,\
                                                  behavior[3]: 0,\
                                                  behavior[4]: 0,\
                                                  user_good_feature_3days[1]:0,\
						  user_good_feature_3days[2]:0,\
						  user_good_feature_3days[3]:0,\
						  user_good_feature_3days[4]:0,\
                                                  user_good_feature_7days[1]:0,\
						  user_good_feature_7days[2]:0,\
						  user_good_feature_7days[3]:0,\
						  user_good_feature_7days[4]:0,\
                                             }
                one_user_good = user_good[use_good_id];
                one_user_good[behavior_type] = one_user_good[behavior_type] + 1
                # 更新前3天/前7天的情况
                if time_stamp - b_time <= days_feature[0] :
                    #print 'have record'
                    days_feature_name = user_good_days_feature_name[0]+"_"+behavior_type
                    one_user_good[days_feature_name] = one_user_good[days_feature_name] + 1
                if time_stamp - b_time <= days_feature[1] :
                    #print 'have record'
                    days_feature_name = user_good_days_feature_name[1]+"_"+behavior_type
                    one_user_good[days_feature_name] = one_user_good[days_feature_name] + 1
                '''
                if one_user_one_good.has_key(behavior_type) == True:
                    one_user_one_good_one_behavior = one_user_one_good[behavior_type]
                    one_user_one_good_one_behavior = one_user_one_good_one_behavior + [b_time]
                else:
                    one_user_one_good[behavior_type] = [b_time]
                else:
                    one_user[item_id] = {behavior_type:[b_time]}
                
                if test_user_dic.has_key(user_id) == True:
                    good = test_user_dic[user_id]
                    if good.has_key(item_id) != True:
                        good[item_id] = 1
                else:
                    test_user_dic[user_id] = {item_id:1}
                '''
            #加入分割点时间的tag
            #如果out_put_type  == 0 （trainSet）,利用cut_time当天的结果标记之前的TrainSet的tag
            elif out_put_type == 0 and  b_time == time_stamp :
                    if not use_item_result.has_key(AppendUseItemString(user_id, item_id)) :
                        result = False
                        if behavior_type == 'buy' :
                            tag_count = tag_count + 1
                        #    print 'buy'
                            result = True                        
                        use_item_result[AppendUseItemString(user_id, item_id)] = { 'tag' : result}
                    else :
                        if behavior_type == 'buy' and use_item_result[AppendUseItemString(user_id, item_id)]['tag'] is False :
                            tag_count = tag_count + 1
                            use_item_result[AppendUseItemString(user_id, item_id)] = { 'tag' : True }
    csvfile.close()
    print "read ok"
    print "All buy behavior : " + str(tag_count)
    ##############特征提取##################################################

    #确定标题       
    if out_put_type == 0 :
        Title = train_title
        output_file = output_train_file
    elif out_put_type == 1 :
        Title = predict_title
        output_file = output_vec_file
    
    writer = csv.writer(file(output_file,'wb'))
    writer.writerow(Title)

    count = 0
    tag2_count = 0
    tag3_count = 0
    if out_put_type == 0 :
        user_good_list = use_item_result
    elif out_put_type == 1 :
        user_good_list = user_good

    for user_good_key in user_good_list.keys() :
        array = user_good_key.split('-')
        user = array[0]
        good = array[1]
        # 没发生过行为的 && 超过一些 负样本边界条件的 都剔除掉
        if not user_good.has_key(user_good_key) :
            if use_item_result[user_good_key]['tag'] is True :
                tag2_count = tag2_count + 1
            continue;
        #V1.0
        good_feature = good_dic[good]
        user_feature = user_dic[user]					
        good_f1 = good_feature[behavior[4]]
        good_f2 = good_feature[behavior[3]]
        good_f3 = good_feature[days_featureName[0]]
        good_f3 = good_f3 * 1.0 * 10 / 500 #归一化处理
        #good_f4 = good_feature[days_featureName[1]]  #前7天结果和前3天一样，统计上可能是集合划分的问题，暂时先不用
        user_f1 = len(user_feature[AppendUseItemString(behavior[4], 'days')]) * 1.0 * ratio / (cut_time_stamp - start_time_stamp)
        user_f2 = user_feature[behavior[4]] * 1.0 * ratio / ( user_feature[behavior[1]] + user_feature[behavior[2]] + user_feature[behavior[3]] + user_feature[behavior[4]] )
	    
	#V2.0
        user_good_feature = user_good[user_good_key]
            					
        #未考虑正负样本抽样，正负样本比例先按照 1：5 来取
        if out_put_type == 0 :
            # 过滤掉光点不买的
            if user_good_feature[user_good_feature_7days[4]] == 0 and user_good_feature[user_good_feature_7days[1]] > 9 :
               continue;
            
            if (use_item_result[user_good_key]['tag'] is False) and (count == 10) :
                #writer.writerow([0, good_f1, good_f2, good_f3, good_f4, user_f1, user_f2])
                writer.writerow([0, user_good_feature[user_good_feature_3days[1]], user_good_feature[user_good_feature_3days[2]], user_good_feature[user_good_feature_3days[3]], user_good_feature[user_good_feature_3days[4]],\
                                 user_good_feature[user_good_feature_7days[1]], user_good_feature[user_good_feature_7days[2]], user_good_feature[user_good_feature_7days[3]], user_good_feature[user_good_feature_7days[4]]\
                               ])
                count = 0
            elif (use_item_result[user_good_key]['tag'] is False) and (count < 10) :
                count = count + 1
            elif use_item_result[user_good_key]['tag'] is True :
                tag3_count = tag3_count + 1
                writer.writerow([1, user_good_feature[user_good_feature_3days[1]], user_good_feature[user_good_feature_3days[2]], user_good_feature[user_good_feature_3days[3]], user_good_feature[user_good_feature_3days[4]],\
                                 user_good_feature[user_good_feature_7days[1]], user_good_feature[user_good_feature_7days[2]], user_good_feature[user_good_feature_7days[3]], user_good_feature[user_good_feature_7days[4]]\
                                ])
        elif out_put_type == 1 :
            writer.writerow([user, good, user_good_feature[user_good_feature_3days[1]], user_good_feature[user_good_feature_3days[2]], user_good_feature[user_good_feature_3days[3]], user_good_feature[user_good_feature_3days[4]],\
                             user_good_feature[user_good_feature_7days[1]], user_good_feature[user_good_feature_7days[2]], user_good_feature[user_good_feature_7days[3]], user_good_feature[user_good_feature_7days[4]]\
                            ])
    csvfile.close()
    print 'no feature records: ' + str(tag2_count)
    print 'have feature records: ' + str(tag3_count)
    print 'generate over'
    return
    
if __name__ == '__main__' :
    #GenerateFeature(0)
    GenerateFeature(0)
