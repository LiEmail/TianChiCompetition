# -*- coding: cp936 -*-
import csv
import time

dir = 'D:\\TianChi\\'
cut_day = '2014-12-18'
feature_day = ['20141217','20141216','20141215']
input_file_result_file = dir + 'sold_result\\'+cut_day+'result.csv'
#input_user_file = dir + 'tianchi_mobile_recommend_train_user.csv'
input_user_file = dir + 'row_record.csv'

#时间戳转化成天数
def date2hours(date):
    test_time_array = time.strptime(date,'%Y-%m-%d %H')
    hours_i = int((time.mktime(test_time_array))/(3600))
    return hours_i
    #days_f = float((time.mktime(test_time_array))/(3600)
    #if(days_f - days_i) > 0.66 : 
    #    return days_i + 1
    #else:
    #    return days_i
	
#形成 userid_itemid串，用于匹配target
def AppendUseItemString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

def GetDupRatio() :
	#得到购买的 用户-物品对
	buy_user_item_dic = set() #购买记录
	with open(input_file_result_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	       if	AppendUseItemString(row['user_id'],row['item_id']) in buy_user_item_dic :
	           continue
	       else :
	           buy_user_item_dic.add(AppendUseItemString(row['user_id'],row['item_id']))
	
	#统计3天之内，按6小时为界的总情况
	user_item_dic = set ()
	dup_item_dic = set ()
	with open(input_user_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader : 
	        index = AppendUseItemString(row['user_id'],row['item_id'])
	        if index in buy_user_item_dic : 
	               if index in buy_user_item_dic : 
	                   dup_item_dic.add(index)
	               else :  
	                   user_item_dic.add(index)

	buy_len = len(buy_user_item_dic)
	print 'All_buy ' + str(buy_len)
	print 'Dup Ratio ' + str(len(dup_item_dic) * 100.0 / len(buy_user_item_dic)) 
			
        '''
	#生成分割日期集    
        if(split_date != null && !split_date.equals("null")){
            //转换为小时
            String[] ls = split_date.split("-");
            if(ls != null ){
                //假设month只为12
                int month = Integer.parseInt(ls[0]);
                int day = Integer.parseInt(ls[1]);
                //也就是说,运行一遍该程序也会同时产生用于预测19号数据的特征文件(即包含12-18的交易记录)
                while(day < 20){
                    long hour = 0;
                    if(month == 11){
                        hour = (day - 18) * 24;
                    }
                    else if(month == 12){
                        hour = 13 * 24 + (day - 1) * 24;
                    }
                    split_dates.put(hour,ls[0] + ls[1]);
                    split_dates_ordered.add(hour);
                    day++;
                }
            }
        }
	'''
def Alth() :
	#得到购买的 用户-物品对
	buy_user_item_dic = set() #购买记录
	with open(input_file_result_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	       if	AppendUseItemString(row['user_id'],row['item_id']) in buy_user_item_dic :
	           continue
	       else :
	           buy_user_item_dic.add(AppendUseItemString(row['user_id'],row['item_id']))
	
	#统计3天之内，按6小时为界的总情况
	user_item_dic = set ()
	dup_item_dic = set ()
	with open(input_user_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader : 
	        index = AppendUseItemString(row['user_id'],row['item_id'])
	        if index in buy_user_item_dic : 
	               if index in buy_user_item_dic : 
	                   dup_item_dic.add(index)
	               else :  
	                   user_item_dic.add(index)

	buy_len = len(buy_user_item_dic)
	print 'All_buy ' + str(buy_len)
	print 'Dup Ratio ' + str(len(dup_item_dic) * 100.0 / len(buy_user_item_dic)) 


if __name__ == '__main__' :
        #GetDupRatio()
