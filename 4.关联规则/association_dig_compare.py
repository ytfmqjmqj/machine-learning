#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 22:51:13 2019

@author: xuganggang
"""

# 1.Apriori算法中的辅助函数
# 创建1-候选项集列表
def create_C1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

# 由候选项集列表Ck创建频繁项集列表Lk和相应的支持度字典
def scanD(D, Ck, minSupport):
    to_be_chosen = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in to_be_chosen:
                    to_be_chosen[can] = 1
                else:
                    to_be_chosen[can] += 1
    num_Items = len(D)
    ret_List = []
    support_Data = {}
    for key in to_be_chosen:
        support = to_be_chosen[key] / num_Items
        if support >= minSupport:
            ret_List.insert(0, key)
            support_Data[key] = support
    return ret_List, support_Data

# 2.Apriori算法
# 创建候选项集列表Ck
def aprioriGen(Lk, k):
    ret_List = []
    len_Lk = len(Lk)
    for i in range(len_Lk):
        for j in range(i + 1, len_Lk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                ret_List.append(Lk[i] | Lk[j])
    return ret_List

# 由数据集和最小支持度得到所有的频繁项集和相应的支持度字典
def apriori(dataSet, minSupport = 0.5):
    C1 = create_C1(dataSet)
    D = list(map(set, dataSet))
    L1, support_Data = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        support_Data.update(supK)
        L.append(Lk)
        k += 1
    return L, support_Data


# 3.关联规则生成函数
# 对规则进行评估，看其是否满足最小可信度要求
def calc_Conf(freqSet, H, support_Data, br1, minConf = 0.7):
    prunedH = []
    for conseq in H:
        conf = support_Data[freqSet] / support_Data[freqSet - conseq]
        if conf >= minConf:
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

# 频繁项集元素数目超过2，对它做进一步的合并
def rules_From_Conseq(freq_Set, H, support_Data, br1, minConf = 0.7):
    m = len(H[0])
    if len(freq_Set) > (m + 1):
        calc_Conf(freq_Set, H, support_Data, br1, minConf)
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_Conf(freq_Set, Hmp1, support_Data, br1, minConf)
        if len(Hmp1) > 1:
            rules_From_Conseq(freq_Set, Hmp1, support_Data, br1, minConf)

# 由所有频繁项集、相应的支持度字典和最小可信度生成规则列表
def generate_Rules(L, supportData, minConf = 0.7):
    big_Rule_List = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rules_From_Conseq(freqSet, H1, supportData, big_Rule_List, minConf)
            else:
                calc_Conf(freqSet, H1, supportData, big_Rule_List, minConf)
    return big_Rule_List

L, suppData = apriori(dataSet)
#mush_DatSet = [line.split() for line in open('mushroom.dat').readlines()]
## 数据类型由字符型转换为整型
#for i in range(len(mush_DatSet)):
#    mush_DatSet[i] = list(map(int, mush_DatSet[i]))

# 使用算法
#while True:
#    try:
#        min_Support_Conf = input('请输入最小支持度(<=0.4)和最小可信度,用空格隔开，回车结束')
#        minSupport, minConf = list(map(float, min_Support_Conf.split()))
#        L, supp_Data = apriori(mush_DatSet, minSupport)
#        rules = generate_Rules(L, supp_Data, minConf)
#        poison_List = []
#        for rule in rules:
#            if rule[1] == {2}:
#                poison_List.append(rule)
#        poison_List.sort(key = lambda x: x[2], reverse = True)
#        for poison_Rule in poison_List:
#            print(poison_Rule)
#    except:
#        break