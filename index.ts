var myDate = new Date();
let t = myDate.getTime()- 24 * 60*10000000;
let a1 = getFormatTime(t);


console.log(a1)

        
let a2 = myDate.getFullYear(); //获取完整的年份(4位,1970-????)
let a4 = myDate.getMonth(); //获取当前月份(0-11,0代表1月)
let a5 = myDate.getDate(); //获取当前日(1-31)
let a6 = myDate.getDay(); //获取当前星期X(0-6,0代表星期天)
let a7 = myDate.getTime(); //获取当前时间(从1970.1.1开始的毫秒数)
let a8 = myDate.getHours(); //获取当前小时数(0-23)
let a9 = myDate.getMinutes(); //获取当前分钟数(0-59)
let a0 = myDate.getSeconds(); //获取当前秒数(0-59)
let a11 = myDate.getMilliseconds(); //获取当前毫秒数(0-999)
let a12 = myDate.toLocaleDateString(); //获取当前日期

let a13 = myDate.toLocaleTimeString(); //获取当前时间
let a14 = myDate.toLocaleString(); //获取日期与时间



console.log("a2: " ,a2)
console.log("a4: " ,a4)
console.log("a5: " ,a5)
console.log("a6: " ,a6)
console.log("a7: " ,a7)
console.log("a8: " ,a8)
console.log("a9: " ,a9)
console.log("a0: " ,a0)
console.log("a11: " ,a11)
console.log("a12: " ,a12)
console.log("myDate: " ,myDate)
console.log("a13: " ,a13)
console.log("a14: " ,a14)


function getFormatTime(t: number) {
    // let _this = this;
        let nowDateTime = new Date();
        let leadTime = nowDateTime.getTime() - t;
        let lastMsgDate = new Date(t);
    
        // x(列表显示时间) = y(当前时间) - z(收到消息时间)。x的显示，均采用12小时制。
        // 1.收到消息的时间与当前时间在同一天，且间隔小于等于一分钟  「y(Y.M.D)=z(Y.M.D)，0min<x<=1min，x取分钟值」。显示格式：刚刚。
        // 2.收到消息的时间与当前时间在同一天，但间隔在1分钟到60分钟之间  「y(Y.M.D)=z(Y.M.D)，1min<x<60min，x取分钟值」。显示格式：x分钟前。
        // 3.收到消息的时间与当前时间在同一天，但间隔大于等于60分钟  「y(Y.M.D)=z(Y.M.D)。显示格式：上午 10:20。
        // 4.收到消息的时间是当前时间的前一天  「y(Y.M)=z(Y.M)，y(D)-z(D)=1」。显示格式：昨天。
        // 5.收到消息的时间是当前时间的前二到六天  「y(Y.M)=z(Y.M)，7>y(D)-z(D)>1」。显示格式：星期三。
        // 6.收到消息的时间早于当前时间的前七天  「y(Y.M.D)>z(Y.M.D)，y(D)-z(D)>=7」。显示格式：10/23。
        // 7.收到消息的时间与当前时间不在同一自然年  「y(Y)>z(Y)」。显示格式：2019/01/17 (YYYY/MM/DD)。
    
        let yesterday = new Date();
        yesterday.setTime(yesterday.getTime()-24*60*60*1000);
        let aWeekAgo = new Date();
        aWeekAgo.setTime(aWeekAgo.getTime()-24*60*60*1000);
    
        console.log('nowDateTime',
            nowDateTime.getFullYear(),
            nowDateTime.getMonth(),
            nowDateTime.getDate(),
            nowDateTime.getHours(),
            nowDateTime.getMinutes(),
            // nowDateTime.getTime(),
        );
    
        console.log('yesterday',
            yesterday.getFullYear(),
            yesterday.getMonth(),
            yesterday.getDate(),
            yesterday.getHours(),
            yesterday.getMinutes(),
            yesterday.getTime(), );
        console.log('aWeekAgo',
            aWeekAgo.getFullYear(),
            aWeekAgo.getMonth(),
            aWeekAgo.getDate(),
            aWeekAgo.getHours(),
            aWeekAgo.getMinutes(),
            aWeekAgo.getTime(), );
    
        console.log('lastMsgDate',
            lastMsgDate.getFullYear(),
            lastMsgDate.getMonth(),
            lastMsgDate.getDate(),
            lastMsgDate.getHours(),
            lastMsgDate.getMinutes(),
            // lastMsgDate
            );
        console.log('date');
        console.log('t', t);
        console.log('leadTime', leadTime,);
        let resultDateTimeStr = '';
        if(nowDateTime.getFullYear()!=lastMsgDate.getFullYear()){
            resultDateTimeStr = `${lastMsgDate.getFullYear().toString()}/${(lastMsgDate.getMonth()+1).toString()}/${lastMsgDate.getDate().toString()}`;
        }else if (aWeekAgo.getTime()-t > 0){
                resultDateTimeStr = `${(lastMsgDate.getMonth()+1).toString()}/${lastMsgDate.getDate().toString()}`;
        }else if (yesterday.getTime()-t > 0){
            let weekMap = ['星期天', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
            resultDateTimeStr = weekMap[lastMsgDate.getDay()]
        }else if (
            yesterday.getFullYear()==lastMsgDate.getFullYear() &&
            yesterday.getMonth()==lastMsgDate.getMonth() &&
            yesterday.getDate()==lastMsgDate.getDate()
        ){
            resultDateTimeStr = '昨天'
        }else if (
            nowDateTime.getFullYear()==lastMsgDate.getFullYear() &&
            nowDateTime.getMonth()==lastMsgDate.getMonth() &&
            nowDateTime.getDate()==lastMsgDate.getDate()
        ){
            if (leadTime < 1000 * 60) {
                resultDateTimeStr = '刚刚';
            } else if (leadTime >= 60 * 1000 && leadTime < 60 * 1000 * 60) {
                let m = Math.round(leadTime/(60 * 1000));
                resultDateTimeStr = `${m}分钟前`;
            }else{
                if (lastMsgDate.getHours()<12){
                    resultDateTimeStr = '上午 ' + lastMsgDate.getHours().toString + ':' + lastMsgDate.getMinutes().toString()
                }else {
                    resultDateTimeStr = '下午 ' + (lastMsgDate.getHours()-12).toString + ':' + lastMsgDate.getMinutes().toString()
                }
            }
        }
        console.log('resultDateTimeStr', resultDateTimeStr);
        return resultDateTimeStr;
    }
