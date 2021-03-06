
import itertools
import sys
import time
import numpy as np
import pandas as pd

from pip._vendor.distlib.compat import raw_input

print("Welcome to apriori algorithms. \n Please choose the dataSet you want: \n 1. test \n 2. t2 \n 3. t3 \n 4. t4 \n 5. t5")
while True:
    choice_of_data=input()
    if(choice_of_data=='1'):
        data=pd.read_csv('test.txt')
        break
    elif(choice_of_data=='2'):
        data=pd.read_csv('t2.txt')
        break
    elif(choice_of_data=='3'):
        data=pd.read_csv('t3.txt')
        break
    elif(choice_of_data=='4'):
        data=pd.read_csv('t4.txt')
        break
    elif(choice_of_data=='5'):
        data=pd.read_csv('t5.txt')
        break
    else:
        print("Invalid data, please enter the valid data")
        break     

min_support = float(raw_input("Enter the minimum support - range(0-1): "))
min_confidence = float(raw_input("Enter the minimum confidence - range (0-1): "))
min_lift = float(raw_input("Enter the minimum lift (min_lift): "))

C1 = {}
transactions = 0
D = []
T = []

#def transactions(dataList):
    #Transactions = []
    #df_items = dataList['TransactionList']
    #comma_splitted_df = df_items.apply(lambda x: x.split(','))
    #for i in comma_splitted_df:
    #    Transactions.append(i)
    #return Transactions
    #load_transactions(dataList)
for line in data:
    T = []
    transactions += 1
    for word in line.split():
        T.append(word)
        if word not in C1.keys():
            C1[word] = 1
        else:
            count = C1[word]
            C1[word] = count + 1
    D.append(T)
    
#load_transactions(dataList)

#Transactions = load_transactions(dataList)
#Transactions

#with open("t2.txt", "r") as f:
#    for line in f:
#        T = []
#        transactions += 1
#        for word in line.split():
#            T.append(word)
#            if word not in C1.keys():
#                C1[word] = 1
#            else:
#                count = C1[word]
#                C1[word] = count + 1
#        D.append(T)

L1 = []
for key in C1:
    if (C1[key] / transactions) >= min_support:
        list = [key]
        L1.append(list)
print("----------------------FREQUENT 1-ITEMSET-------------------------")
print(L1)
print("-----------------------------------------------------------------")


def apriori_gen(Lk_1, k):
    length = k
    Ck = []
    for list1 in Lk_1:
        for list2 in Lk_1:
            count = 0
            c = []
            if list1 != list2:
                while count < length - 1:
                    if list1[count] != list2[count]:
                        break
                    else:
                        count += 1
                else:
                    if list1[length - 1] < list2[length - 1]:
                        for item in list1:
                            c.append(item)
                        c.append(list2[length - 1])
                        if not has_infrequent_subset(c, Lk_1, k):
                            Ck.append(c)
    return Ck


def find_subsets(c, k):
    return set(itertools.combinations(c, k))


def has_infrequent_subset(c, Lk_1, k):
    list = find_subsets(c, k)
    for item in list:
        s = []
        for l in item:
            s.append(l)
        s.sort()
        if s not in Lk_1:
            return True
    return False


def frequent_itemsets():
    k = 2
    Lk_1 = []
    L = []
    for item in L1:
        Lk_1.append(item)
    while Lk_1:
        Lk = []
        Ck = apriori_gen(Lk_1, k - 1)
        for c in Ck:
            count = 0
            transactions = 0
            s = set(c)
            for T in D:
                transactions += 1
                t = set(T)
                if s.issubset(t):
                    count += 1
            if (count / transactions) >= min_support:
                c.sort()
                Lk.append(c)
        Lk_1 = []
        print("----------------------FREQUENT %d-ITEMSET-------------------------" % k)
        print(Lk)
        print("------------------------------------------------------------------")
        for l in Lk:
            Lk_1.append(l)
        k += 1
        if Lk:
            L.append(Lk)

    return L


def generate_association_rules():
    num = 1
    L = frequent_itemsets()
    print("--------------------ASSOCIATION RULES-------------------")
    print("")
    print("RULE \t \t \t       SUPP      CONF      LIFT")
    print("--------------------------------------------------------")
    for itemset in L:
        for l in itemset:
            length = len(l)
            count = 1
            while count < length:
                r = find_subsets(l, count)
                count += 1
                for item in r:
                    T_supporting_A = 0
                    T_supporting_B = 0
                    T_supporting_AB = 0
                    s = []
                    m = []
                    for i in item:
                        s.append(i)
                    for T in D:
                        if set(s).issubset(set(T)):
                            T_supporting_A += 1
                            if set(l).issubset(set(T)):
                                T_supporting_AB += 1
                        if set(l).issubset(set(T)):
                            T_supporting_B += 1

                            suppAB = T_supporting_AB / len(D)
                            confAB = T_supporting_AB / T_supporting_A
                            liftAB = confAB / (T_supporting_B / len(D))

                    if confAB >= min_confidence and liftAB >= min_lift:
                        for index in l:
                            if index not in s:
                                m.append(index)

                        print("Rule #%d : %s ==> %s   %f  %f  %f" % (num, s, m, suppAB, confAB, liftAB))
                        num += 1


generate_association_rules()

print("--------------------------------------------------------")