# -*- coding: utf-8 -*-
import csv
import time
from collections import defaultdict
from sets import Set

#处理时间的字符串为 小时数
def AppendItems(user_id, item_id) :
        s = []
        s.append(user_id)
        s.append('-')
        s.append(item_id)
        item = ''.join(s)
        return item

def CalF1() :
        Ref_result = csv.DictReader(open('D:\\pythonCode\\chenlin\\sold_result\\2014-12-16result.csv'))
        Predict_result = csv.DictReader(open('D:\\pythonCode\\chenlin\\predict_result.csv'))
        '''
        # interaction size = |A + B| - |A| - |B|
        # then, using dict(a, **b) to speed up
        # can not do it -- as they are list of dictionarys
        Ref_size = len(Ref_result)
        Predict_size = len(Predict_result)
        All_size = len(dict(Ref_result, **Predict_result))
        Inter_size = Ref_size + Predict_size - Inter_size
        print Ref_size + "," + Predict_size + "," + Inter_size
        '''
        # using set to build hash and search
        Ref_set = Set()
        Predict_set = Set()
        Inter_size = 0
        for row in Ref_result :
                Ref_set.add(AppendItems(row['user_id'], row['item_id']))
        print '\n'
        for row in Predict_result :
                query = AppendItems(row['user_id'],row['item_id'])
                Predict_set.add(query)
                if(query in Ref_set) :
                        Inter_size = Inter_size + 1
        
        #Cal the F1       
        Ref_size = len(Ref_set)
        Predict_size = len(Predict_set)
        print Inter_size, Ref_size, Predict_size
        print "Precise: ",
        print Inter_size*1.0 / Predict_size
        print "Recal: ",
        print Inter_size*1.0 / Ref_size
        return (2 * Inter_size) * 1.0 / (Ref_size + Predict_size)

if __name__ == '__main__' :
	print CalF1()
