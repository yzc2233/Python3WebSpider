import collections
import re
import sys
import json
import os

def convertArgus(Request):
    dict = Request
    pattern = re.compile('"(\w*?)":.*?[,|}]')
    match = pattern.findall(dict)

    Argus = collections.OrderedDict()
    Argument = ''
    for key in match:
        v = '${' + key + '}    '
        v1 = '${' + key + '}'
        # print(v,end='')
        Argus[key] = v1
        Argument = Argument + v
    print(Argument)
    print('\n\n')

    ArgusBody = ''
    for key,value in Argus.items():
        ArgusBody = ArgusBody +'"' + key + '":' + '"' + value +'",'
        # print('"' + key + '":' + '"' + value +'",',end='')
    ArgusBody = '{' + ArgusBody[:-1] + '}'

    print(ArgusBody)

# req ={"activityId":"737483909","bookDate":"2021-04-09","bookTime":"14:00-14:15","customerName":"AutoTest","customerRemarks":"AutoTestMemo","openId"
# :"ojmVG4xoByjqcm7AEAYk8IUpdpZw","phoneNum":"12345678901","storeId":"9909"}
#
# convertArgus(req)


if __name__ == '__main__':
    filepath = os.path.join(os.getcwd(),'RequestParams.txt')
    with open(filepath,'r') as f:
        req = f.readline()
    convertArgus(req)


