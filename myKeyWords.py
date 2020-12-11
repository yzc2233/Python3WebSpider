#coding=utf-8
import os
import requests
import sys
import GetIP
import time
import json
import datetime

try:
    import pymysql
except:
    print('pymysql模块未安装，现在开始安装')
    os.system('pip install pymysql')
    import pymysql

try:
    import configparser
except:
    print('configparser模块未安装，现在开始安装')
    os.system('pip install configparser')
    import configparser

config =configparser.ConfigParser()
config.read('properties.conf')

allowedenv = config.get('allowedenv','allowedenv')
allowedenv = allowedenv.split(',')



def createNewOrdercheckInputArgus(skuNumberLimit='3'):
    skuIdlist = []
    inputargvlength = len(sys.argv)
    if inputargvlength < 3:
        print('请输入完整的请求至少包含：需要执行的文件 执行环境 用户uid，example：python CreateNewOrder.py qa2 2001844981 \n','需在文件目录下执行命令')
        exit()
    elif inputargvlength >= 3:
        env = sys.argv[1].lower()
        if env not in allowedenv:
            print('输入的环境 %s 有误，仅支持qa2及stage环境！' %env)
            exit()
        mysqlhost = config['mysql_'+ env]['host']
        mysqluser = config['mysql_'+ env]['user']
        mysqlpassword = config['mysql_'+ env]['password']
        uid = sys.argv[2]
        try:
            uid = int(uid)
            uid = str(uid)
        except ValueError as e:
            print('输入的用户uid：%s 格式错误' %uid)
            exit()
        defaultskuId = [config['skuId'][env + '_skuId']]
        if inputargvlength > 3:
            for arg in sys.argv[3:]:
                try:
                    skuIdlist.append(int(arg))
                except ValueError:
                    print('输入的skuId集合中 %s 格式错误！' %arg)
                    exit()
        elif inputargvlength == 3:
            skuIdlist = getskuIdlist(mysqlhost,mysqluser,mysqlpassword,skuNumberLimit)
        else:
            skuIdlist = defaultskuId
        return env,uid,skuIdlist,mysqlhost,mysqluser,mysqlpassword

def getskuIdlist(mysqlhost,mysqluser,mysqlpassword,skuNumberLimit):
    print('-'*20,'开始数据库随机获取两个skuId，请稍作等待','-'*20)
    datalist = []
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'product')
    cur = conn.cursor()
    sql = "select b.sku_id from prod_product a LEFT JOIN prod_sku b on a.id=b.product_id where a.`status`=1 and b.`status`=1 and b.sku_type=1  and b.sale_channel->'$[0]'='ALL' order by RAND() limit "+str(skuNumberLimit)+';'
    cur.execute(sql)
    data = cur.fetchall()
    for da in data:
        datalist.append(da[0])
    print('获取到的skuId的集合是 %s' %datalist)
    print('-'*20,'数据库获取随机两个skuId结束','-'*20,'\n\n')
    cur.close()
    return datalist


def addToCartForSingleProduct(ShopCart_IP,uid,skuId,quantity=2):
    print('-'*20,'开始添加单个商品至购物车','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"channel":"PC","checked":1,"quantity":quantity,"skuId":skuId,"type":1}}
    addproduct_url = ShopCart_IP + '/v1/shopcart/shopcart/addToCartForSingleProduct'
    req = requests.post(addproduct_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] <=0:
        print('添加单个商品%s至购物车失败：%s' %(skuId,response))
        exit()
    else:
        print('添加单个商品%s至购物车成功' %skuId)
    print('-'*20,'添加单个商品至购物车结束','-'*20 ,'\n\n')

def getShopcartStepTwo(ShopCart_IP,uid):
    print('-'*20,'开始购物车第二步','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"orderType":"1","channel":"PC"}}
    ShopcartStepTwo_url = ShopCart_IP + '/v1/shopcart/shopcart/getShopcartStepTwo'
    req = requests.post(ShopcartStepTwo_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None:
        print('购物车第二步失败',response)
        exit()
    else:
        print('购物车第二步成功')
    print('-'*20,'开始购物车第二步结束','-'*20 ,'\n\n')

def clearShopcartSkuId(ShopCart_IP,uid,skuId):
    print('-'*20,'开始清除购物车指定商品','-'*20)
    skuId = str(skuId)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"head":{"token":"string","userId":"string"},"queryBody":[{"skuId":skuId,"type":1,"userId":uid}]}
    clearShopcartSkuId_url = ShopCart_IP + '/v1/shopcart/shopcart/removeFromCart'
    req = requests.post(clearShopcartSkuId_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None:
        print('清除购物车指定商品%s失败 %s'%(skuId,response))
        exit()
    else:
        print('清除购物车指定商品%s成功' %skuId)
    print('-'*20,'清除购物车指定商品结束','-'*20 ,'\n\n')

def changePayment(ShopCart_IP,uid):
    print('-'*20,'开始修改支付方式','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"payMethod":"COD","type":"1"}}
    changePayment_url = ShopCart_IP + '/v1/shopcart/payment/changePayment'
    req = requests.put(changePayment_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['status'] != 'SUCCESS':
        print('修改支付方式失败',response)
        exit()
    else:
        print('修改支付方式成功')
    print('-'*20,'修改支付方式结束','-'*20 ,'\n\n')

def addOrders(ShopCart_IP,uid,skuIdlist):
    print('-'*20,'开始提交订单','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"channel":"PC","type":1,"firstOrderSource":{"utm_source":"samsung","utm_medium":"referral","utm_campaign":"bixby","utm_content":"undefined","utm_term":"undefined"}}}
    addOrders_url = ShopCart_IP + '/v1/shopcart/order/addOrders'
    req = requests.post(addOrders_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['resultStatus'] != 'SUCCESS':
        print('提交订单失败',response)
        #清除购物车
        # for skuId in skuIdlist:
        #     time.sleep(1)
        #     clearShopcartSkuId(ShopCart_IP,uid,skuId)
        # print('\n创建订单失败')
        clearCartAll(ShopCart_IP,uid)
        exit()
    else:
        orderId = response['results']['orderId']
        print('提交订单成功，订单号：',orderId)
        print('-'*20,'提交订单结束','-'*20 ,'\n\n')
        return orderId

def addOrdersV3(ShopCart_IP,uid,skuIdlist,addressId):
    print('-'*20,'开始提交订单','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"addressId":addressId,"comments":None,"giftComments":None,"payMethod":"ONLINE_PAY","type":1,"deliveryInfo":"1","channel":"PC","firstOrderSource":{"utm_source":"ebtrgremail","utm_medium":"ecrm","utm_campaign":"edm_ebsystem_password","utm_content":"undefined","utm_term":"undefined"}}}
    addOrders_url = ShopCart_IP + '/v3/shopcart/order/commitOrderExtend'
    req = requests.post(addOrders_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['resultStatus'] != 'SUCCESS':
        print('提交订单失败',response)
        #清除购物车
        # for skuId in skuIdlist:
        #     time.sleep(1)
        #     clearShopcartSkuId(ShopCart_IP,uid,skuId)
        # print('\n创建订单失败')
        clearCartAll(ShopCart_IP,uid)
        exit()
    else:
        orderId = response['results']['orderId']
        print('提交订单成功，订单号：',orderId)
        print('-'*20,'提交订单结束','-'*20 ,'\n\n')
        return orderId

def getaddressIdByUid(mysqlhost,mysqluser,mysqlpassword,uid):
    print('-'*20,'开始获取收货地址','-'*20)
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'shopcart')
    cur = con.cursor()
    sql = r"select addr_id from addr_cneeinfo where user_id={0} and status='E' order by is_default desc,create_time desc limit 1;".format(uid)
    cur.execute(sql)
    data = cur.fetchall()
    if data:
        addressId = data[0][0]
    print('-'*20,'获取收货地址结束','-'*20,'\n\n')
    return addressId

def orderSync(Order_IP,orderId):
    print('-'*20,'开始推送订单至OMS并索引至elasticSearch','-'*20)
    orderSync_url = Order_IP + '/v1/order/orderSync/orderSync/' + orderId
    req = requests.get(orderSync_url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('推送订单至OMS并索引至elasticSearch失败:',response)
        # exit()
    else:
        print('推送订单至OMS并索引至elasticSearch成功')
    print('-'*20,'推送订单至OMS并索引至elasticSearch结束','-'*20 ,'\n\n')

def forwadOnehour(mysqlhost,mysqluser,mysqlpassword,orderId):
    print('-'*20,'开始将订单提前一小时','-'*20)
    # 连接数据库
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'order')
    # 得到一个可执行的光标对象
    cursor = conn.cursor()
    # 定义要执行的额SQL语句
    print('查询订单号为 %s 的订单记录' %orderId)
    sql = "select * from orders where order_id="+"'"+orderId+"';"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    if not data:
        print('未找到订单号为 %s 的记录' %orderId)
        exit()
    print('数据库开始将订单号为 %s 的订单记录创建时间提前一小时' %orderId)
    updatesql = "update orders set create_time=DATE_SUB(create_time ,INTERVAL 1 HOUR) where order_id="+"'"+orderId+"';"
    print(updatesql)
    try :
        # 执行更新语句
        cursor.execute(updatesql)
        # 提交到数据库执行
        conn.commit()
        print('数据库开始将订单号为 %s 的订单记录创建时间提前一小时成功' %orderId)
        time.sleep(3)
    except:
        # 发生错误时回滚
        conn.rollback()
        print('数据库开始将订单号为 %s 的订单记录创建时间提前一小时失败' %orderId)
        exit()
    finally:
        cursor.close()
        print('-'*20,'将订单提前一小时结束','-'*20 ,'\n\n')

def getSkuIdList2SkuCodelist(mysqlhost,mysqluser,mysqlpassword,skuIdList):
    skuCodeList = []
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'product')
    cur = con.cursor()
    for skuId in skuIdList:
        sql = 'select sku_code from prod_sku where sku_id= '+str(skuId)+';'
        cur.execute(sql)
        data = cur.fetchall()
        skuCodeList.append(data[0][0])
    return skuCodeList

def CreateNewOrder():
    print('仅支持Python3环境')

    env,uid,skuIdlist,mysqlhost,mysqluser,mysqlpassword = createNewOrdercheckInputArgus(2)
    ShopCart_IP = GetIP.getIp(env,'shop-cart')
    Order_IP = GetIP.getIp(env,'sephora-order-service')
    PIM_IP = GetIP.getIp(env,'pim')
    OMS_IP = GetIP.getIp(env,'OMS')

    #更新库存
    skuCodeList = getSkuIdList2SkuCodelist(mysqlhost,mysqluser,mysqlpassword,skuIdlist)
    updateInventory(PIM_IP,skuCodeList)
    time.sleep(3)

    ## 循环添加单个商品至购物车
    for sku in skuIdlist:
        addToCartForSingleProduct(ShopCart_IP,uid,sku,3)

    ## 购物车第二步
    getShopcartStepTwo(ShopCart_IP,uid)

    ## 修改支付方式
    changePayment(ShopCart_IP,uid)

    #获取收货地址
    addressId = getaddressIdByUid(mysqlhost,mysqluser,mysqlpassword,uid)
    if not addressId:
        print('未找到收货地址，请设置！')
        exit()

    ## 提交订单
    # orderId = addOrders(ShopCart_IP,uid,skuIdlist)
    orderId = addOrdersV3(ShopCart_IP,uid,skuIdlist,addressId)
    time.sleep(3)

    ## 将订单提前一小时
    forwadOnehour(mysqlhost,mysqluser,mysqlpassword,orderId)

    ## 推送订单至OMS并索引至elasticSearch
    orderSync(Order_IP,orderId)

    ##OMS处理订单流程
    dealNormalOrderOMSProcess(OMS_IP,mysqlhost,mysqluser,mysqlpassword,orderId)

    print('%s环境创建处理中订单成功，订单号：%s\n' %(env,orderId))
    return orderId


def get_SalesOrderStatus(mysqlhost,mysqluser,mysqlpassword,orderId):
    print('-'*20,'开始获取sales_order中订单状态','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "select a.ORDER_INTERNAL_STATUS,a.TYPE,a.SALES_ORDER_SYS_ID from sales_order a where a.SALES_ORDER_NUMBER="+ "'" + orderId + "';"
    print(sql)
    try:
        cur.execute(sql)
        data = cur.fetchone()
        ORDER_INTERNAL_STATUS = data[0]
        SALES_ORDER_SYS_ID = data[2]
        print('成功获取sales_order中订单状态 %s,orderSysId= %s' %(ORDER_INTERNAL_STATUS,SALES_ORDER_SYS_ID))
        return ORDER_INTERNAL_STATUS,SALES_ORDER_SYS_ID
    except:
        print('获取sales_order中订单状态失败')
        cur.close()
        exit()
    finally:
        cur.close()
    print('-'*20,'获取sales_order中订单状态结束','-'*20 ,'\n\n')

def dealPending(OMS_IP):
    print('-'*20,'开始处理Pending状态订单','-'*20)
    url = OMS_IP + '/job/exec/orders?th=omsPendingOrdersJob'
    req = requests.get(url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('处理Pending状态订单失败:',response)
        exit()
    else:
        for step in range(0,45,3):
            print('等待3s')
            time.sleep(3)
        print('处理Pending状态订单成功')
    print('-'*20,'处理Pending状态订单结束','-'*20 ,'\n\n')

def dealException(OMS_IP,orderSysId):
    print('-'*20,'开始处理Exception状态订单','-'*20)
    url = OMS_IP+'/v1/oms/order/exception/status/close?orderSysId='+str(orderSysId)+'&comment=undefined&orderFrom=SO'
    req = requests.post(url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('处理Exception状态订单失败:',response)
        exit()
    else:
        for step in range(0,24,3):
            print('等待3s')
            time.sleep(3)
        print('处理Exception状态订单成功')
    print('-'*20,'处理Exception状态订单结束','-'*20 ,'\n\n')

def dealWaitSend(sec):
    print('-'*20,'开始处理WAIT_SEND_SAP状态订单','-'*20)
    for step in range(0,sec,3):
        print('等待3s')
        time.sleep(3)
    print('-'*20,'处理Exception状态订单结束','-'*20 ,'\n\n')

def getPurchaseOrder(mysqlhost,mysqluser,mysqlpassword,orderId):
    print('-'*20,'开始获取purchase_order对应订单记录','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "select a.PURCHASE_ORDER_NUMBER,a.SIGN_TIME,a.ORDER_INTERNAL_STATUS  from purchase_order a where a.SALES_ORDER_NUMBER=" + "'" + orderId + "';"
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    if len(data):
        print('成功获取purchase_order对应订单记录\n %s' %str(data))
        return data
    else:
        print('获取purchase_order对应订单记录失败，未获取到相应记录')
        cur.close()
        exit()
    cur.close()
    print('-'*20,'获取purchase_order对应订单记录结束','-'*20 ,'\n\n')

def IsSplit(data):
    data = list(data)
    IsSplit = False
    if len(data) > 1:
        IsSplit = True
    return IsSplit

def updateOrder_NotSpilt(mysqlhost,mysqluser,mysqlpassword,data,orderId,signTime):
    print('-'*20,'开始非拆单情况下更新订单数据','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    # sql = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+data[0][0]+"';"
    sql = ("update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='%s' where PURCHASE_ORDER_NUMBER='%s';" %(signTime,data[0][0]))
    sql2  = "update sales_order set ORDER_INTERNAL_STATUS='SIGNED' where  SALES_ORDER_NUMBER="+"'"+orderId+"';"
    try:
        cur.execute(sql)
        print(sql)
        cur.execute(sql2)
        print(sql2)
        conn.commit()
        print('非拆单情况下更新订单数据成功')
    except:
        conn.rollback()
        print('非拆单情况下更新订单数据失败')
        cur.close()
        exit()
    finally:
        cur.close()
    print('-'*20,'非拆单情况下更新订单数据结束','-'*20 ,'\n\n')

def updateOrder_IsSpilt(mysqlhost,mysqluser,mysqlpassword,data,orderId,signTime):
    print('-'*20,'开始拆单情况下更新订单数据','-'*20)
    length = len(data)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    # sql = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED/SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+data[0][0]+"';"
    sql = ("update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED/SIGNED',SIGN_TIME='%s' where PURCHASE_ORDER_NUMBER='%s';" %(signTime,data[0][0]))
    sql2  = "update sales_order set ORDER_INTERNAL_STATUS='SIGNED/SIGNED' where  SALES_ORDER_NUMBER="+"'"+orderId+"';"
    try:
        for i in range(1,length):
            # sql3 = updatepurchase_sql3 = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+data[i][0]+"';"
            sql3 =  ("update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='%s' where PURCHASE_ORDER_NUMBER='%s';"  %(signTime,data[i][0]))
            cur.execute(sql3)
            print(sql3)
        cur.execute(sql)
        print(sql)
        cur.execute(sql2)
        print(sql2)
        conn.commit()
        print('拆单情况下更新订单数据成功')
    except:
        conn.rollback()
        print('拆单情况下更新订单数据失败')
        cur.close()
        exit()
    finally:
        cur.close()
    print('-'*20,'拆单情况下更新订单数据结束','-'*20 ,'\n\n')

def orderStatusSync(Order_IP,uid,orderId,orderStatus='DELIVERED'):
    print('-'*20,'开始修改订单状态','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"head":{"token":"string","userId":"string"},"queryBody":[{"orderNo":orderId,"orderStatus":orderStatus,"orderType":"NORMAL"}]}
    orderStatusSync_url = Order_IP + '/v1/order/orderSync/orderStatusSync'
    req = requests.put(orderStatusSync_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['info'] != '成功':
        print('修改订单状态失败',response)
        exit()
    else:
        print('修改订单状态成功')
        print('-'*20,'修改订单状态结束','-'*20 ,'\n\n')
        return orderId

def dealNormalOrderOMSProcess(OMS_IP,mysqlhost,mysqluser,mysqlpassword,orderId):
    dealflag = True
    waitTimes = 0
    while dealflag and waitTimes < 5:
        # 获取sales_order中订单状态
        OrderStatus,orderSysId = get_SalesOrderStatus(mysqlhost,mysqluser,mysqlpassword,orderId)
        if OrderStatus == 'PENDING':
            dealPending(OMS_IP)
            waitTimes += 1
        elif OrderStatus == 'EXCEPTION':
            dealException(OMS_IP,orderSysId)
        elif OrderStatus == 'PENDING_MIDDLE':
            dealWaitSend(30)
            print('等待3s')
            waitTimes += 1
        elif OrderStatus == 'WAIT_SEND_SAP' or OrderStatus == 'WAIT_ROUTE_ORDER':
            dealWaitSend(30)
            waitTimes += 1
        elif OrderStatus == 'WAIT_SAPPROCESS' or OrderStatus == 'WAIT_SAPPROCESS/WAIT_SAPPROCESS':
            dealflag = False
        elif OrderStatus == 'SIGNED' or OrderStatus == 'SIGNED/SIGNED':
            print('订单已经是已签收状态')
            exit()
        else:
            time.sleep(5)
            waitTimes += 1
        if waitTimes >= 5:
            print('已等待五次还未处理成功，目前订单%s 状态是%s' %(orderId,OrderStatus))
            exit()

def modifyFullPreSaleOrderEstimatedDeliveryTime(mysqlhost,mysqluser,mysqlpassword,orderId):
    con = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'orders')
    cur = con.cursor()
    sql = "select order_type from orders where order_id=" + "'" + str(orderId) + "'"
    print(sql)
    cur.execute(sql)
    data = cur.fetchone()
    oneDayBeforedate = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    if data == 3:
        con2 = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'orders')
        cur2 = con2.cursor()
        sql2 = 'update purchase_order set ORDER_SHIPPING_TIME=' +"'" +str(oneDayBeforedate) + "'" + 'where SALES_ORDER_NUMBER=' + "'" +str(orderId) + "';"
        con2.close()
    con.close()




##创建已签收订单
def UpdateOrderDelivered():
    env = sys.argv[1]
    # env = 'qa2'
    uid = sys.argv[2]
    # uid = '2000000070'

    OMS_IP = GetIP.getIp(env,'oms')
    Order_IP = GetIP.getIp(env,'sephora-order-service')

    mysqlhost = config['mysql_'+ env]['host']
    mysqluser = config['mysql_'+ env]['user']
    mysqlpassword = config['mysql_'+ env]['password']

    signTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    inputargvlength = len(sys.argv)
    if inputargvlength == 3:
        orderId = CreateNewOrder()
    elif inputargvlength == 4:
        orderId = sys.argv[3]

    orderId = str(orderId)

    ## 将订单提前一小时
    # forwadOnehour(mysqlhost,mysqluser,mysqlpassword,orderId)
    #
    # ## 推送订单至OMS并索引至elasticSearch
    # orderSync(Order_IP,orderId)
    #
    # # 处理订单状态至WAIT_SAPPROCESS
    # dealNormalOrderOMSProcess(OMS_IP,mysqlhost,mysqluser,mysqlpassword,orderId)

    # 获取purchase_order对应订单记录
    data = getPurchaseOrder(mysqlhost,mysqluser,mysqlpassword,orderId)
    #判断是否拆单
    splitFlag = IsSplit(data)
    if splitFlag:
        #拆单情况下更新数据库对应记录
        updateOrder_IsSpilt(mysqlhost,mysqluser,mysqlpassword,data,orderId,signTime)
    else:
        #未拆单情况下更新数据库对应记录
        updateOrder_NotSpilt(mysqlhost,mysqluser,mysqlpassword,data,orderId,signTime)
    #修改订单状态
    orderStatusSync(Order_IP,uid,orderId)
    print('%s环境已生成已签收订单：%s' % (env,orderId))




def dbGetSku(mysqlhost,mysqluser,mysqlpassword,skuType='1'):
    # print('-'*20,'数据库查询商品开始','-'*20)
    skuInfoList = []
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'product')
    cur = conn.cursor()
    if skuType == '1':
        vbsql = ''
    elif skuType == '6':
        vbsql = ' and (select 1 from prod_vb_sku_rel c where c.vb_sku_id=b.sku_id and c.vb_sku_code=b.sku_code limit 1)=1 '
    sql = 'select b.sku_id,b.sku_code from prod_product a left join prod_sku b on a.id=b.product_id where a.`status`=1 and b.`status`=1 and b.sku_type='+ str(skuType) + vbsql +' order by RAND() limit 1;'
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    skuInfoList.append(data[0])
    print('获取到的skuInfo：',skuInfoList)
    # print('-'*20,'数据库查询商品结束','-'*20,'\n\n')
    return skuInfoList

def getSkuInfo(mysqlhost,mysqluser,mysqlpassword,normalQuanty,vbQuanty=0):
    print('-'*20,'获取所需商品开始','-'*20)
    normalSkuList = []
    vbSkuList = []
    #获取普通商品信息列表
    if normalQuanty !=0:
        for i in range(normalQuanty):
            dbskuList = dbGetSku(mysqlhost,mysqluser,mysqlpassword,skuType='1')
            normalSkuList = normalSkuList + dbskuList
    #获取套装商品信息列表
    if vbQuanty != 0:
        for i in range(vbQuanty):
            dbvbskuList = dbGetSku(mysqlhost,mysqluser,mysqlpassword,skuType='6')
            vbSkuList = vbSkuList + dbvbskuList
    #校验必须有商品数量
    if not (normalQuanty or vbQuanty):
        print('普通商品和VB套装商品数量不能都为0！')
        exit()
    elif vbQuanty==0 and normalQuanty<2:
        print('VB套装商品为0时，普通商品至少2个！')
        exit()
    print('获取到的普通商品：%s\n获取到的VB套装商品：%s' %(normalSkuList,vbSkuList))
    print('-'*20,'获取所需商品结束','-'*20,'\n\n')
    return normalSkuList,vbSkuList

def getVbSkuRel(mysqlhost,mysqluser,mysqlpassword,vbSkuInfo):
    print('-'*20,'数据库查询VB商品包含的商品信息开始','-'*20)
    skuInfoList = []
    for vbSku in vbSkuInfo:
        conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'product')
        cur = conn.cursor()
        sql = 'select bind_sku_id,bind_sku_code from prod_vb_sku_rel where vb_sku_id='+"'"+ str(vbSku[0])+"'" +' and vb_sku_code='+"'"+ str(vbSku[1])+"'" + ';'
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        skuInfoList.extend(data)
    print('VB包含的商品信息：%s' %skuInfoList)
    print('-'*20,'数据库查询VB商品包含的商品信息结束','-'*20,'\n\n')
    return skuInfoList




#获取购物车信息
def getCartSku(ShopCart_IP,uid,orderType=1):
    header = {'Content-Type':'application/json','uid':str(uid)}
    #展示购物车，获取已存在商品skuId
    url = ShopCart_IP + '/v1/shopcart/shopcart/cartInfoDisplaying'
    body = {"queryBody":{"orderType":orderType,"channel":"PC"}}
    req = requests.post(url,json=body,headers=header)
    Response = json.loads(req.text)
    return Response

def clearCartAll(ShopCart_IP,uid,orderType=1):
    print('-'*20,'清除购物车开始','-'*20)
    headers = {"Content-Type":"application/json","uid":str(uid)}
    url = ShopCart_IP + '/v1/shopcart/shopcart/removeFromCart'
    param = {"head":{"token":"string","userId":"string"},"queryBody":[]}
    #获取购物车信息
    CartSkuInfo = getCartSku(ShopCart_IP,uid)['results']['shopcartSkuGroups']
    for i in range(len(CartSkuInfo)):
        skuId = CartSkuInfo[i]['shopcartSkus'][0]['skuId']
        skuIdDic = {"skuId":skuId,"type":1,"userId":uid}
        param['queryBody'].append(skuIdDic)
    req = requests.post(url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None:
        response = json.dumps(response,encoding='utf-8',ensure_ascii=False)
        print('清除购物车失败 %s' %(response))
    else:
        print('清除购物车成功')
    print('-'*20,'清除购物车结束','-'*20,'\n\n')

def updateInventory(PIM_IP,skucodelist,locationCode='OMS',quantity=999):
    print('-'*20,'开始更新库存','-'*20)
    url = PIM_IP + '/v1/pimBackend/productVirtualInv/updateInventory'
    for skucode in skucodelist:
        headers = {"Content-Type":"application/json"}
        param = {"locationCode":locationCode,"quantity":quantity,"skuCode":str(skucode),"storeCode":"S001"}
        req = requests.post(url,json=param,headers=headers)
        response = json.loads(req.text)
        if response['errorCode'] is not None:
            response = json.dumps(response,encoding='utf-8',ensure_ascii=False)
            print('更新库存失败',response)
        else:
            print('更新库存成功:%s' %param)
    print('-'*20,'更新库存结束','-'*20 ,'\n\n')

def updateInventory2(PIM_IP,skucodelist,locationCode='OMS',quantity=999):
    # print('-'*20,'开始更新库存','-'*20)
    url = PIM_IP + '/v1/pimBackend/productVirtualInv/updateInventory'
    for skucode in skucodelist:
        headers = {"Content-Type":"application/json"}
        param = {"locationCode":locationCode,"quantity":quantity,"skuCode":str(skucode),"storeCode":"S001"}
        req = requests.post(url,json=param,headers=headers)
        response = json.loads(req.text)
        if response['errorCode'] is not None:
            response = json.dumps(response,encoding='utf-8',ensure_ascii=False)
            # print('更新库存失败',response)
        else:
            pass
            # print('更新库存成功:%s' %param)
    # print('-'*20,'更新库存结束','-'*20 ,'\n\n')


def updateVirtualInventory(PIM_IP,skucodelist,locationCode='OMS',quantity=999):
    print('-'*20,'开始更新虚拟库存','-'*20)
    url = PIM_IP + '/v1/pimBackend/productVirtualInv/updateVirtualInventory'
    for skucode in skucodelist:
        headers = {"Content-Type":"application/json"}
        param = {"locationCode":locationCode,"quantity":quantity,"skuCode":skucode,"storeCode":"S001"}
        req = requests.post(url,json=param,headers=headers)
        response = json.loads(req.text)
        if response['errorCode'] is not None:
            response = json.dumps(response,encoding='utf-8',ensure_ascii=False)
            print('更新虚拟库存失败',response)
        else:
            print('更新虚拟库存成功',skucode)
    print('-'*20,'更新虚拟库存结束','-'*20 ,'\n\n')

#拆单商品更新库存
def updateSplitOrderSkuInventory(PIM_IP,skucodelist,type='normal'):
    print('-'*20,'更新拆单商品库存开始','-'*20)
    #序号奇数的商品BJ仓无货，偶数商品SH仓无货
    for i in range(len(skucodelist)):
        if (i+1)%2 == 0:
            if not skucodelist[i].startswith('VS'):
                updateInventory(PIM_IP,[skucodelist[i]],locationCode='SH')
            else:
                updateInventory(PIM_IP,[skucodelist[i]],locationCode='SH',quantity=-777)
            updateInventory(PIM_IP,[skucodelist[i]],locationCode='BJ',quantity=-888)
        else:
            updateInventory(PIM_IP,[skucodelist[i]],locationCode='SH',quantity=-888)
            if not skucodelist[i].startswith('VS'):
                updateInventory(PIM_IP,[skucodelist[i]],locationCode='BJ')
            else:
                updateInventory(PIM_IP,[skucodelist[i]],locationCode='BJ',quantity=-777)
        # if type.lower() != 'vb':
        updateInventory(PIM_IP,[skucodelist[i]],locationCode='OMS')
    print('-'*20,'更新拆单商品库存结束','-'*20 ,'\n\n')

def dealSpiitOrderOmsProcess(OMS_IP,mysqlhost,mysqluser,mysqlpassword,orderId):
    dealflag = True
    waitTimes = 0
    while dealflag and waitTimes < 5:
        # 获取sales_order中订单状态
        OrderStatus,orderSysId = get_SalesOrderStatus(mysqlhost,mysqluser,mysqlpassword,orderId)
        if OrderStatus == 'PENDING':
            dealPending(OMS_IP)
            waitTimes += 1
        elif OrderStatus == 'EXCEPTION':
            dealException(OMS_IP,orderSysId)
        elif OrderStatus == 'PENDING_MIDDLE':
            dealWaitSend(30)
            print('等待3s')
            waitTimes += 1
        elif OrderStatus == 'WAIT_SEND_SAP' or OrderStatus == 'WAIT_ROUTE_ORDER':
            dealWaitSend(30)
            waitTimes += 1
        elif OrderStatus == 'WAIT_SAPPROCESS' or OrderStatus == 'WAIT_SAPPROCESS/WAIT_SAPPROCESS' or OrderStatus == 'WAIT_SAPPROCESS/WAIT_SEND_SAP':
            dealflag = False
            print('订单已是处理中状态\n')
        else:
            time.sleep(5)
            waitTimes += 1
        if waitTimes >= 5:
            print('已等待五次还未处理成功，目前订单：%s 状态是%s\n' %(orderId,OrderStatus))
            exit()

def dealOmsSplitOrderToOrder(OMS_IP):
    print('-'*20,'开始推送OMS拆单信息至Order','-'*20)
    url = OMS_IP + '/job/exec/orders?th=pushSplitOrderToSoaJob'
    req = requests.get(url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('推送OMS拆单信息至Order失败:',response)
        exit()
    else:
        for step in range(0,45,3):
            print('等待3s')
            time.sleep(3)
        print('推送OMS拆单信息至Order成功')
    print('-'*20,'推送OMS拆单信息至Order结束','-'*20 ,'\n\n')


def getSplitPurchaseOrder(mysqlhost,mysqluser,mysqlpassword,orderId):
    print('-'*20,'开始获取purchase_order对应订单记录','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "select a.PURCHASE_ORDER_NUMBER,a.SIGN_TIME,a.ORDER_INTERNAL_STATUS  from purchase_order a where a.SALES_ORDER_NUMBER=" + "'" + orderId + "';"
    print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    if len(data):
        print('成功获取purchase_order对应订单记录\n %s' %str(data))
    else:
        print('获取purchase_order对应订单记录失败，未获取到相应记录')
        cur.close()
        exit()
    cur.close()
    print('-'*20,'获取purchase_order对应订单记录结束','-'*20 ,'\n\n')
    return data


def checkCreateSplitOrderInputArgus():
    if len(sys.argv) < 5:
        print('请输入正确的入参，例如：python CreateSplitOrder.py stage 2100323 2 0，其中stage代表运行环境，2100323代表uid，2代表2个普通商品，0表示0个VB套装商品')
        exit()
    env = sys.argv[1]
    if env not in allowedenv:
        print('输入的环境%s有误,应该为qa2或者stage' %env)
        exit()
    uid = sys.argv[2]
    if not uid.isdigit():
        print('输入的用户uid：%s有误，请检查' %uid)
        exit()
    normalQuanty = sys.argv[3]
    vbQuanty = sys.argv[4]
    if not normalQuanty.isdigit() or not vbQuanty.isdigit():
        print('输入的普通商品数量：%s,VB套装商品数量：%s 有误，请检查' %(normalQuanty,vbQuanty))
    else:
        normalQuanty = int(normalQuanty)
        vbQuanty = int(vbQuanty)
    return env,uid,normalQuanty,vbQuanty


def CreateSpiltOrder():
    # env = 'qa2'
    # # uid = '2001844981'
    # uid= '130'
    # normalQuanty = 5
    # vbQuanty = 0
    env,uid,normalQuanty,vbQuanty = checkCreateSplitOrderInputArgus()

    mysqlhost = config['mysql_'+ env]['host']
    mysqluser = config['mysql_'+ env]['user']
    mysqlpassword = config['mysql_'+ env]['password']

    ShopCart_IP = GetIP.getIp(env,'shop-cart')
    PIM_IP = GetIP.getIp(env,'pim')
    Order_IP = GetIP.getIp(env,'sephora-order-service')
    OMS_IP = GetIP.getIp(env,'oms')

    skuIdList = []
    skuCodeList = []
    vbSubSkuList = []
    vbSubskuIdList = []
    vbSubskuCodeList = []
    vbSkuTime = 5
    #获取商品信息
    normalSkuList,vbSkuList = getSkuInfo(mysqlhost,mysqluser,mysqlpassword,normalQuanty,vbQuanty)

    #VB商品获取子商品信息
    if vbQuanty:
        vbSubSkuList =  getVbSkuRel(mysqlhost,mysqluser,mysqlpassword,vbSkuList)
    while vbQuanty and  not len(vbSubSkuList) and vbSkuTime > 0:
        print('VB商品包含的子商品未找到，重新获取VB商品')
        normalSkuList,vbSkuList = getSkuInfo(mysqlhost,mysqluser,mysqlpassword,normalQuanty,vbQuanty)
        vbSubSkuList =  getVbSkuRel(mysqlhost,mysqluser,mysqlpassword,vbSkuList)
        vbSkuTime -= 1
        if vbSkuTime <= 0:
            print('%s次还没找到合适的vb商品，退出程序，请重新尝试' %vbSkuTime)
            exit()

    for normalSku in normalSkuList:
        skuIdList.append(normalSku[0])
        skuCodeList.append(normalSku[1])
    for vbSku in vbSkuList:
        skuIdList.append(vbSku[0])
        skuCodeList.append(vbSku[1])
    print('获取到的skuId列表：',skuIdList,'\n','获取到的skuCode列表：',skuCodeList,'\n')

    for vbSubSku in vbSubSkuList:
        vbSubskuIdList.append(vbSubSku[0])
        vbSubskuCodeList.append(vbSubSku[1])

    #清空购物车
    clearCartAll(ShopCart_IP,uid,orderType=1)

    #更新拆单商品库存
    updateSplitOrderSkuInventory(PIM_IP,skuCodeList)
    updateSplitOrderSkuInventory(PIM_IP,vbSubskuCodeList,'vb')

    #添加商品至购物车
    for skuId in skuIdList:
        addToCartForSingleProduct(ShopCart_IP,uid,skuId,quantity=2)

    ## 购物车第二步
    getShopcartStepTwo(ShopCart_IP,uid)

    ## 修改支付方式
    changePayment(ShopCart_IP,uid)

    #获取收货地址
    addressId = getaddressIdByUid(mysqlhost,mysqluser,mysqlpassword,uid)

    if not addressId:
        print('未找到收货地址，请设置！')
        exit()

    ## 提交订单
    # orderId = addOrders(ShopCart_IP,uid,skuIdList)
    orderId = addOrdersV3(ShopCart_IP,uid,skuIdList,addressId)
    time.sleep(3)

    #VB套装商品库存变更
    for vbSku in vbSkuList:
        updateInventory(PIM_IP,[vbSku[1]],'OMS',quantity=-666)

    ## 将订单提前一小时
    forwadOnehour(mysqlhost,mysqluser,mysqlpassword,orderId)

    ## 推送订单至OMS并索引至elasticSearch
    orderSync(Order_IP,orderId)


    #OMS订单变为处理中状态
    dealSpiitOrderOmsProcess(OMS_IP,mysqlhost,mysqluser,mysqlpassword,orderId)

    time.sleep(3)
    data = getSplitPurchaseOrder(mysqlhost,mysqluser,mysqlpassword,orderId)
    #判断是否拆单
    splitFlag = IsSplit(data)

    #推送OMS拆单信息至Order
    dealOmsSplitOrderToOrder(OMS_IP)

    #VB套装商品库存恢复
    for vbSku in vbSkuList:
        updateInventory2(PIM_IP,[vbSku[1]],'OMS',quantity=1000)

    # #修改订单状态为配送中
    # orderStatusSync(Order_IP,uid,orderId,'SHIPPED')

    if splitFlag:
        print('\n\n成功生成拆单订单，订单号是：%s\nOMS中Purchase订单信息%s' %(orderId,data))
    else:
        print('\n\n成功生成拆单订单失败，OMS中订单：%s非拆单' %orderId)




# uid = '130'

# clearCartAll(ShopCart_IP,uid,orderType=1)
#

# env = 'stage'
#
# mysqlhost = config['mysql_'+ env]['host']
# mysqluser = config['mysql_'+ env]['user']
# mysqlpassword = config['mysql_'+ env]['password']
#
# ShopCart_IP = GetIP.getIp(env,'shop-cart')
# PIM_IP = GetIP.getIp(env,'pim')
# Order_IP = GetIP.getIp(env,'sephora-order-service')
# OMS_IP = GetIP.getIp(env,'oms')
# #
# dealNormalOrderOMSProcess(OMS_IP,mysqlhost,mysqluser,mysqlpassword,'1149819229177666')
