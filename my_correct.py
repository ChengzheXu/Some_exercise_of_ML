from tkinter.filedialog import askopenfilename
import re
import math
from collections import Counter
letters = 'abcdefghijklmnopqrstuvwxyz'
librarydictionary = {1:'news.txt',2:'relax.txt',3:'health.txt',4:'science.txt',5:'life.txt',\
                     6:'work.txt',7:'study.txt',8:'sports.txt',9:'food.txt',10:'tour.txt',11:'others.txt'}
def CreateDictionary(library):
    '''传入库字符串并生成字典。'''
    libdict = Counter(re.findall('\w+',library.lower))
    global libdict
def Correct(inputword,Pminwrong):
    '''假设拼错单词的字母是彼此独立的,拼错概率为1/e,传入单词inputword，根据字典libdict以及精度值Pminwrong返回矫正单词。'''
    if inputword.lower() in libdict.keys():
        correctdict = {}
    else:
        factor_one_list = [correctword for correctword in Factor_one(inputword.lower) if correctword in libdict]
        factor_two_list = [correctword for correctword in Factor_two(inputword.lower) if correctword in libdict]
        factor_three_list = [correctword for correctword in Factor_three(inputword.lower) if correctword in libdict]
        output = []
        Poutput = []
        for standword in libdict:
            p = math.exp(-1*math.fabs(len(inputword.lower)-len(standword)))*libdict[standword]
            if p < Pminwrong:
                continue
            else:
                p = math.exp(-Worddefferfactor(standword,factor_one_list,factor_two_list,factor_three_list))\
                    *libdict[standword]
            if p < Pminwrong:
                continue
            else:
                output.append(standword)
                Poutput.append(p)
        else:
            correctdict = dict(zip(output,Poutput))
    if not correctdict:
        outputword = inputword
    else:
        for outputword in correctdict.keys():
            if correctdict[outputword] == max(correctdict.values()):
                break
    return outputword
def Extendlibrary():
    select = int(input('''请选择所要更新的库文件：
    1：新闻类；
    2：休闲类；
    3：健康类；
    4：科技类；
    5：生活类；
    6：工作类；
    7：学习类；
    8：体育运动类；
    9：美食类；
    10：旅游类；
    11：其他。\n'''))
    print("请选择更新文件（txt）。\n")
    with open(askopenfilename(),'r') as newsoursefile:
        newsourse = ' '.join(re.findall('\w+',newsoursefile.read()))
    if select == 1:
        with open('news.txt','a') as newslibrary:
            newslibrary.write(newsourse)
    elif select == 2:
        with open('relax.txt','a') as relaxlibrary:
            relaxlibrary.write(newsourse)
    elif select == 3:
        with open('health.txt','a') as healthlibrary:
            healthlibrary.write(newsourse)
    elif select == 4:
        with open('science.txt','a') as sciencelibrary:
            sciencelibrary.write(newsourse)
    elif select == 5:
        with open('life.txt','a') as lifelibrary:
            lifelibrary.write(newsourse)
    elif select == 6:
        with open('work.txt','a') as worklibrary:
            worklibrary.write(newsourse)
    elif select == 7:
        with open('study.txt','a') as studylibrary:
            studylibrary.write(newsourse)
    elif select == 8:
        with open('sports.txt','a') as sportslibrary:
            sportslibrary.write(newsourse)
    elif select == 9:
        with open('food.txt','a') as foodlibrary:
            foodlibrary.write(newsourse)
    elif select == 10:
        with open('tour.txt','a') as tourlibrary:
            tourlibrary.write(newsourse)
    else:
        with open('others.txt', 'a') as otherslibrary:
            otherslibrary.write(newsourse)
    print("更新成功！\n")
    return None
def Worddefferfactor(standword,factor_one_list,factor_two_list,factor_three_list):
    '''假设不可能出现四个/对字母以上(含)的错误，且错误的出现彼此独立，而且概率均为1/e。'''
    if standword in factor_one_list:
        return 1
    elif standword in factor_two_list:
        return 2
    elif standword in factor_three_list:
        return 3
    else:
        return 10
def Factor_one(word):
    splits = [(word[:i:], word[i::]) for i in range(len(word) + 1)]
    deletes = [L + R[1::] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2::] for L, R in splits if len(R) > 1]
    replace = [L + c + R[1::] for L, R in splits if R for c in letters]
    insert = [L + c + R for L, R in splits for c in letters]
    return deletes + transposes + replace + insert
def Factor_two(word):
    return list(set([word2 for word1 in Factor_one(word) for word2 in Factor_one(word1)]))
def Factor_three(word):
    return list(set([word3 for word2 in Factor_two(word) for word3 in Factor_one(word2)]))
def main():
    if int(input("是否更新库文件？(1 for 是，0 for 否）\n")):
        Extendlibrary()
    try:
        select = int(input("请选择单词矫正的文章背景。\n"))
        with open(librarydictionary[select],'r') as library:
            CreateDictionary(library.read())
    except:
        print("非法输入！\n")
        exit(0)
    correctword = Correct(input("请输入单词："),eval(input("请输入最小允许概率(小于该概率，将被认为为不可能发生)：")))
    print("修正后的单词为：{0}\n".format(correctword))
    return None
