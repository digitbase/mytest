'''
作成日期： 2023年11月2日
作者：许能
功能：代码模仿http数据接收和图片存储
    仅用于设备的接收

    存储路径默认存储在：linux home目录 或者是  Storagepath 根据变量去修改
    windows：在桌面
    请根据自己的需求修改路径
    路径修改的地点：fuc_mkdir()

'''

import tornado.ioloop
import tornado.web
from tornado import gen
import json
import datetime 
import logging
import base64
import os
import ssl



'''
修改区域
'''
isSavePic=False #是否存储图片
g_Pictype=".jpg"  #图片存储后缀
HTTP_PORT="8092" #http的端口
HTTPS_PORT="8093" #https的端口


'''
g_folder_full_path  不修改
EvertType_info  新增扩展字段时候添加

'''

g_folder_full_path=""  #存储路径，不做修改仅仅用于变量

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
    def save_Picture(self,file_path,binary_data):
        if isSavePic == True:
            print(f"---->存储图片，存图路径{file_path}")
            with open(file_path, 'wb') as file:
                file.write(binary_data) 
        else:
            print(f"---->不存图，存图路径{file_path}")
    def info_print(self,locurtime,client_address,port,fun_name, m_uri):
        print(f"{locurtime}-->Client Address: {client_address} ---访问端口:-{port}--入口：-{fun_name}------Request URI:----{m_uri}---------")


    @gen.coroutine
    def process_data(self, client_address, content_length , post_data):
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            json_data = json.loads(post_data)
            # print(json_data)
            key = next(iter(json_data.keys()))  #返回json的第一个键值
            lengthbody = len(post_data)
            content_length =  int(content_length)
            delta = content_length - lengthbody
            print(f"{locurtime}-->Client Address: {client_address} --> 报文类型为：{key} content_length:{content_length} 计算body：{lengthbody} 差值:{delta}")
            if 'SceneListObject' == key:
                SceneObject = json_data.get('SceneListObject', {}).get('SceneObject', [{}])[0]
                DeviceID=SceneObject['DeviceID']
                # RtspStreamAddress=SceneObject['RtspStreamAddress']
                SubImageInfoObject=SceneObject['SubImageList']['SubImageInfoObject']
                for temp_SubImageInfoObject in SubImageInfoObject:
                    EventSort=str(temp_SubImageInfoObject['EventSort'])
                    ShotTime=str(temp_SubImageInfoObject['ShotTime'])
                    mType=str(temp_SubImageInfoObject['Type'])
                    # 解码Base64数据
                    binary_data = base64.b64decode(temp_SubImageInfoObject['Data'])
                    file_path = g_folder_full_path + "/" + ShotTime + "_"+ EventSort + "_"+ mType + g_Pictype
                    self.save_Picture(file_path, binary_data)
                    print(f"{locurtime}-->Client Address: {client_address} --> 设备ID:{DeviceID}-->类型:{EvertType_info.get(EventSort)}-存储图片类型:{Image_Typeinfo.get(mType)}->抓拍时间:{ShotTime}")


                # print("SceneListObject")
            elif 'PersonListObject' == key:
                PersonObject = json_data.get('PersonListObject', {}).get('PersonObject', [{}])[0]
                DeviceID=PersonObject['DeviceID']
                # RtspStreamAddress=PersonObject['RtspStreamAddress']
                SubImageInfoObject=PersonObject['SubImageList']['SubImageInfoObject']
                for temp_SubImageInfoObject in SubImageInfoObject:
                    EventSort=str(temp_SubImageInfoObject['EventSort'])
                    ShotTime=str(temp_SubImageInfoObject['ShotTime'])
                    mType=str(temp_SubImageInfoObject['Type'])
                    # 解码Base64数据
                    binary_data = base64.b64decode(temp_SubImageInfoObject['Data'])
                    file_path = g_folder_full_path + "/" + ShotTime + "_"+ EventSort + "_"+ mType + g_Pictype
                    self.save_Picture(file_path, binary_data)
                    print(f"{locurtime}-->Client Address: {client_address} --> 设备ID:{DeviceID}-->类型:{EvertType_info.get(EventSort)}-存储图片类型:{Image_Typeinfo.get(mType)}->抓拍时间:{ShotTime}")
                     
                # print("PersonListObject")
            elif 'FaceListObject' == key:
                FaceObject = json_data.get('FaceListObject', {}).get('FaceObject', [{}])[0]
                DeviceID=FaceObject['DeviceID']
                # RtspStreamAddress=FaceObject['RtspStreamAddress']
                SubImageInfoObject=FaceObject['SubImageList']['SubImageInfoObject']
                for temp_SubImageInfoObject in SubImageInfoObject:
                    EventSort=str(temp_SubImageInfoObject['EventSort'])
                    ShotTime=str(temp_SubImageInfoObject['ShotTime'])
                    mType=str(temp_SubImageInfoObject['Type'])
                    # 解码Base64数据
                    binary_data = base64.b64decode(temp_SubImageInfoObject['Data'])
                    file_path = g_folder_full_path + "/" + ShotTime + "_"+ EventSort + "_"+ mType + g_Pictype
                    self.save_Picture(file_path, binary_data)
                    print(f"{locurtime}-->Client Address: {client_address} --> 设备ID:{DeviceID}-->类型:{EvertType_info.get(EventSort)}-存储图片类型:{Image_Typeinfo.get(mType)}->抓拍时间:{ShotTime}")

                # print("FaceListObject")
                # print(json_data)
            elif 'MotorVehicleListObject' == key:
                MotorVehicleObject = json_data.get('MotorVehicleListObject', {}).get('MotorVehicleObject', [{}])[0]
                DeviceID=MotorVehicleObject['DeviceID']
                # RtspStreamAddress=FaceObject['RtspStreamAddress']
                SubImageInfoObject=MotorVehicleObject['SubImageList']['SubImageInfoObject']
                for temp_SubImageInfoObject in SubImageInfoObject:
                    EventSort=str(temp_SubImageInfoObject['EventSort'])
                    ShotTime=str(temp_SubImageInfoObject['ShotTime'])
                    mType=str(temp_SubImageInfoObject['Type'])
                    # 解码Base64数据
                    binary_data = base64.b64decode(temp_SubImageInfoObject['Data'])
                    file_path = g_folder_full_path + "/" + ShotTime + "_"+ EventSort + "_"+ mType + g_Pictype
                    self.save_Picture(file_path, binary_data)
                    print(f"{locurtime}-->Client Address: {client_address} --> 设备ID:{DeviceID}-->类型:{EvertType_info.get(EventSort)}-存储图片类型:{Image_Typeinfo.get(mType)}->抓拍时间:{ShotTime}")
                # print("FaceListObject")
                # print(json_data) 

            elif 'VideoLabelListObject' == key:
                VideoLabelObject = json_data.get('VideoLabelListObject', {}).get('VideoLabelObject', [{}])[0]
                DeviceID=VideoLabelObject['DeviceID']
                # RtspStreamAddress=FaceObject['RtspStreamAddress']
                SubImageInfoObject=VideoLabelObject['SubImageList']['SubImageInfoObject']
                for temp_SubImageInfoObject in SubImageInfoObject:
                    EventSort=str(temp_SubImageInfoObject['EventSort'])
                    ShotTime=str(temp_SubImageInfoObject['ShotTime'])
                    mType=str(temp_SubImageInfoObject['Type'])
                    
                    # 解码Base64数据
                    binary_data = base64.b64decode(temp_SubImageInfoObject['Data'])
                    file_path = g_folder_full_path + "/" + ShotTime + "_"+ EventSort + "_"+ mType + g_Pictype
                    self.save_Picture(file_path, binary_data)
                    print(f"{locurtime}-->Client Address: {client_address} --> 设备ID:{DeviceID}-->类型:{EvertType_info.get(EventSort)}-存储图片类型:{Image_Typeinfo.get(mType)}->抓拍时间:{ShotTime}")
                     
                # print("FaceListObject")
                # print(json_data) 
            else:
                # MotorVehicleListObject
                print(f"{locurtime}-->invalid case")

        except Exception as e:
            print(f"{locurtime}-->问题数据包{post_data} 问题数据长度：{len(post_data)}")
            logging.error(f"{locurtime}-->解析请求数据中的JSON失败{e}")


class http_AiotReceiveDataHandler(CommonHandler):
    async def post(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTP_PORT,"POST http_AiotReceiveDataHandler", self.request.uri)
        # 发送200 OK响应和指定的消息
        response_message = {"message": "http:// POST http_AiotReceiveDataHandler request handled Success"} 
        self.set_status(200)
        self.write(response_message)
        pass

    async def get(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTP_PORT,"Get http_AiotReceiveDataHandler", self.request.uri)
        response_message = {"message": "http:// Get http_AiotReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

class http_RootReceiveDataHandler(CommonHandler):
    async def post(self):
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 接收POST请求中的数据
        post_data = self.request.body.decode('utf-8')
        content_length = self.request.headers['content-length']
        client_address = self.request.connection.context.address
        # 异步处理接收到的数据
        self.info_print(locurtime,client_address,HTTP_PORT,"POST http_RootReceiveDataHandler", self.request.uri)      
        await self.process_data(client_address, content_length, post_data)
        # 发送200 OK响应和指定的消息
        response_message = {"message": "http:// POST http_RootReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)
    
    async def get(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTP_PORT,"Get http_RootReceiveDataHandler", self.request.uri)
        response_message = {"message": "http:// Get http_RootReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

class http_ReceiveDataHandler(CommonHandler):
    async def post(self):
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 接收POST请求中的数据
        post_data = self.request.body.decode('utf-8')
        content_length = self.request.headers['content-length']
        client_address = self.request.connection.context.address
        # 异步处理接收到的数据
        self.info_print(locurtime,client_address,HTTP_PORT,"POST http_ReceiveDataHandler", self.request.uri)      
        await self.process_data(client_address, content_length, post_data)
        # 发送200 OK响应和指定的消息
        response_message = {"message": "http:// POST http_ReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

    async def get(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTP_PORT,"Get http_RootReceiveDataHandler", self.request.uri)
        response_message = {"message": "http:// Get http_ReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)


class https_AiotReceiveDataHandler(CommonHandler):
    async def post(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTPS_PORT,"POST https_AiotReceiveDataHandler", self.request.uri)
        # 发送200 OK响应和指定的消息
        response_message = {"message": "https:// POST https_AiotReceiveDataHandler request handled Success"} 
        self.set_status(200)
        self.write(response_message)
        pass

    async def get(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTPS_PORT,"Get https_AiotReceiveDataHandler", self.request.uri)
        response_message = {"message": "https:// Get https_AiotReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

class https_RootReceiveDataHandler(CommonHandler):
    async def post(self):
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 接收POST请求中的数据
        post_data = self.request.body.decode('utf-8')
        content_length = self.request.headers['content-length']
        client_address = self.request.connection.context.address
        # 异步处理接收到的数据
        self.info_print(locurtime,client_address,HTTPS_PORT,"POST https_RootReceiveDataHandler", self.request.uri)
        await self.process_data(client_address, content_length, post_data)

        # 发送200 OK响应和指定的消息
        response_message = {"message": "https:// POST https_RootReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)
    
    async def get(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTPS_PORT,"Get https_RootReceiveDataHandler", self.request.uri)
        response_message = {"message": "https:// Get https_RootReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

class https_ReceiveDataHandler(CommonHandler):
    async def post(self):
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 接收POST请求中的数据
        post_data = self.request.body.decode('utf-8')
        content_length = self.request.headers['content-length']
        client_address = self.request.connection.context.address
        # 异步处理接收到的数据
        # await self.process_data(self.request.remote_ip, post_data)
        self.info_print(locurtime,client_address,HTTPS_PORT,"POST https_ReceiveDataHandler", self.request.uri)
        await self.process_data(client_address, content_length, post_data)


        # 发送200 OK响应和指定的消息
        response_message = {"message": "https:// POST https_ReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

    async def get(self):
        client_address = self.request.connection.context.address
        locurtime  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_print(locurtime,client_address,HTTPS_PORT,"GET https_ReceiveDataHandler", self.request.uri)
        response_message = {"message": "https:// Get https_ReceiveDataHandler request handled Success"} 
        self.set_header('Connection', 'Keep-Alive')
        self.set_status(200)
        self.write(response_message)

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
    # 遍历字典的键
    global g_folder_full_path
    g_folder_full_path = m_path


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
        ssl._create_default_https_context = ssl._create_unverified_context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)  
        ssl_context.load_cert_chain(certfile=ssl_cert, keyfile=ssl_key) 
        
        return (tornado.web.Application([
            (r"/aiot/api/.*", http_AiotReceiveDataHandler),
            (r"/aiot/api/.*", https_AiotReceiveDataHandler, {"ssl_options": ssl_context}),
            (r"/.*", http_ReceiveDataHandler),
            (r"/.*", https_ReceiveDataHandler, {"ssl_options": ssl_context}),
            (r"/", http_RootReceiveDataHandler),
            (r"/", https_RootReceiveDataHandler, {"ssl_options": ssl_context}),
        ]),ssl_context)
    else:
        print("------------缺失密钥文件-------------")
        return (tornado.web.Application([
            (r"/aiot/api/.*", http_AiotReceiveDataHandler),
            (r"/AiEvent/.*", http_ReceiveDataHandler),
            (r"/", http_RootReceiveDataHandler),
        ]),"NONE")

if __name__ == "__main__":

    ret = fuc_mkdir()
    if(NameError == ret):
        exit()
    else:
        fuc_mkfolders(ret)

    (app,ssl_context) = make_app()
    if("NONE" != ssl_context):
        app.listen(HTTP_PORT)
        app.listen(HTTPS_PORT, ssl_options=ssl_context)
        print(f"Server started on port http服务 {HTTP_PORT}.and.https服务{HTTPS_PORT}.")
    else:
        app.listen(HTTP_PORT)
        print(f"Server started on port http服务 {HTTP_PORT}.and.无法正确启动https服务{HTTPS_PORT}.")

    tornado.ioloop.IOLoop.current().start()
