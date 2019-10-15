import random

def Create_lotto(times):
    CreateNumberList = []
    redrange = list(range(1,36))
    bluerange = list(range(1,13))
    for i in range(0,times):
        redlist = random.sample(redrange,5)
        bluelist = random.sample(bluerange,2)
        redlist.sort()
        bluelist.sort()
        lottocode = '{:0>2d} {:0>2d} {:0>2d} {:0>2d} {:0>2d}    {:0>2d} {:0>2d}'.format(redlist[0],redlist[1],redlist[2],redlist[3],redlist[4],bluelist[0],bluelist[1])
        CreateNumberList.append(lottocode)
    # print(CreateNumberList)
    return CreateNumberList
