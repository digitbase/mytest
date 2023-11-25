'''
作成日期： 2023年11月2日
作者：许能
功能：代码模仿1400服务端实现1400的数据接收和图片存储
	仅用于设备的接收

	设备号：默认三个设备号：device_registerinfo
	所有信息请按需添加 

	存储路径默认存储在：linux home目录 或者是  Storagepath 根据变量去修改
	windows：在桌面
	请根据自己的需求修改路径
	路径修改的地点：fuc_mkdir()

'''


import random, hashlib
import ssl
import os
import tornado.ioloop
import tornado.web
import json
import string
import json,time,base64
import datetime
import re
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import urlparse, parse_qs



'''
修改区域
'''

PORT=20092 #1400的端口
timeout = 3600  # 3600s
max_recordsize = 5
max_vol_Pictures = 10000 #暂时没用

isCloseConn=True #是否开启短链接模式

isSavePic=True  #全局是否存储图片 
g_Pictype=".jpg" #图片存储后缀
MAX_PICLIST_VOL=0

isSaveJson=True #全局是否存储json 
g_Logtype=".json" #json存储后缀
MAX_JSONLIST_VOL=0

# 保存客户端信息
device_registerinfo = {
         "31010002031190000078":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':()}}
        ,"31010002031190000079":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000080":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000081":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000082":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000083":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000084":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000085":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000086":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000087":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000088":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
        ,"31010002031190000089":{"ip_port": '',"online":False,"password":"ctff1234","registertime":'','realm':'', 'nonce':'', 'record_registertime':[], 'unregistertime':[], 'result':{},'property':{'isSavePic':'False', 'picList':[],'isSaveJson':'False','JSONList':[]}}
    }  # 前端注册信息 


'''
g_folder_full_path  status_data 不修改
EvertType_info  新增扩展字段时候添加

'''

g_folder_full_path=""

status_data = {"0":"OK", '1':"OtherError", "2":"Device Busy", "3":"Device Error", \
               "4":"Invalid Operation", "5":"Invalid XML Format", "6":"Invalid XML Content", \
               "7":"Invalid JSON Format", "8":"Invalid JSON Content", "9":"Reboot"}

#B.3.51 视频图像分析处理事件类型（EventType）
EvertType_info={
    "0":"其他****"
    ,"1":"卡口**过车**"
    ,"2":"卡口**过人**"
    ,"3":"卡口**打架**"
    ,"4":"卡口**快速奔跑**"
    ,"5":"目标检测与特征提取**运动目标检测**"
    ,"6":"目标检测与特征提取**目标分类**"
    ,"7":"目标检测与特征提取**目标颜色检测**"
    ,"8":"目标检测与特征提取**行人检测**"
    ,"9":"目标检测与特征提取**人员属性分析**"
    ,"10":"目标检测与特征提取**人脸检测**"
    ,"11":"目标检测与特征提取**人脸比对**"
    ,"12":"目标检测与特征提取**车辆检测**"
    ,"13":"目标检测与特征提取**车辆比对**"
    ,"14":"目标数量分析**流量统计**"
    ,"15":"目标数量分析**密度检测**"
    ,"16":"目标识别**车牌识别**"
    ,"17":"目标识别**车辆基本特征识别**"
    ,"18":"目标识别**车辆个体特征识别**"
    ,"19":"行为分析**绊线检测**"
    ,"20":"行为分析**入侵检测**"
    ,"21":"行为分析**逆行检测**"
    ,"22":"行为分析**徘徊检测**"
    ,"23":"行为分析**遗留物检测**"
    ,"24":"行为分析**目标移除检测**"
    ,"25":"视频摘要**视频摘要**"
    ,"26":"视频增强与复原**去雾**"
    ,"27":"视频增强与复原**去模糊**"
    ,"28":"视频增强与复原**对比度增强**"
    ,"29":"视频增强与复原**低照度视频图像增强**"
    ,"30":"视频增强与复原**偏色校正**"
    ,"31":"视频增强与复原**宽动态增强**"
    ,"32":"视频增强与复原**超分辨率重建**"
    ,"33":"视频增强与复原**几何畸变校正**"
    ,"34":"视频增强与复原**奇偶场校正**"
    ,"35":"视频增强与复原**颜色空间分量分离**"
    ,"36":"视频增强与复原**去噪声**"
    ,"600":"行为分析**高空抛物**扩展"
    ,"601":"行为分析**摔跤识别**扩展"
    ,"602":"行为分析**打架斗殴识别**扩展"
    ,"603":"目标识别**车辆禁停**扩展"
    ,"604":"目标检测与特征提取**打电话**扩展"
    ,"605":"目标检测与特征提取**未戴厨师帽**扩展"
    ,"606":"目标检测与特征提取**无口罩**扩展"
    ,"607":"目标检测与特征提取**抽烟**扩展"
    ,"608":"目标检测与特征提取**未戴手套**扩展"
    ,"609":"目标检测与特征提取**未穿工作服**扩展"
    ,"610":"目标检测与特征提取**环境卫生**扩展"
    ,"611":"目标检测与特征提取**地面积水**扩展"
    ,"612":"目标检测与特征提取**垃圾桶未盖**扩展"
    ,"613":"目标检测与特征提取**违规置物**扩展"
    ,"614":"目标识别**有老鼠**扩展"
    ,"615":"视频诊断**视频不正**扩展"
    ,"616":"视频诊断**视频模糊**扩展"
    ,"617":"明厨亮灶**明厨亮灶**扩展"
    ,"618":"目标检测与特征提取**离岗**扩展"
    ,"619":"目标识别**明火检测**扩展"
    ,"620":"目标检测与特征提取**水利-水位尺**扩展"
    ,"621":"目标检测与特征提取**安全帽**扩展"
    ,"622":"目标检测与特征提取**动物检测**扩展"
    ,"623":"视频抽帧**视频抽帧**扩展"
    ,"624":"目标检测与特征提取**车辆违停**扩展"
    ,"625":"视频诊断**视频诊断**扩展"
    ,"626":"目标检测与特征提取**持刀持械**扩展"
    ,"627":"目标检测与特征提取**物品检测**扩展"
    ,"628":"目标检测与特征提取**人员聚集**扩展"
    ,"629":"目标检测与特征提取**电动车识别**扩展"
    ,"630":"目标检测与特征提取**垃圾桶溢出检测**扩展"
    ,"631":"目标检测与特征提取**全目标检测**扩展"
    ,"632":"流量统计**动态客流统计**扩展"
    ,"633":"流量统计**静态客流统计**扩展"
    ,"634":"卡口**过非机动车**扩展"
    ,"635":"目标检测与特征提取**街边秩序检测**扩展"
    ,"636":"流量统计**过船统计**扩展"
    ,"637":"目标检测与特征提取**巡店组合**扩展"
    ,"638":"目标检测与特征提取**玩手机**扩展"
    ,"639":"目标检测与特征提取**过斑马线检测**扩展"
    ,"640":"目标检测与特征提取**地面垃圾检测**扩展"
    ,"641":"视频提取**时光缩影**扩展"
    ,"642":"目标检测与特征提取**长袖**扩展"
    ,"643":"目标检测与特征提取**短袖**扩展"
    ,"644":"目标检测与特征提取**无袖**扩展"
    ,"645":"目标检测与特征提取**无衬衫**扩展"
    ,"646":"目标检测与特征提取**占道检测**扩展"
    ,"647":"视频提取**家装缩影**扩展"
    ,"650":"目标检测与特征提取**医用防护服检测**扩展"
    ,"651":"目标检测与特征提取**开关门**扩展"
    ,"652":"目标检测与特征提取**久出未归**扩展"
    ,"653":"目标检测与特征提取**钓鱼推送**扩展"
    ,"654":"目标检测与特征提取**行人闯红灯**扩展"
    ,"654":"目标检测与特征提取**行人闯红灯**"
    ,"655":"目标检测与特征提取**双人在岗**"
    ,"656":"目标检测与特征提取**人员逗留**"
    ,"657":"目标检测与特征提取**代客操作手机**"
    ,"658":"目标检测与特征提取**翻越围栏**"
    ,"659":"目标检测与特征提取**智慧城管**"
    ,"660":"目标检测与特征提取**店外经营**"
    ,"661":"目标检测与特征提取**无照经营游商(游摊小贩)**"
    ,"662":"目标检测与特征提取**占道废品收购**"
    ,"663":"目标检测与特征提取**违章接坡**"
    ,"664":"目标检测与特征提取**私搭乱建**"
    ,"665":"目标检测与特征提取**擅自搭建气模拱门**"
    ,"666":"目标检测与特征提取**擅自架设管线、杆线设施**"
    ,"667":"目标检测与特征提取**桥头街面占线(违规撑伞)**"
    ,"668":"目标检测与特征提取**沿街晾挂**"
    ,"669":"目标检测与特征提取**空调室外机低挂**"
    ,"670":"目标检测与特征提取**违规牌匾标识**"
    ,"671":"目标检测与特征提取**违规户外广告**"
    ,"672":"目标检测与特征提取**违规标语宣传品**"
    ,"673":"目标检测与特征提取**非装饰性树挂**"
    ,"674":"目标检测与特征提取**非法小广告**"
    ,"675":"目标检测与特征提取**流浪乞讨**"
    ,"676":"目标检测与特征提取**街头散发广告**"
    ,"677":"目标检测与特征提取**临街屠宰**"
    ,"678":"目标检测与特征提取**擅自饲养家禽家畜**"
    ,"679":"目标检测与特征提取**露天烧烤**"
    ,"680":"目标检测与特征提取**方形垃圾箱异常(倒伏、门未关闭、破损、缺失等)**"
    ,"681":"目标检测与特征提取**垃圾桶不整洁**"
    ,"682":"目标检测与特征提取**不规范垃圾桶**"
    ,"683":"目标检测与特征提取**打包垃圾**"
    ,"684":"目标检测与特征提取**施工占道**"
    ,"685":"目标检测与特征提取**乱堆物堆料**"
    ,"686":"目标检测与特征提取**积存垃圾渣土**"
    ,"687":"目标检测与特征提取**施工废弃料**"
    ,"688":"目标检测与特征提取**工地物料乱堆放**"
    ,"689":"目标检测与特征提取**废弃家具设备**"
    ,"690":"目标检测与特征提取**乱倒乱排污水、废水**"
    ,"691":"目标检测与特征提取**焚烧垃圾、树叶**"
    ,"692":"目标检测与特征提取**水域不洁**"
    ,"693":"目标检测与特征提取**绿化弃料**"
    ,"694":"目标检测与特征提取**绿地脏乱**"
    ,"695":"目标检测与特征提取**动物尸体**"
    ,"696":"目标检测与特征提取**道路积水**"
    ,"697":"目标检测与特征提取**道路遗洒**"
    ,"698":"目标检测与特征提取**道路破损**"
    ,"699":"目标检测与特征提取**道路塌陷**"
    ,"700":"目标检测与特征提取**船只防撞检测**"
    ,"701":"目标检测与特征提取**在岗检测**"
    ,"702":"目标检测与特征提取**垃圾桶检测（视频抽帧）**"
    ,"703":"目标检测与特征提取**垃圾分类**"
    }

Image_Typeinfo={
    "1":"车辆大图"
    ,"2":"车牌彩色小图"
    ,"3":"车牌二值化图"
    ,"4":"驾驶员面部特征图"
    ,"5":"副驾驶面部特征图"
    ,"6":"车标"
    ,"7":"违章合成图"
    ,"8":"过车合成图"
    ,"9":"车辆特写图"
    ,"10":"人员图"
    ,"11":"人脸图"
    ,"12":"非机动车图"
    ,"13":"物品图"
    ,"14":"场景图"
    ,"100":"一般图片"
}


class CommonHandler(tornado.web.RequestHandler):  
    '''
     用来产生nonce
    '''
    def create_realm_nonce(self, bits):
        # ------------有新连接时，产生随机数-------------------
        chars = string.ascii_letters + string.digits
        realm_nonce = ''
        for i in range(bits):
            realm_nonce += ''.join(random.sample(chars, 1))
        return realm_nonce
    
    # 设置 nonce    
    def set_device_nonce(self, id, nonce):   
        device_registerinfo[id]['nonce'] = nonce
        print(f"-----设置 nonce ----->{device_registerinfo[id]}----------------")


    # 获得 nonce    
    def get_device_nonce(self,id):    
        ret = device_registerinfo.get(id, {}).get('online', "KeyError")
        if "KeyError" != ret:  
            if device_registerinfo.get(id) == None:
                ret = None       
            else:
                ret = device_registerinfo[id].get('nonce')
            return ret
        else:
            return "KeyError"        

     
    # 设置 realm    
    def set_device_realm(self, id, realm):   
        device_registerinfo[id]['realm'] = realm
        print(f"-----设置 realm ----->{device_registerinfo[id]}----------------")


     #获得 realm    
    def get_device_realm(self,id): 
        ret = device_registerinfo.get(id, {}).get('online', "KeyError")
        if "KeyError" != ret:
            if device_registerinfo.get(id) == None:
                ret = None       
            else:
                ret = device_registerinfo[id].get('realm')
            return ret
        else:
            return "KeyError"
    
        # 设置 ip_port    
    def set_device_ip_port(self, id, ip_port):   
        device_registerinfo[id]['ip_port'] = ip_port
        print(f"-----设置 ip_port----->{device_registerinfo[id]}----------------")


     #获得 ip_port    
    def get_device_ip_port(self,id): 
        ret = device_registerinfo.get(id, {}).get('online', "KeyError")
        if "KeyError" != ret:       
            if device_registerinfo.get(id) == None:
                ret = None       
            else:
                ret = device_registerinfo[id].get('ip_port')
            return ret
        else:
            return "KeyError"
        
    # 获得 是否有设备ip 信息
    def get_device_info(self, id):        
        try:  
            ret = device_registerinfo.get(id)
            return ret
        except KeyError:  
            print(f"{id} does not exist in the dictionary.")
            return None
              
    # 获得 注册时间 registertime
    def get_device_registertime(self, ip_port, id):       
        if device_registerinfo.get(id) == None:
            others = "%s not register"%id
            print(f"{ip_port} +  {others}")
            ret = None               
        else:
            ret = device_registerinfo[id].get('registertime')
        return ret
    
     # 设置 注册时间 registertime
    def set_device_registertime(self,ip_port, id, registertime):
        device_registerinfo[id]['registertime'] = registertime
        print(f"注册信息：{ip_port} ***** {id}*****{registertime}")

    # 设置 记录 注册时间列表 record_registertime
    def set_device_recordregtime(self, ip_port, id, record_registertime):
        record_registertime_list = device_registerinfo[id]["record_registertime"]

        if len(record_registertime_list) > max_recordsize:  
            record_registertime_list.pop(0)# 删除最老的数据 

        record_registertime_list.append(record_registertime)
        device_registerinfo[id]["registertime"] = record_registertime_list

        print(f"记录 注册时间:{ip_port} ***** {id}*****{record_registertime}")


    # 设置 注销时间 unregistertime
    def set_device_unregistertime(self, id, unregistertime):
        unregistertime_list = device_registerinfo[id]["unregistertime"]

        if len(unregistertime_list) > max_recordsize:  
            unregistertime_list.pop(0)# 删除最老的数据 

        unregistertime_list.append(unregistertime)
        device_registerinfo[id]["unregistertime"] = unregistertime_list
    
    # 设置 记录 注册时间列表 password
    def get_device_password(self, id):
           return device_registerinfo[id]['password']

    # 设置 记录 注册时间列表 record_registertime
    def set_device_onlinestatus(self, ip_port, id, status):
            device_registerinfo[id]['online'] = status   

    # 设置 记录 注册时间列表 record_registertime
    def get_device_onlinestatus(self, ip_port, id):
           return device_registerinfo.get(id, {}).get('online', "KeyError")

    # 删除 注册时间 registertime
    def del_device_registertime(self, id):    
        device_registerinfo[id]['registertime'] = None



    # 获得 注册时间 record_registertime
    def get_device_recordregtime(self, id):        
        regtime_list = device_registerinfo[id].get('record_registertime')
        if len(regtime_list) > 0:  
            regtime = regtime_list[-1] # 最近的注册时间    
        else:  
            regtime = None
        return regtime
         
    # # 设置 刷新注册时间 refresh_registertime
    # def set_device_refreshregtime(self, ip_port, id, refresh_registertime):
    #     refresh_registertime_list = device_registerinfo[id]["refresh_registertime"]

    #     if len(refresh_registertime_list) > max_recordsize:  
    #         refresh_registertime_list.pop(0)# 删除最老的数据 

    #     refresh_registertime_list.append(refresh_registertime)
    #     device_registerinfo[id]["registertime"] = refresh_registertime_list

    #     print(f"设置 刷新注册时间:{ip_port} ***** {id}*****{refresh_registertime}")

    # # 获得 刷新注册时间 refresh_registertime
    # def get_device_refreshregtime(self, id): 
    #     refreshtime_list = device_registerinfo[id].get('refresh_registertime')
    #     if len(refreshtime_list) > 0:  
    #         refreshtime = refreshtime_list[-1]   
    #     else:  
    #         refreshtime = 0
    #     return refreshtime


    def response_StatusObject(self, ip_port, id, m_uri, m_time):
        """
        功能：服务器返回200 OK ,StatusCode="0"
        :param ID:    id
        return
            True ：回复正常
        """   
        # 如果有ga.ini文件，根据ini文件内容回复消息
        # if self.response_useinifile():
        #     return
        # 1，组包 body
        StatusCode = "0"
        StatusString = "OK"
        LocalTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        content_dict = {
            "ResponseStatusObject": {
                "Id": id,
                "RequestURL": m_uri,
                "StatusCode": StatusCode,
                "StatusString": StatusString,
                "LocalTime": LocalTime
            }
        }
        content_str = json.dumps(content_dict)
        content_len = len(content_str)
        # 2，组包 header
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        
        headers = {}
        #header["Expires"] = '0'
        headers["Content-Type"] = "application/json;charset=UTF-8"
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        headers["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
        headers["Connection"] = "close" 
        headers["Content-Length"] = str(content_len)

        infomsg = "200 OK" + " ,ID:" + id
        infomsg +=" ,RequestURL:" + m_uri
        infomsg +=" ,返回消息时长:" + "%.06f"%(time.time()- m_time) + 's'
        # 3，回复消息
        if self.response_base(200, headers, content_str):
            print(f"{ip_port} + 回复:  + {infomsg}") 
            return True
        else:
            print(f"{ip_port} +  没有正确回复: + {infomsg}") 
        return  False
    

    def response_400(self, ip_port, Reason):
        """
        功能：返回400
        :param Reason: 原因
        """        
        header = {}
        header["Content-Type"] = "application/json; charset=utf-8" 
        header["Reason-Phrase"] = Reason
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        header["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
        header["Connection"] = "close" 
        header["Content-Length"] = "0"
        infomsg = " 回复400" + " ,Reason:" + Reason
        if self.response_base(400, header, ""):
            print(f"{ip_port} + 回复:  + {infomsg}") 
        else:
            print(f"{ip_port} +  没有正确回复: + {infomsg}") 
        return
        

    def response_401(self, id, Reason, m_time):
        """
        功能：返回401鉴权挑战
        :param Reason: 原因
        """
        realm = self.get_device_realm(id)
        if "KeyError" != realm:
            if realm == None or realm == '':
                realm = self.create_realm_nonce(10)   
                self.set_device_realm(id, realm) # 保存
                print(f"{self.request.remote_ip} + ' 随机生成realm:{realm}")
            realmstr = '"' + realm + '"'

            # 2, 获得nonce
            nonce = self.get_device_nonce(id)
            if nonce == None or nonce == '':
                nonce = self.create_realm_nonce(16)   
                self.set_device_nonce(id, nonce) # 保存
                print(f"{self.request.remote_ip} + ' 随机生成nonce:{nonce}")
            noncestr = '"' + nonce + '"'
            qopstr = '"auth"'

            stalestr = '"true"'

            #auth = 'Digest realm=' + realmstr + ',qop=' + qopstr + ',nonce=' + noncestr + ',stale=' + stalestr
            auth = 'Digest realm=' + realmstr + ',qop=' + qopstr + ',nonce=' + noncestr
        else:
            auth = ""
            print(f"-------------------{Reason}---------------------------")

        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        headers = {}
        headers["Content-Type"] = "application/json; charset=utf-8" 
        headers["Reason-Phrase"] = Reason
        headers["WWW-Authenticate"] = auth
        headers["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
        headers["Connection"] = "close" 
        headers["Content-Length"] = "0"

        infomsg = "401鉴权挑战" +" ,Reason:" + Reason
        if self.response_base(401, headers, ""):  
            print(f"{self.request.remote_ip} + 回复:  + {infomsg}")
        else:
            print(f"{self.request.remote_ip} + 没有正确回复:  + {infomsg}")
        return True

    def response_200(self, IDs, Reason, StatusCode, m_uri, m_time):
        """
        功能：返回200
        :param IDs:    IDs多个ID
        :param Reason:      原因
        :param StatusCode:  StatusCode
            O-OK， 正常
            1-OtherError，其他未知错误
            2-Device Busy，设备忙
            3-Device Error，设备错
            4-Invalid Operation，无效操作
            5-Invalid XML Format，XML格式无效
            6-Invalid XML Content，XML内容无效
            7-Invalid JSON Format，JSON格式无效
            8-Invalid JSON Content，JSON内容无效
            9-Reboot，系统重启中，以附录B中类型定义为准
        """
        # 如果有ga.ini文件，根据ini文件内容回复消息
        # if self.response_useinifile():
        #     return
        # 1，组包 body
        status_data = {"0":"OK", '1':"OtherError", "2":"Device Busy", "3":"Device Error", \
                        "4":"Invalid Operation", "5":"Invalid XML Format", "6":"Invalid XML Content", \
                        "7":"Invalid JSON Format", "8":"Invalid JSON Content", "9":"Reboot"}
        StatusString = status_data.get(StatusCode)  
        if StatusString == None:
            # GAlogging.error(self.ip_port + "StatusCode=%s, error"%StatusCode)
            return
        LocalTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        content_dict = {
            "ResponseStatusListObject":{
                "ResponseStatusObject": []
            }
        }        
        value = content_dict["ResponseStatusListObject"]["ResponseStatusObject"]  
        for id in IDs:
            value.append({"RequestURL": m_uri, "StatusCode":StatusCode, "StatusString":StatusString, 'Id':id, "LocalTime":LocalTime})
        content_str = json.dumps(content_dict)
        content_len = len(content_str)
        # 2，组包 header
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        headers = {}
        headers["Content-Type"] = "application/json; charset=utf-8" 
        headers["Reason-Phrase"] = Reason 
        headers["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
        headers["Connection"] = "close" 
        headers["Content-Length"] = str(content_len)
        infomsg = " StatusCode:{}, StatusString:{}, Reason:{}, RequestURL:{}".format(StatusCode, StatusString, Reason, m_uri)
        infomsg += "\n IDs:{}".format(IDs)
        infomsg += "\n 返回消息时长:%.06f"%(time.time()- m_time) + 's'


        # 3，回复消息
        if self.response_base(200, headers, content_str):
            pass

    def response_base(self, statuscode, headers, body): 
        # 返回http响应信息 return False 显示错误信息
        self._headers.update(headers)
        self.set_status(statuscode)
        self.write(body)
        self.CloseConn()
        return True

    def check_Authorization(self, id, digest, noncestr, m_time):
        """
        功能：检查digest中的授权信息，认证失败返回False，并回复401鉴权挑战
        :param in
        digest: http中的Authorization: Digest username=..., realm=...,
        noncestr: 全局变量nonce（服务器返回401时生成的nonce值，保存在一全局变量中）
        :return True：根据计算nonce中的，认证成功
        """        
        username = realm = uri = nonce = nc = cnonce = qop = response = None
        # 1 取值
        Authorization_str = digest.split(",")
        for a in Authorization_str:
            param = a.strip()
            if param.startswith('Digest username='):
                username = param[len('Digest username='):].strip().strip('"')
            elif param.startswith('realm='):
                realm = param[len('realm='):].strip().strip('"')
            elif param.startswith('uri='):
                uri = param[len('uri='):].strip().strip('"')                
            elif param.startswith('nonce='):
                nonce = param[len('nonce='):].strip().strip('"')
            elif param.startswith('nc='):
                nc = param[len('nc='):].strip().strip('"')           
            elif param.startswith('cnonce='):
                cnonce = param[len('cnonce='):].strip().strip('"')
            elif param.startswith('qop='):
                qop = param[len('qop='):].strip().strip('"')
            elif param.startswith('response='):
                response = param[len('response='):].strip().strip('"')
        if username is None or realm is None or uri is None or nonce is None or nc is None or cnonce is None or qop is None or response is None:
            # GAlogging.error(self.ip_port + ' Digiest : ' + digest)
            others = "Digiest error"
            self.response_401(id, others, m_time)
            return False
            
        # 2 检查nonce        
        if nonce != noncestr:         
            msg = "nonce 错误" + " ,客户端携带的nonce:" + nonce+ " ,全局变量中的nonce:" + noncestr
            # GAlogging.error(self.ip_port + msg + '\n Digiest : ' + digest)
            others = "nonce error"
            self.response_401(id, others, m_time)
            return False
        
        # 3 计算公式

        A1 = username + ":" + realm + ":" + self.get_device_password(id)
        A2 = "POST:" + uri

        m2 = hashlib.md5()
        m2.update(A1.encode('utf-8'))
        HA1 = m2.hexdigest()

        m2 = hashlib.md5()
        m2.update(A2.encode('utf-8'))
        HA2 = m2.hexdigest()

        response_str = HA1 + ":" + nonce + ":" + nc + ":" + cnonce + ":" + qop + ":" + HA2
        m2 = hashlib.md5()
        m2.update(response_str.encode('utf-8'))
        response_md5 = m2.hexdigest()
        # 4 判断计算得到的response与digest中值是否一样
        if response_md5 == response:
            # GAlogging.info(self.ip_port + '认证成功')
            return True
        errmsg = "response计算结果与客户端携带的不一样"        
        errmsg +="\n\t ,username={},realm={},uri={},nonce={},nc={},cnonce={},qop={}".format(username, realm, uri, nonce, nc, cnonce, qop)
        errmsg += "\n\t ,客户端携带response:" + response
        errmsg += "\n\t ,计算的response:" + response_md5
        # GAlogging.error(self.ip_port + errmsg + '\n' + " Digest: " + digest)      
        others = "Authentication failed"
        self.response_401(id, others, m_time)
        return False

    def check_regtime_auth(self, headers, ip_port, id, m_time, check_auth):
        # 检查全局变量中的注册时间 正常返回True， 错误返回False ，并回复401鉴权挑战 
        # 1, 获取当前时间id
        curtime = time.time()

        # 2, 获取id，注册时间
        if self.get_device_info(id) == None:  
            others = "not found DeviceID in System"
            self.response_200([''], others, "3", "/VIID/Syetem/Register", m_time)
            return False
        
        # 3 检查是否有注册时间
        regtime_1 = self.get_device_registertime(ip_port, id)
        if regtime_1 == None: 
            others = "not found %s registertime"%ip_port
            self.response_401(id, others, m_time)
            return False
        
        # 4 获取 注册时间 列表
        regtime = self.get_device_recordregtime(id)  
        if regtime == None: 
            others = "not found %s registertime list"%id
            self.response_401(id, others, m_time)
            return False
                  
        # 5 pc时间小于 注册时间 ， 删除该id的注册信息，重新注册
        if curtime < regtime:
            others = "pctime < registertime" 
            others += ", pctime:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(curtime)))
            others += ", registertime:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(regtime)))
            self.set_device_nonce(id, '')
            self.set_device_realm(id, '')
            print(f"{ip_port} + {others} +  , {id}注册信息已删除, 需要重新注册")
            self.response_401(id, others, m_time)                               
            return False            
        # 4，pc时间 比注册时间 超时，回复401鉴权挑战  
        delta_time = curtime - regtime
        if delta_time >= timeout:
            others = "pctime-registertime=%d >= %d s"%(delta_time, timeout)
            others += ", pctime:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(curtime)))
            others += ", registertime:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(regtime)))
            print(f"{ip_port}---------注册时间超时---------时间差：{delta_time}--超时时间:{timeout}--所有注册信息--{device_registerinfo}---")
            self.response_401(id, others, m_time)          
            return False            
        # 5, 每个消息都检查Auth
        if check_auth == True: 
            digest = headers.get("Authorization") 
            if digest == None:
                others = "not found Authorization"
                self.response_401(id, others, m_time) 
                return False           
            User_Identify = headers.get("User-Identify") 
            if User_Identify == None:
                others = "not found User_Identify"
                self.response_401(id, others, m_time) 
                return False               
            nonce = self.get_device_nonce(id)
            if nonce == None:
                others = "not found %s nonce"%id
                self.response_401(id, others, m_time) 
                return False
            # 检查认证是否成功
            if self.check_Authorization(id, digest, nonce, m_time) == False:
                return False
        else:
            User_Identify = headers.get("User-Identify") 
            if User_Identify == None:
                others = "not found User_Identify"
                self.response_401(id, others, m_time) 
                return False               
            nonce = self.get_device_nonce(id)
            if nonce == None:
                others = "not found %s nonce"%id
                self.response_401(id, others, m_time) 
                return False
        return True


    # @tornado.gen.coroutine  
    def read_httpContent(self, headers, m_uri, m_time):
        cont_length = headers.get("Content-Length")
        # 获取Content-Length的值  
        if cont_length == None:
            others = "not found Content-Length" 
            self.response_200( [''], others, "1", m_uri, m_time)
            return False
        elif int(cont_length) < 0:
            others = 'Content-Length=%d is error'%cont_length
            self.response_200( [''], others, "1", m_uri, m_time)
            return False
        return True
    
    #替换字符
    def replace_data_Str(self, json_data):
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == 'Data':
                    json_data[key] = 'base64'
                else:
                    self.replace_data_Str(value)
        elif isinstance(json_data, list):
            for item in json_data:
                self.replace_data_Str(item)
        return json_data
    
    #替换存图服务
    def save_Picture(self,file_path,binary_data):
        with open(file_path, 'wb') as file:
            file.write(binary_data) 
    
    def save_Json_dict(self,file_path,json_dict):
        with open(file_path, 'w') as json_file:
            json.dump(json_dict, json_file, indent=4)

    def CloseConn(self):
        if isCloseConn:
            self.finish()
            self.request.connection.stream.close()
        else:
           pass

    def result_Key(self, id, path):
        # Check if the specified key exists in the "result" dictionary
        device_registerinfo[id]["result"].setdefault(path, 1)

        # Increment the value corresponding to the specified key
        device_registerinfo[id]["result"][path] += 1

    #查询属性服务
    def get_Property(self, id, pkey):
        # Retrieve device information for the given 'id'
        device_info = self.get_device_info(id)

        # Check if the device information is not found
        if device_info is None:
            return False
        else:
            # Retrieve the property value for the specified key
            property_value = device_info.get('property', {}).get(pkey)

            # Return the property value (or None if not found)
            return property_value
        
    #设置属性服务
    def set_Property(self, id, pkey, value):
        # Retrieve device information for the given 'id'
        device_info = self.get_device_info(id)

        # Check if the device information is not found
        if device_info is None:
            return False

        # Update the property value
        device_info['property'][pkey] = value

        # Indicate that the property was successfully set
        return True

    #存储属性服务
    def save_Property(self, id, pkey, value):
        # Retrieve device information for the given 'id'
        ret = self.get_device_info(id)

        # Check if the device information is not found
        if ret is None:
            return False
        else:
            # Determine the maximum allowed size for the property based on 'pkey'
            if 'picList' == pkey:
                max_size = MAX_PICLIST_VOL
            else:
                max_size = MAX_JSONLIST_VOL

            # If the maximum size is 0, set it to a default value of 100
            if max_size == 0:
                max_size = 100

            # Check if the length of the property list exceeds the maximum size
            if len(device_registerinfo[id]['property'][pkey]) > max_size:
                # Remove the oldest element if the list exceeds the maximum size
                device_registerinfo[id]['property'][pkey].pop(0)

            # Insert the new 'value' into the property list
            # Ensure that the value is not inserted if it is a duplicate
            if value not in device_registerinfo[id]['property'][pkey]:
                device_registerinfo[id]['property'][pkey].append(value)

        # Indicate that the property was successfully saved
        return True
    
    def parse_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # 提取ID
        path_parts = parsed_url.path.split('/')
        id_value = None
        if len(path_parts) >= 3 and path_parts[1] == "images":
            id_value = path_parts[2]

        # 提取isSavePic和isSaveJson的值
        is_save_pic = query_params.get("isSavePic", [None])[0]
        is_save_json = query_params.get("isSaveJson", [None])[0]

        return id_value, is_save_pic, is_save_json
    # def start_scheduler(self):
    #     self.scheduler = BackgroundScheduler()  
    #     self.scheduler.add_job(self.check_HeartBeat, 'interval', seconds=5 )   
    #     self.scheduler.start()
    


class ERRORDataHandler(CommonHandler):
    async def post(self):
        headers = self.request.headers
        json_dict = json.loads(self.request.body.decode('utf-8'))
        content_length = headers.get('content-length')
        ip_port = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        others = "PathError:can't use root path"
        print(f"{locurtime}------->{ip_port}----->{self.request.uri} ---{content_length}------PathError:can't use root path-------------")
        self.response_400(ip_port, others)




class RegisterClientHandler(CommonHandler):
    '''
     函数post主入口  用来判断注册方向
    '''
    async def post(self, path):  
        headers = self.request.headers
        json_dict = json.loads(self.request.body.decode('utf-8'))
        ip_port = self.request.connection.context.address
        m_time = time.time()
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if path == "UnRegister": 
            # 处理UnRegister请求  
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** 注销 ***")
            self.process_unregister_request(ip_port,headers,json_dict,"/VIID/System/UnRegister", m_time)    

        elif path == "Register":
            # 处理Register请求  
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** 注册 ***")
            self.process_register_request(ip_port,headers,json_dict,"/VIID/System/Register", m_time)

        elif path == "Keepalive":  
            # 处理Keepalive请求
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** 心跳 ***")
            self.process_keepalive_request(ip_port,headers,json_dict,"/VIID/System/Keepalive", m_time)
            # self.write("处理Keepalive请求")  
        else:  
            # 处理其他路径的请求  
            self.write("未知路径，无法处理")  
            
    async def get(self, path): 
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headers = self.request.headers
        ip_port = self.request.connection.context.address
        LocalTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        if path == "Time":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** 校时 *** +\n {headers}")
            VIIDServerID = headers.get("User-Identify", "0")
            content_dict =  {
                "SystemTimeObject": {
                    "LocalTime": LocalTime,
                    "RequestURL": "/VIID/System/Time",
                    "TimeMode": 1,
                    "TimeZone": "Etc/GMT-8",
                    "VIIDServerID": VIIDServerID
                }
            }
            content_str = json.dumps(content_dict)
            content_len = len(content_str)
            header = {}
            header["Content-Type"] = "application/json; charset=utf-8" 
            GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
            header["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
            header["Connection"] = "close"
            header["Content-Length"] = str(content_len)
            infomsg = content_str
            if self.response_base(200, header, content_str):
                print(f"{locurtime}------->{ip_port} + 回复:  + {infomsg}")
            else:
                print(f"{locurtime}------->{ip_port} + 没有正确回复:  + {infomsg}")
        else:
            
            print(f"{locurtime}------->{ip_port}----<<<<<<<<<{path}>>>>>>>>>>")
            id = path
            ret = self.get_device_info(id)
            if None == ret:
                content_dict =  {
                        "device_registerinfo": device_registerinfo,
                }
            else:
                content_dict =  {
                        "device_registerinfo": ret,
                }
            content_str = json.dumps(content_dict)
            content_len = len(content_str)
            header = {}
            header["Content-Type"] = "application/json; charset=utf-8" 
            GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
            header["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
            header["Connection"] = "close"
            header["Content-Length"] = str(content_len)
            infomsg = content_str
            self.response_base(200, header, content_str)
            
    async def put(self, path):
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headers = self.request.headers
        ip_port = self.request.connection.context.address
        LocalTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        id = path
        if id.isdigit():
            ret = self.get_device_info(id)
            if ret == None:
                self.set_status(400)  # 设置响应状态码为 400 Bad Request
                self.write("PathError: wrong DeviceID")
                return
            else:
                body = self.request.body
                if not body:
                    self.set_status(400)  # 设置响应状态码为 400 Bad Request
                    self.write("Empty request body")
                    return
                # 如果消息体不为空，可以进行进一步的处理
                try:
                    # 解析 JSON 数据
                    data = tornado.escape.json_decode(body)
                    # 使用 get() 方法检查 'isSavePic' 是否是字典的键，并获取其对应的值
                    is_save_pic_value = data.get('isSavePic')
                    # 判断是否存在 'isSavePic' 键
                    if is_save_pic_value is not None:
                        print("isSavePic is present with value:", is_save_pic_value)
                        self.set_Property(id,'isSavePic',is_save_pic_value)
                    else:
                        print("isSavePic is not present in the dictionary")

                    is_save_json_value = data.get('isSaveJson')
                    # 判断是否存在 'isSaveJson' 键
                    if is_save_json_value is not None:
                        print("isSaveJson is present with value:", is_save_json_value)
                        self.set_Property(id,'isSaveJson',is_save_json_value)
                    else:
                        print("isSaveJson is not present in the dictionary")

                    self.set_status(200)  # 设置响应状态码为 400 Bad Request
                    self.write("success")
                    return
                except json.JSONDecodeError:
                    self.set_status(400)  # 设置响应状态码为 400 Bad Request
                    self.write("Invalid JSON format in request body")
                    return
 
        elif path == "isSavePic":
                body = self.request.body
                if not body:
                    self.set_status(400)  # 设置响应状态码为 400 Bad Request
                    self.write("Empty request body")
                    return
                try:
                    # 解析 JSON 数据
                    data = tornado.escape.json_decode(body)
                    # 使用 get() 方法检查 'isSavePic' 是否是字典的键，并获取其对应的值
                    is_save_pic_value = data.get('isSavePic')
                    # 判断是否存在 'isSavePic' 键
                    if is_save_pic_value is not None:
                        other = f"isSavePic is present with value: {is_save_pic_value}"
                        print(other)
                        # 检查目标键是否存在于字典中
                        for id in device_registerinfo:
                            # 获取目标键对应的字典
                            self.set_Property(id,'isSavePic',is_save_pic_value)
                    else:
                        other = "isSavePic is not present in the dictionary"
                        print(other)

                    self.set_status(200)  # 设置响应状态码为 400 Bad Request
                    self.write(other)
                    return
                except json.JSONDecodeError:
                    self.set_status(400)  # 设置响应状态码为 400 Bad Request
                    self.write("Invalid JSON format in request body")
                    return
        elif path == "isSaveJson":
                body = self.request.body
                if not body:
                    self.set_status(400)  # 设置响应状态码为 400 Bad Request
                    self.write("Empty request body")
                    return
                try:
                    # 判断是否存在 'isSaveJson' 键
                    is_save_json_value = data.get('isSaveJson')
                    # 判断是否存在 'isSaveJson' 键
                    if is_save_json_value is not None:
                        other = f"isSaveJson is present with value: {is_save_json_value}"
                        print(other)
                        # 检查目标键是否存在于字典中
                        for id in device_registerinfo:
                            # 获取目标键对应的字典
                            self.set_Property(id,'isSaveJson',is_save_json_value)
                    else:
                        other = "isSaveJson is not present in the dictionary"
                        print(other)
                    self.set_status(200)  # 设置响应状态码为 400 Bad Request
                    self.write(other)
                    return
                except json.JSONDecodeError:
                    self.set_status(400)  # 设置响应状态码为 400 Bad Request
                    self.write("Invalid JSON format in request body")
                    return
        else:
            self.set_status(400)  # 设置响应状态码为 400 Bad Request
            self.write("PathError: wrong path")
            return


    # @tornado.gen.coroutipptne  
    def process_register_request(self, ip_port, headers, json_dict, m_uri, m_time):
        # DeviceID = json_dict["RegisterObject"].get("DeviceID")
        # self.response_StatusObject(ip_port, DeviceID, m_uri, m_time)
        # return
        if False == self.read_httpContent(headers, m_uri, m_time):
            print("***************--read_httpContent--***********************")
            return False
        else:
            # 2，检查参数 RegisterObject DeviceID
            RegisterObject = json_dict.get("RegisterObject")
            if RegisterObject == None:
                others = "not found RegisterObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return
            DeviceID = json_dict["RegisterObject"].get("DeviceID")

            if DeviceID == None:
                others = "not found DeviceID in RegisterObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return
            
            if self.get_device_info(DeviceID) == None:
                others = "not found DeviceID in System"
                self.response_400(ip_port, others)
                return
            
            # 3， 检查 Authorization 判断
            digest = headers.get("Authorization") 
            if digest == None:
                print(f"{ip_port} + 没有携带授权信息")          
                self.del_device_registertime(DeviceID) # 删除 注册时间 registertime
                self.set_device_nonce(DeviceID, '')
                self.set_device_realm(DeviceID, '')     
                others = "删除注册时间，nonce"
                print(f"{ip_port} +  {others}")
                # 4，服务器回复401鉴权挑战 
                self.response_401(DeviceID, 'Authorization not in Register request', m_time)
                return 
            else:
                print(f"{ip_port} + ***有授权信息***") 
                # 5，判断 id 是否有效
                m_device_registerinfom = self.get_device_info(DeviceID)
                if None == m_device_registerinfom :
                    others = "%s not register" %DeviceID
                    self.response_401(DeviceID, others)
                    return
                # 6，判断 nonce
                nonce = self.get_device_nonce(DeviceID)
                if nonce == None:
                    others = "not found %s nonce"%DeviceID
                    self.response_401(DeviceID, others, m_time)
                    return   
                # 7，检查 认证 是否成功，如认   
                if self.check_Authorization(DeviceID, digest, nonce, m_time) == False:
                    return
                # 8，判断 注册时间
                if self.get_device_registertime(ip_port, DeviceID): # 如果有注册时间
                    curtime = time.time()
                    self.set_device_recordregtime(ip_port, DeviceID, curtime)
                    others = "更新注册时间列表:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(curtime)))
                    print(f"{ip_port} +  {others}")
                else:   # 没有注册时间
                    curtime = time.time()
                    self.set_device_registertime(ip_port, DeviceID, curtime)       # 设置注册时间
                    self.set_device_recordregtime(ip_port, DeviceID, curtime)
                    othersmsg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(curtime))
                    others = "设置注册时间:{}".format(othersmsg)
                    others += " , 更新注册时间列表:{}".format(othersmsg)
                    print(f"{ip_port} +  {others}")
                self.set_device_onlinestatus(ip_port, DeviceID, True)
                self.set_device_ip_port(DeviceID, ip_port)
                m_device_registerinfom = self.get_device_info(DeviceID)
                print(f"{ip_port} --process_register_request--> 所有注册信息:--{DeviceID}:->{m_device_registerinfom}---")
                # 9， 响应
                self.response_StatusObject(ip_port, DeviceID, m_uri, m_time)                
                return   
             
    # @tornado.gen.coroutine                      
    def process_keepalive_request(self, ip_port, headers, json_dict, m_uri, m_time):    
        # 处理 keepalive 请求            
        # 1, 读body数据， 没有读到 内部已经返回200 错误
        if False == self.read_httpContent(headers, m_uri, m_time):
            print("***************--read_httpContent--***********************")
            return False
        else:
           
            DeviceID = headers.get("User-Identify")
            if DeviceID == None:
                others = "not found DeviceID in RegisterObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return
            
            if self.get_device_info(DeviceID) == None:
                others = "not found DeviceID in System"
                self.response_400(ip_port, others)
                return
            
            # 2, 检查注册时间 和 认证
            if self.check_regtime_auth(headers, ip_port, DeviceID, m_time, False) == False:
                return
            # 3，检查参数 KeepaliveObject DeviceID
            KeepaliveObject = json_dict.get("KeepaliveObject")
            if KeepaliveObject == None:
                others = "not found KeepaliveObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return   
            DeviceID = json_dict["KeepaliveObject"].get("DeviceID")
            if DeviceID == None:
                others = "not found DeviceID in KeepaliveObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return
            # 4， 响应
            m_device_registerinfom = self.get_device_info(DeviceID)

            print(f"{ip_port} --process_keepalive_request--> 所有注册信息:--{DeviceID}:->{m_device_registerinfom}---")
            self.response_StatusObject(ip_port, DeviceID, m_uri, m_time)    
            return 
          
    # @tornado.gen.coroutine     
    def process_unregister_request(self, ip_port, headers, json_dict, m_uri, m_time):
        # 处理注销请求
        # 1, 读body数据， 没有读到 内部已经返回200 错误
        if False == self.read_httpContent(headers, m_uri, m_time):
            print("***************--read_httpContent--***********************")
     
        else:
            # 2，检查参数 UnRegisterObject DeviceID
            UnRegisterObject = json_dict.get("UnRegisterObject")
            if UnRegisterObject == None:
                others = "not found UnRegisterObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return   
            DeviceID = json_dict["UnRegisterObject"].get("DeviceID")
            if DeviceID == None:
                others = "not found DeviceID in UnRegisterObject"
                self.response_200([''], others, "8", m_uri, m_time)
                return  
            
            if self.get_device_info(DeviceID) == None:
                others = "not found DeviceID in System"
                self.response_400(ip_port, others)
                return   
            
            # 3， 检查 Authorization 判断
            digest = headers.get("Authorization") 
            if digest == None:
                print(f"{ip_port} + 没有携带授权信息")                 
                # 4, 服务器回复401鉴权挑战 
                self.response_401(DeviceID, 'Authorization not in UnRegister request', m_time) 
                return
            else:
                print(f"{ip_port} + ***有授权信息***")    
                # 5，判断 ip 是否注册
                if self.get_device_info(DeviceID) == None:
                    others = "%s not register"%DeviceID
                    self.response_400(ip_port, others)
                    return  
                # 6，判断 nonce
                nonce = self.get_device_nonce(DeviceID)
                if nonce == None:
                    others = "not found %s nonce"%DeviceID
                    self.response_401(DeviceID, others, m_time)
                    return   
                # 7，检查 认证 是否成功，如认证失败 内部返回401 重新认证
                if self.check_Authorization(DeviceID, digest, nonce, m_time) == False:
                    return    
                # 8，更新注销时间
                curtime = time.time()
                self.set_device_unregistertime(DeviceID, curtime) # 设置注销时间
                self.del_device_registertime(DeviceID) # 删除 注册时间 registertime
                self.set_device_nonce(DeviceID, '')
                self.set_device_realm(DeviceID, '')    
                others = "更新注销时间:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(curtime)))
                others += "删除注册时间，nonce"
                print(f"{ip_port} + ***{others}***") 
                # 9， 响应
                self.set_device_onlinestatus(ip_port, DeviceID, False)
                self.set_device_ip_port(DeviceID, '')
                
                m_device_registerinfom = self.get_device_info(DeviceID)
                print(f"{ip_port} --process_register_request--> 所有注册信息:--{DeviceID}:->{m_device_registerinfom}---")
                self.response_StatusObject(ip_port, DeviceID, m_uri, m_time)    
                return      


class ReceiveDataHandler(CommonHandler):
    async def post(self, path):
        if path == "VideoSlices" :
            m_case=("*** 上传自动采集视频片段 ***") 
        elif  path == "Images":
            m_case=("*** 上传自动采集图像 ***")
            # return 
        elif  path == "Files":
            m_case=("*** 上传自动采集文件 ***") 
            # return
        elif  path == "Persons":
            m_case=("*** 上传自动采集人员 ***") 
            # return
        elif  path == "Faces":
            m_case=("*** 上传自动采集人脸 ***")  
            # return
        elif  path == "MotorVehicles":
            m_case=("*** 上传自动采集机动车 ***")
            # return   
        elif  path == "NonMotorVehicles":
            m_case=("*** 上传自动采集非机动车 ***") 
            # return  
        elif  path == "Things":
            m_case=("*** 上传自动采集物品 ***")  
            # return
        elif  path == "Scenes":
            m_case=("***  上传自动采集场景 ***")
            # return        
        elif  path == "VideoLabels":
            m_case=("***  上传自动采集视频图像标签 ***")  
            # return
        elif  path == "AnalysisRules":
            m_case=("***  上传视频图像分析规则 ***")  
            # return
        else:
            m_case=(" ----------其他消息-------------")
        
        headers = self.request.headers
        json_dict = json.loads(self.request.body.decode('utf-8'))
        content_length = headers.get('content-length')
        ip_port = self.request.connection.context.address
        m_time = time.time()
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        print(f"{locurtime}------->{ip_port}----->{self.request.uri} ---------{m_case}---------{content_length}----")
        (DeviceID, m_uri, Reason) = self.process_data(path, ip_port, headers, json_dict, m_time)
        if DeviceID != False:
            await self.distribute_data(path, ip_port, headers, DeviceID, json_dict, m_time)
            self.result_Key(DeviceID,path)
            self.response_200([''], "Correct", "0", m_uri, m_time)
            print(f"{ip_port} +  ----------Correct----{m_uri}----{Reason}-----") 
        else:
            print(f"{ip_port} +  ----------Error-----{m_uri}----{Reason}-----") 

    async def get(self, path): 
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headers = self.request.headers
        ip_port = self.request.connection.context.address
        print(f"{locurtime}------->{ip_port} + *** GET *** +\n {headers}")
        if path == "Images":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 查询图像 ***")
        elif path == "VideoSlices":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 查询视频片段 ***")
        elif path == "APEs":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 查询采集设备 ***")
        elif path == "APSs":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 查询采集系统  ***")
        elif path == "Tollgates":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 查询视频卡口  ***")
        elif path == "Lanes":
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 查询车道  ***")
        else:
            print(f"{locurtime}------->{ip_port}----->{self.request.uri} *** GET ****** 其他GET消息 ***")

    def process_data(self, path, ip_port, headers, json_dict, m_time):
        # print(json_dict)
        m_uri = "http://localhost:{}/VIID/{}".format(PORT, path)

        # 1, 读body数据， 没有读到 内部已经返回200 错误
        if False == self.read_httpContent(headers, m_uri, m_time):
            print("***************--read_httpContent--***********************")
            return (False , m_uri, "Error_read_httpContent")
        else:
            # 检查参数 User-Identify: 35010201001320000008
            # RegisterObject = json_dict.get("RegisterObject")
            # if RegisterObject == None:
            #     others = "not found RegisterObject"
            #     self.response_200([''], others, "8", m_uri, m_time)
            #     return
            DeviceID = headers.get("User-Identify")
            ret = self.get_device_onlinestatus(ip_port, DeviceID)
            if "KeyError" == ret:
                others = "not found DeviceID in System"
                self.response_400(ip_port, others)
                return (False , m_uri, others)
            elif False == ret:
                others = "Device offline, please register again"
                self.response_401(DeviceID, others, m_time)
                return (False , m_uri, others)
            else:
                pass

            if DeviceID == None:
                others = "not found DeviceID in RegisterObject"
                self.response_200([''], others, "8", m_uri, m_time)
                print(f"{ip_port} +  ----------{others}-------------")
                return (False , m_uri, others)
            # 2, 检查注册时间 和 认证
            if self.check_regtime_auth(headers, ip_port, DeviceID, m_time, False) == False:
                others = "check_regtime_auth_Failed, please register again"
                return (False , m_uri, others)
            return (DeviceID , m_uri, "True")


    @tornado.gen.coroutine
    def distribute_data(self, path, ip_port, headers, deviceID, json_dict, m_time):

        m_uri = {
        "VideoSlices":["VideoSliceListObject","VideoSlice"]#上传自动采集视频片段 /
        ,"Images":["ImageListObject","Image"]#上传自动采集图像
        ,"Files":["FileListObject","File"]#上传自动采集文件
        ,"Persons":["PersonListObject","PersonObject"]#上传自动采集人员
        ,"Faces":["FaceListObject","FaceObject"]#上传自动采集人脸
        ,"MotorVehicles":["MotorVehicleListObject","MotorVehicleObject"]#上传自动采集机动车
        ,"NonMotorVehicles":["NonMotorVehicleListObject","NonMotorVehicleObject"] #上传自动采集非机动车 
        ,"Things":["ThingListObject","ThingObject"] #上传自动采集物品
        ,"Scenes":["SceneListObject","SceneObject"] #上传自动采集场景
        ,"VideoLabels":["VideoLabelListObject","VideoLabelObject"] #上传自动采集视频图像标签
        ,"AnalysisRules":["AnalysisRuleListObject","AnalysisRuleObject"]  #上传视频图像分析规则 
        ,"DispositionNotifications":["DispositionNotificationListObject","DispositionNotificationListObject"] #订阅通知
        ,"Subscribes":["SubscribeListObject","SubscribeListObject"] #批量订阅 
        ,"Dispositions":["DispositionListObject","DispositionObject"] #批量布控         
        ,"Cases":["CaseListObject","Case"] #批量视频案事件新增          
        ,"VideoSlices":["VideoSliceListObject","VideoSlice"] #批量创建人工采集视频片段
        ,"VideoImages":["VideoImageListObject","VideoImage"] #批量创建人工采集图像 
        ,"VideoFiles":["VideoFilesListObject","VideoFile"] #批量创建人工采集文件 
        ,"AuthImage":["1111","2222"] #图片防盗链配置
        }
        
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cont_length = headers.get("Content-Length")
        print(f"{locurtime}-->Client Address: {ip_port} --> 报文类型为：{path} content_length:{cont_length}")
        try:
            if  path == "Images":
                m_vol = {"PersonList":None,"FaceList":None,"MotorVehicleList":None,\
                        "NonMotorVehicleList":None,"ThingList":None,"SceneList":None}
                JsonObject=json_dict.get(m_uri.get(path)[0], {}).get(m_uri.get(path)[1], [{}])[0]
                # m_vol.update(JsonObject) //完全复制
                # 找到共同的键
                common_keys = set(JsonObject.keys()) & set(m_vol.keys())

                #主图提取信息
                main_EventSort=str(JsonObject['ImageInfo']['EventSort'])
                
                # 将dict1的值赋值给dict2
                for key in common_keys:
                    m_vol[key] = JsonObject[key]
                
                for key, value in m_vol.items():
                    locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sub_hasPic = False
                    if value == None:
                        continue
                    if key == "PersonList":
                        for item in value['PersonObject']:
                            if None != item.get('Data'):
                                sub_hasPic = True
                                sub_binary_data = base64.b64decode(JsonObject['Data'])

                            ChannleID=str(item['DeviceID'])
                            sub_EventSort=str(item['EventSort'])
                            ShotTime=str(item['BeginTime'])
                    elif key == "FaceList":
                        for item in value['FaceObject']:
                            if None != item.get('Data'):
                                sub_hasPic = True
                                sub_binary_data = base64.b64decode(JsonObject['Data'])

                            ChannleID=str(item['DeviceID'])
                            sub_EventSort=str(item['EventSort'])
                            ShotTime=str(item['BeginTime'])       
                    elif key == "MotorVehicleList":
                        for item in value['MotorVehicleObject']:
                            if None != item.get('Data'):
                                sub_hasPic = True
                                sub_binary_data = base64.b64decode(JsonObject['Data'])

                            ChannleID=str(item['DeviceID'])
                            sub_EventSort=str(item['EventSort'])
                            ShotTime=str(item['BeginTime'])
                    elif key == "NonMotorVehicleList":
                        for item in value['NonMotorVehicleObject']:
                            if None != item.get('Data'):
                                sub_hasPic = True
                                sub_binary_data = base64.b64decode(JsonObject['Data'])

                            ChannleID=str(item['DeviceID'])
                            sub_EventSort=str(item['EventSort'])
                            ShotTime=str(item['BeginTime'])
                    elif key == "ThingList":
                        for item in value['ThingObject']:
                            if None != item.get('Data'):
                                sub_hasPic = True
                                sub_binary_data = base64.b64decode(JsonObject['Data'])

                            ChannleID=str(item['DeviceID'])
                            sub_EventSort=str(item['EventSort'])
                            ShotTime=str(item['BeginTime'])
                    else: #key == "SceneList" :
                        for item in value['SceneObject']:
                            if None != item.get('Data'):
                                sub_hasPic = True
                                sub_binary_data = base64.b64decode(JsonObject['Data'])

                            ChannleID=str(item['DeviceID'])
                            sub_EventSort=str(item['EventSort'])
                            ShotTime=str(item['BeginTime'])

                    if(True == sub_hasPic):
                        filename = ChannleID + "_" + ShotTime + "_"+ main_EventSort + "_"+ sub_EventSort + "_" + g_Pictype
                        file_path = g_folder_full_path + "/" + str(deviceID) + "/"+ filename
                        self.save_Picture(file_path, sub_binary_data)
                        self.save_Property(deviceID,'picList',filename)
                        print(f"{locurtime}-->存储{path}消息体图片：Client Address: {ip_port} -->设备ID:{deviceID}，-->通道ID:{ChannleID}-->>>主类型:{EvertType_info.get(main_EventSort)}-->辅类型:{EvertType_info.get(sub_EventSort)}-->抓拍时间:{ShotTime}-->存图路径：{file_path}")
                    else:
                        print(f"{locurtime}--不存储{path}图片：Client Address: {ip_port} -->设备ID:{deviceID}，-->通道ID:{ChannleID}-->>>主类型:{EvertType_info.get(main_EventSort)}-->辅类型:{EvertType_info.get(sub_EventSort)}-->抓拍时间:{ShotTime}")
                
                #主图处理
                ShotTime= str(JsonObject['ImageInfo']['ShotTime'])
                if 'True' == self.get_Property(deviceID,'isSavePic') and isSavePic:
                    #场景图图片数据
                    main_binary_data = base64.b64decode(JsonObject['Data'])
                    filename = ChannleID + "_" + ShotTime + "_" + main_EventSort + "_" + g_Pictype
                    main_file_path = g_folder_full_path + "/" + str(deviceID) + "/" +  filename  
                    self.save_Picture(main_file_path, main_binary_data)
                    self.save_Property(deviceID,'picList',filename)
                    print(f"{locurtime}-->存储{path}图片：Client Address: {ip_port} -->设备ID:{deviceID}，-->通道ID:{ChannleID}-->>>主类型:{EvertType_info.get(main_EventSort)}-->抓拍时间:{ShotTime}-->存图路径：{main_file_path}")
                else:
                    print(f"{locurtime}-->不存储{path}图片：Client Address: {ip_port} -->设备ID:{deviceID}，-->通道ID:{ChannleID}-->>>主类型:{EvertType_info.get(main_EventSort)}-->抓拍时间:{ShotTime}")
            
            elif  path == "DispositionNotifications":
                JsonObject = json_dict.get(m_uri.get(path)[0], {}).get(m_uri.get(path)[1], [{}])[0]
                NotificationID=JsonObject.get('NotificationID')#该布控告警标识符
                DispositionID=JsonObject.get('DispositionID')#布控标识
                Title=JsonObject.get('Title')#描述布控的主题和目标
                TriggerTime=JsonObject.get('TriggerTime')#触发时间
                CntObjectID=JsonObject.get('CntObjectID')#自动采集过车或过人记录ID
                print(f"{locurtime}->不存储{path}图片：Client Address: {ip_port} -->NotificationID:{NotificationID}-->DispositionID:{DispositionID}-->Title:{Title}-->TriggerTime:{TriggerTime}-->CntObjectID:{CntObjectID}")
                pass
            else:
                JsonObject = json_dict.get(m_uri.get(path)[0], {}).get(m_uri.get(path)[1], [{}])[0]
                ChannleID=JsonObject.get('DeviceID')
                SubInfoObject=JsonObject['SubImageList']['SubImageInfoObject']
                for temp_Object in SubInfoObject:
                    main_EventSort=str(temp_Object['EventSort'])
                    ShotTime=str(temp_Object['ShotTime'])
                    mType=str(temp_Object['Type'])
                    if 'True' == self.get_Property(deviceID,'isSavePic') and isSavePic:
                        # 解码Base64数据
                        binary_data = base64.b64decode(temp_Object['Data'])
                        filename = ChannleID + "_" + ShotTime + "_"+ main_EventSort + "_"+ mType + g_Pictype
                        file_path = g_folder_full_path + "/" + str(deviceID) + "/" +  filename
                        self.save_Picture(file_path, binary_data)
                        self.save_Property(deviceID,'picList',filename)
                        print(f"{locurtime}-->存储{path}图片：Client Address: {ip_port} --> 设备ID:{deviceID},-->通道ID:{ChannleID}-->图片类型:{Image_Typeinfo.get(mType)}-->类型:{EvertType_info.get(main_EventSort)}-->抓拍时间:{ShotTime}-->存图路径：{file_path}")
                    else:
                        print(f"{locurtime}-->不存储{path}图片：Client Address: {ip_port} --> 设备ID:{deviceID},-->通道ID:{ChannleID}-->图片类型:{Image_Typeinfo.get(mType)}-->类型:{EvertType_info.get(main_EventSort)}-->抓拍时间:{ShotTime}")
        except:
            print(f"ERROR-------->{locurtime}-->Client Address: {ip_port} --> 报文类型为：{path}--->content_length:{cont_length}--->报文为：{json_dict}")
        
        if 'True' == self.get_Property(deviceID,'isSaveJson') and isSaveJson:
            final_json = self.replace_data_Str(json_dict)
            filename = ChannleID + "_" + ShotTime + "_" + main_EventSort + "_" + g_Logtype
            file_path = g_folder_full_path + "/" + str(deviceID) + "/" + filename
            self.save_Json_dict(file_path,final_json)
            self.save_Property(deviceID,'JSONList',filename)

class ImageHandler(CommonHandler):
    def get(self, filename):
        # 指定存储图片的目录
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_port = self.request.connection.context.address
        image_dir = g_folder_full_path
        m_URL=self.request.uri
        match = re.match(r"/images/(\d+)/(.+\.jpg)", m_URL)
        if match:
            image_id = match.group(1)
            image_filename = match.group(2)
            print(f"ImageHandler-------->{locurtime}-->Client Address: {ip_port} -->图片路径:{image_dir}-->网址路径：{m_URL}-->Image ID:, {image_id}-->Image Filename:, {image_filename}")

            # 拼接图片文件的完整路径
            full_path = os.path.join(image_dir, image_id, image_filename)

            # 检查文件是否存在
            if os.path.exists(full_path):
                # 设置响应头部信息
                self.set_header("Content-Type", "image/jpeg")  # 设置图片类型，根据实际情况修改
                self.set_header("Content-Disposition", "inline")
                
                # 读取图片并将其写入响应中
                with open(full_path, "rb") as f:
                    self.write(f.read())
            else:
                self.set_status(404)
                self.write("Image not found")
            return
        
        id_value, is_save_pic, is_save_json = self.parse_url(m_URL)
        print(f"ID: {id_value}, isSavePic: {is_save_pic}, isSaveJson: {is_save_json}")
        if id_value is None and is_save_pic is None and is_save_json is None:
            others = "PathError: wrong DeviceID"
            self.response_400(ip_port, others)
            return
    
        if id_value is None:
            if is_save_pic is not None:
                other = f"isSavePic is present with value: {is_save_pic}"
                print(other)
                # 检查目标键是否存在于字典中
                for id in device_registerinfo:
                    # 获取目标键对应的字典
                    self.set_Property(id,'isSavePic',is_save_pic)
                
                                # 判断是否存在 'isSaveJson' 键
            if is_save_json is not None:
                other = f"isSaveJson is present with value: {is_save_json}"
                print(other)
                # 检查目标键是否存在于字典中
                for id in device_registerinfo:
                    # 获取目标键对应的字典
                    self.set_Property(id,'isSaveJson',is_save_json)

            content_dict =  {
                        "device_registerinfo": device_registerinfo,
                }
            content_str = json.dumps(content_dict)
            content_len = len(content_str)
            header = {}
            header["Content-Type"] = "application/json; charset=utf-8" 
            GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
            header["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
            header["Connection"] = "close"
            header["Content-Length"] = str(content_len)
            infomsg = content_str
            self.response_base(200, header, content_str)
                    
        elif False == id_value.isdigit():
            others = "PathError: wrong DeviceID"
            self.response_400(ip_port, others)
            return
        
        else:
            ret = self.get_device_info(id_value)
            if ret == None:
                others = "PathError: wrong DeviceID"
                self.response_400(ip_port, others)
                return
            else:
                if is_save_pic is not None:
                    print("isSavePic is present with value:", is_save_pic)
                    self.set_Property(id_value,'isSavePic',is_save_pic)
                else:
                    print("isSavePic is not present in the dictionary")
                
                if is_save_json is not None:
                    print("isSaveJson is present with value:", is_save_json)
                    self.set_Property(id_value,'isSaveJson',is_save_json)
                else:
                    print("isSaveJson is not present in the dictionary")

                ret = self.get_device_info(id_value)

                content_dict =  {
                            "device_registerinfo": ret,
                    }
                content_str = json.dumps(content_dict)
                content_len = len(content_str)
                header = {}
                header["Content-Type"] = "application/json; charset=utf-8" 
                GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
                header["Date"] = time.strftime(GMT_FORMAT, time.localtime(time.time()))
                header["Connection"] = "close"
                header["Content-Length"] = str(content_len)
                infomsg = content_str
                self.response_base(200, header, content_str)


Storagepath = 2
def get_fileDir():
    # 获取操作系统类型
    if os.name == 'posix':  # 对于Linux和macOS，os.name返回'posix'
        # 在Linux中，'~/'代表用户的主目录（home目录）
        if Storagepath == 1:
            folder_path = os.path.expanduser("~")
        elif Storagepath == 2:#存储到当前脚本运行目录
            file_path = os.path.realpath(__file__)
            folder_path = os.path.dirname(file_path)
        elif Storagepath == 3:#存储到用户目录
            folder_path="other"#请填写绝对路径
        else:
            folder_path=None

    elif os.name == 'nt':  # 对于Windows，os.name返回'nt'
        if Storagepath == 1:
            folder_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        elif Storagepath == 2:#存储到当前脚本运行目录
        # 在Windows中，通常使用桌面的路径
            file_path = os.path.realpath(__file__)
            folder_path = os.path.dirname(file_path)
        elif Storagepath == 3:#存储到用户目录
            folder_path="other"#请填写绝对路径
        else:
            folder_path=None
    else:
        # 如果是其他操作系统，你可以进行相应的处理
        # folder_path = os.path.expanduser("~")
        print(f"系统未知错误：{os.name}")
        return NameError
    return folder_path



def fuc_mkdir():
    folder_path = get_fileDir()
    if(NameError == folder_path):
        return NameError
    else:
        pass

    # 创建文件夹
    folder_name = 'Pictures'
    folder_full_path = os.path.join(folder_path, folder_name)

    if not os.path.exists(folder_full_path):
        os.makedirs(folder_full_path)
        print(f"文件夹已创建在：{folder_full_path}")
        return folder_full_path
    else:
        print(f"文件夹已存在：{folder_full_path}")
        return folder_full_path

    
def fuc_mkfolders(m_path):
    global g_folder_full_path
    g_folder_full_path = m_path
    # 遍历字典的键
    for key in device_registerinfo.keys():
        # 使用键的名称创建文件夹
        tmp_path = os.path.join(m_path, key) 
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
            print(f"文件夹已创建在：{tmp_path}")
        else:
            print(f"文件夹已存在：{tmp_path}")

def check_file(file_list):
    
    # 判断文件是否存在  
    for file in file_list:  
        if os.path.exists(file):  
            print(f"------------------->{file} 存在")  
        else:  
            print(f"------------------->{file} 不存在")
            return False
    return True

def make_app():
    folder_path = get_fileDir()
    # 创建文件夹
    file_name = 'server.crt'
    ssl_cert = os.path.join(folder_path, file_name)
    file_name = 'server.key'
    ssl_key = os.path.join(folder_path, file_name)

    file_list = [ssl_cert, ssl_key] 
    if True == check_file(file_list):
        # 创建SSL上下文  
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)  
        ssl_context.load_cert_chain(certfile=ssl_cert, keyfile=ssl_key) 
        return tornado.web.Application([
            (r"/VIID/System/([^/]+)", RegisterClientHandler),
            (r"/VIID/([^/]+)", ReceiveDataHandler),
            (r"/images/(.*)", ImageHandler),  # 图片服务的路由规则
            (r"/.*", ERRORDataHandler),
        ], ssl_options=ssl_context)
    else:
        print("------------缺失密钥文件-------------")    
        return tornado.web.Application([
            (r"/VIID/System/([^/]+)", RegisterClientHandler),
            (r"/VIID/([^/]+)", ReceiveDataHandler),
            (r"/images(.*)", ImageHandler),  # 图片服务的路由规则
            (r"/.*", ERRORDataHandler),
        ])
    

if __name__ == "__main__":
    ret = fuc_mkdir()
    if(NameError == ret):
        exit()
    else:
        fuc_mkfolders(ret)
    
    app = make_app()
    app.listen(PORT)  # 监听端口 8888
    print(f"Server started on port {PORT}...")
    tornado.ioloop.IOLoop.current().start()
