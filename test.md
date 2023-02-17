
## 主机
- 10.200.52.236
- /data/liugang/hc-production-screen  项目目录
- ./ODB 后端目录
- ./web 前端目录 
- 访问地址：http://10.200.52.236:8051 user:admin pwd:liugang

## 数据库

```
MYDB_HOST=10.200.52.222
MYDB_PORT=3306
MYDB_DATABASE=hc_proscreen
MYDB_USERNAME=hc_proscreen
MYDB_PASSWORD=*3oNoNz,bi-::
```

- [pro_day__cst] #生产日数据表

- [pro_setmonth__cst] #生产月计划表

## 开发环境
- package.json #启动角本

- npm install  #安装依赖

- npm run build #编辑打包


## 运行程序


- pm2 start hc-production-ODB #启动服务
- pm2 list #显示服务列表
- pm2 restart hc-production-ODB  #重启服务


## 后台程序
- 数据库配置文件

  .env.production
  ```
  # <AB> 广钢能环管理系统
    DB_AB_HOST=10.200.17.71
    DB_AB_PORT=1522
    DB_AB_DATABASE=fgemsrun


  # <AC> 广钢物流管理系统
    DB_AC_HOST=10.200.16.14
    DB_AC_PORT=1521
    DB_AC_DATABASE=orcl

    .........
  ```

- 程序初使化文件
  
  app.module.ts
  ```
    1.数据库连接
  
    2.cron每小时采集设置
    
    @Cron(CronExpression.EVERY_HOUR, { name: 'get_data_from_db' })
    readDB() {
      let input : Input01 = {
        type:"now"
      }
      pr('cron start get_data_from_db',1122)
      new InsertOneDay().run(input)  <==== [读取数据,入口文件]
  ```

- 生产名称定义文件

  ./src/modules/proscreen_app/hw/public/service/proDay_add.ts

  ```
  #各分项名
  var inName = ["YLMT_101", "YLMT_102", "YLMT_103", "SJC_SJ", .....

  #各厂名
  var inName2 = ["SJC","JHC","LTC","LGC","BXC","RZC","LZC","DLC","CPMT_SUM","YLMT_SUM"]

  #中文对应
  export const nameArray = new Map();
  nameArray.set("YLMT_101", "原料码头101")
  nameArray.set("YLMT_102", "原料码头102")
  nameArray.set("YLMT_103", "原料码头103")
  .......


  #求合关系
  var allArray = []
  allArray.push({ key: "SJC", value: ["SJC_SJ", "SJC_QT"] });//烧结厂
  allArray.push({ key: "JHC", value: ["JHC_JT"] });//焦化厂

  ```
- 生产数据SQL请求定义汇总

  ./src/modules/proscreen_app/controller/proinfo/proinfo.controller.ts
  ```
  @ApiOperation({ summary: "a7" })
	@Get("/proDay/A7/query")
	async queryA7(@Query() input: ActionInput) {
		return await new A7Query().run(input);
  }

  @ApiOperation({ summary: "a0" })
	@Get("/proDay/A0/query")
	async queryA0(@Query() input: ActionInput) {
		return await new A0Query().run(input);
  }

  .........
  ```
## 接口API
```
#Insert 请求当天前一天数据,并插入数据库
/Production_Screen/2.0.0/proDay/insertOneDay?type=now

#Insert 请求多天数据,并插入数据库
/Production_Screen/2.0.0/proDay/insertDays?startDate=2022-1-1&endDate=2023-1-1

#Insert 请求某月生产计划,并插入数据库
/Production_Screen/2.0.0/proDay/planA1?queryDay=2022-12-01

#Query 全厂,当天所有数据
/Production_Screen/2.0.0/proDay/queryOneDay?queryDay=2023-01-01

#Query 全厂,多天所有数据
/Production_Screen/2.0.0/proDay/queryAllSUM?startDate=2022-12-01&endDate=2022-12-08

#Query 全厂,某月生产计划
/Production_Screen/2.0.0/proDay/queryPlan?queryDay=2022-11-08

#Query 分厂,某年生产总合
/Production_Screen/2.0.0/proDay/show/year/query?year=2023&name=YLMT

#Query 分厂,各月生产,加计划,完成率
/Production_Screen/2.0.0/proDay/show/day/query?startDay=2022-12-18&endDay=2023-01-16&name=LZC

#Query 分厂,各日生产,加计划,完成率
/Production_Screen/2.0.0/proDay/show/day/query?startDay=2022-12-18&endDay=2023-01-16&name=LZC

#Query 分厂,多年生产总合
/Production_Screen/2.0.0/proDay/show/some_year/query?startYear=2018&endYear=2023&name=SJC

```

