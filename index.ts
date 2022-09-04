

let a1 = getFormatTime(1);


console.log(a1)


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
        // console.log('resultDateTimeStr', resultDateTimeStr);
        return resultDateTimeStr;
    }
