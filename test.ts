import pr from './comm'



let v =    [
            {
                "cnt": "7",
                "recType": null,
                "recTypeStr": null,
                "sum_price": "212.00"
            },
            {
                "cnt": "4",
                "recType": "4",
                "recTypeStr": "闯红灯",
                "sum_price": "224.00"
            },
            {
                "cnt": "2",
                "recType": "7",
                "recTypeStr": "逆行",
                "sum_price": "100.00"
            },
            {
                "cnt": "1",
                "recType": "24",
                "recTypeStr": "主驾驶员不系安全带",
                "sum_price": "8.00"
            }
        ]

let arr = [];

for (let i of v) {

	if(i.recTypeStr == null) {
		arr.push({
	        "cnt": i.cnt,
	        "recType": i.recType,
	        "recTypeStr": "无类型",
	        "sum_price": i.sum_price
		});
	} else {
		arr.push(i);
	}
}

pr(arr)