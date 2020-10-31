"""
	获取短信验证码，当为生产环境时，由于有两套集群，故特殊处理
	老流程发送的短信验证码：python MyClusterRedis2.py stage 14444404550 r
	usercenter新流程获取的短信验证码：python MyClusterRedis2.py stage 18817943321 new  ios forget
	usercenter新流程场景（忘记密码：FORGET；账号密码注册：REGIST；手机验证码登录：SMS；账号密码登录：
	`	PWD；联合登录绑定手机：SOCIALBIND）

"""
import sys
from rediscluster import RedisCluster

redis_db_qa2 = [{'host':'10.157.26.84', 'port':6379},{'host':'10.157.26.85', 'port':6379},
				{'host':'10.157.26.86', 'port':6379}, {'host':'10.157.26.87', 'port':6379},
				{'host':'10.157.26.88', 'port':6379}]

redis_db_stage = [{'host':'10.157.24.45', 'port':6379},{'host':'10.157.24.46', 'port':6379},
			     {'host':'10.157.24.47', 'port':6379}, {'host':'10.157.24.54', 'port':6379},
				 {'host':'10.157.24.55', 'port':6379}]

redis_db_prd = [{'host':'10.157.32.78', 'port':6379}]
redis_db_prd2 = [{'host':'10.157.32.78', 'port':6479},
		 {'host':'10.157.32.79', 'port':6479},{'host':'10.157.32.80', 'port':6479},
		 {'host':'10.157.32.65', 'port':6479},{'host':'10.157.32.66', 'port':6479},
		 {'host':'10.157.32.69', 'port':6479}]

def getsmCode(env,node,rediskey):
	redisconn = RedisCluster(startup_nodes=node,decode_responses=True)
	smsCode = redisconn.get(rediskey)
	if smsCode:
		return smsCode
	elif env == 'prd':
		redisconn = RedisCluster(startup_nodes=redis_db_prd2,decode_responses=True)
		smsCode = redisconn.get(rediskey)
		if smsCode:
			return smsCode

if __name__ == '__main__':
	env = sys.argv[1]
	if env == 'qa2':
		target_redis = redis_db_qa2
	elif env == 'stage':
		target_redis = redis_db_stage
	elif env == 'prd':
		target_redis = redis_db_prd
	else:
		print('Bad argument!!!!!!!')
		sys.exit(1)

	sence = sys.argv[3].lower()
	mobile = sys.argv[2]
	if sence == 'r': #注册
		smscode = 'SOA:MYACCOUNT:SMSCODE:1001:'+ mobile
	elif sence == 'f': #忘记密码
		smscode = 'SOA:MYACCOUNT:SMSCODE:1002:'+ mobile
	elif sence == 'w': #微信绑卡
		smscode = 'SOA:MYACCOUNT:SMSCODE:1003:'+ mobile
	elif sence == 'g':
		smscode = 'SOA:MYACCOUNT:SMSCODE:1004:'+ mobile
	elif sence  == 'm': #留资
		smscode = 'SOA:MYACCOUNT:SMSCODE:1005:'+ mobile
	elif sence == 'l':#验证码登录
		smscode = 'SOA:MYACCOUNT:SMSCODE:1006:'+ mobile
	elif sence  == 'c':
		smscode = 'SOA:MYACCOUNT:SMSCODE:1007:'+ mobile
	elif sence == 'h':
		smscode = 'SOA:MYACCOUNT:SMSCODE:1008:'+ mobile
	elif sence == '9':
		smscode = 'SOA:MYACCOUNT:SMSCODE:1009:'+ mobile
	elif sence == 't':
		smscode = 'SOA:MYACCOUNT:SMSCODE:2001:'+ mobile
	elif sence == 'new':
		channel = sys.argv[4].upper()
		#场景（忘记密码：FORGET；手机验证码登录：SMS；账号密码登录：PWD；联合登录绑定手机：SOCIALBIND）
		scene_new =sys.argv[5].upper()
		smscode = 'cache:usercenter_telephone_smscode:usercenter_telephone_smscode_'+ mobile + '_' + channel + '_' + scene_new
	else:
		print('Bad argument!!!!!!!')
		sys.exit(1)

	try:
		sms = getsmCode(env,target_redis,smscode)
		if sms:
			if sence == 'new':
				sms2 = sms[1:7]
				print("smscode is:", sms2)
			else:
				print("smscode is:", sms)
		else:
			print("Cannot find the smscode")

	except Exception as e:
		print("Connect Redis node error:", e)
		sys.exit(1)
