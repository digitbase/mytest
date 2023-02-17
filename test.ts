function pr(input: any, type2?: number|string): void {
if (typeof type2 == "string") {
console.log(`///////////////////` ,type2, ' : ==>', input ,`///////////////////`);
} else {
console.log(typeof input, '==>', input);  
}
let _type = type2 ? type2 : 0;
let str = '';
if (_type > 0) {
for (let i = 0; i < 10; i++) str += _type.toString() + ' ';
console.log(`===========================    ${str}    =========================`);
}
}


var data =  [
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 15",
            "period_hour": "15",
            "person_type": "PEOPLE",
            "total_enters": "198",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 15",
            "period_hour": "15",
            "person_type": "STAFF",
            "total_enters": "76",
            "total_exits": "23"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 15",
            "period_hour": "15",
            "person_type": "VISITOR",
            "total_enters": "53",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 16",
            "period_hour": "16",
            "person_type": "PEOPLE",
            "total_enters": "45",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 16",
            "period_hour": "16",
            "person_type": "STAFF",
            "total_enters": "88",
            "total_exits": "48"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 16",
            "period_hour": "16",
            "person_type": "VISITOR",
            "total_enters": "19",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 17",
            "period_hour": "17",
            "person_type": "PEOPLE",
            "total_enters": "79",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 17",
            "period_hour": "17",
            "person_type": "STAFF",
            "total_enters": "88",
            "total_exits": "45"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 17",
            "period_hour": "17",
            "person_type": "UNKNOWN",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 17",
            "period_hour": "17",
            "person_type": "VISITOR",
            "total_enters": "8",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 18",
            "period_hour": "18",
            "person_type": "PEOPLE",
            "total_enters": "82",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 18",
            "period_hour": "18",
            "person_type": "STAFF",
            "total_enters": "90",
            "total_exits": "83"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 18",
            "period_hour": "18",
            "person_type": "VISITOR",
            "total_enters": "7",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 19",
            "period_hour": "19",
            "person_type": "PEOPLE",
            "total_enters": "106",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 19",
            "period_hour": "19",
            "person_type": "STAFF",
            "total_enters": "63",
            "total_exits": "46"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 19",
            "period_hour": "19",
            "person_type": "VISITOR",
            "total_enters": "6",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 20",
            "period_hour": "20",
            "person_type": "PEOPLE",
            "total_enters": "43",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 20",
            "period_hour": "20",
            "person_type": "STAFF",
            "total_enters": "40",
            "total_exits": "36"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 20",
            "period_hour": "20",
            "person_type": "VISITOR",
            "total_enters": "2",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 21",
            "period_hour": "21",
            "person_type": "PEOPLE",
            "total_enters": "24",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 21",
            "period_hour": "21",
            "person_type": "STAFF",
            "total_enters": "28",
            "total_exits": "14"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 22",
            "period_hour": "22",
            "person_type": "PEOPLE",
            "total_enters": "60",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 22",
            "period_hour": "22",
            "person_type": "STAFF",
            "total_enters": "33",
            "total_exits": "5"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 22",
            "period_hour": "22",
            "person_type": "VISITOR",
            "total_enters": "2",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 23",
            "period_hour": "23",
            "person_type": "PEOPLE",
            "total_enters": "134",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 23",
            "period_hour": "23",
            "person_type": "STAFF",
            "total_enters": "63",
            "total_exits": "16"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-14 23",
            "period_hour": "23",
            "person_type": "VISITOR",
            "total_enters": "5",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 00",
            "period_hour": "00",
            "person_type": "PEOPLE",
            "total_enters": "12",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 00",
            "period_hour": "00",
            "person_type": "STAFF",
            "total_enters": "41",
            "total_exits": "5"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 01",
            "period_hour": "01",
            "person_type": "PEOPLE",
            "total_enters": "9",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 01",
            "period_hour": "01",
            "person_type": "STAFF",
            "total_enters": "17",
            "total_exits": "4"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 02",
            "period_hour": "02",
            "person_type": "PEOPLE",
            "total_enters": "8",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 02",
            "period_hour": "02",
            "person_type": "STAFF",
            "total_enters": "7",
            "total_exits": "1"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 03",
            "period_hour": "03",
            "person_type": "PEOPLE",
            "total_enters": "3",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 03",
            "period_hour": "03",
            "person_type": "STAFF",
            "total_enters": "3",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 04",
            "period_hour": "04",
            "person_type": "PEOPLE",
            "total_enters": "9",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 04",
            "period_hour": "04",
            "person_type": "STAFF",
            "total_enters": "5",
            "total_exits": "1"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 04",
            "period_hour": "04",
            "person_type": "VISITOR",
            "total_enters": "3",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 05",
            "period_hour": "05",
            "person_type": "PEOPLE",
            "total_enters": "12",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 05",
            "period_hour": "05",
            "person_type": "STAFF",
            "total_enters": "2",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 05",
            "period_hour": "05",
            "person_type": "VISITOR",
            "total_enters": "14",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 06",
            "period_hour": "06",
            "person_type": "PEOPLE",
            "total_enters": "330",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 06",
            "period_hour": "06",
            "person_type": "STAFF",
            "total_enters": "8",
            "total_exits": "1"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 06",
            "period_hour": "06",
            "person_type": "VISITOR",
            "total_enters": "64",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 07",
            "period_hour": "07",
            "person_type": "PEOPLE",
            "total_enters": "1547",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 07",
            "period_hour": "07",
            "person_type": "STAFF",
            "total_enters": "95",
            "total_exits": "7"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 07",
            "period_hour": "07",
            "person_type": "VISITOR",
            "total_enters": "199",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 08",
            "period_hour": "08",
            "person_type": "PEOPLE",
            "total_enters": "177",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 08",
            "period_hour": "08",
            "person_type": "STAFF",
            "total_enters": "53",
            "total_exits": "10"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 08",
            "period_hour": "08",
            "person_type": "VISITOR",
            "total_enters": "69",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 09",
            "period_hour": "09",
            "person_type": "PEOPLE",
            "total_enters": "72",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 09",
            "period_hour": "09",
            "person_type": "STAFF",
            "total_enters": "17",
            "total_exits": "12"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 09",
            "period_hour": "09",
            "person_type": "VISITOR",
            "total_enters": "32",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 10",
            "period_hour": "10",
            "person_type": "PEOPLE",
            "total_enters": "38",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 10",
            "period_hour": "10",
            "person_type": "STAFF",
            "total_enters": "20",
            "total_exits": "11"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 10",
            "period_hour": "10",
            "person_type": "VISITOR",
            "total_enters": "18",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 11",
            "period_hour": "11",
            "person_type": "PEOPLE",
            "total_enters": "83",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 11",
            "period_hour": "11",
            "person_type": "STAFF",
            "total_enters": "34",
            "total_exits": "23"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 11",
            "period_hour": "11",
            "person_type": "VISITOR",
            "total_enters": "16",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 12",
            "period_hour": "12",
            "person_type": "PEOPLE",
            "total_enters": "149",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 12",
            "period_hour": "12",
            "person_type": "STAFF",
            "total_enters": "40",
            "total_exits": "30"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 12",
            "period_hour": "12",
            "person_type": "VISITOR",
            "total_enters": "13",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 13",
            "period_hour": "13",
            "person_type": "PEOPLE",
            "total_enters": "357",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 13",
            "period_hour": "13",
            "person_type": "STAFF",
            "total_enters": "35",
            "total_exits": "15"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 13",
            "period_hour": "13",
            "person_type": "VISITOR",
            "total_enters": "66",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 14",
            "period_hour": "14",
            "person_type": "PEOPLE",
            "total_enters": "227",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 14",
            "period_hour": "14",
            "person_type": "STAFF",
            "total_enters": "46",
            "total_exits": "26"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 14",
            "period_hour": "14",
            "person_type": "VISITOR",
            "total_enters": "58",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 15",
            "period_hour": "15",
            "person_type": "PEOPLE",
            "total_enters": "161",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 15",
            "period_hour": "15",
            "person_type": "STAFF",
            "total_enters": "85",
            "total_exits": "19"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 15",
            "period_hour": "15",
            "person_type": "VISITOR",
            "total_enters": "42",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 16",
            "period_hour": "16",
            "person_type": "PEOPLE",
            "total_enters": "59",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 16",
            "period_hour": "16",
            "person_type": "STAFF",
            "total_enters": "65",
            "total_exits": "31"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 16",
            "period_hour": "16",
            "person_type": "VISITOR",
            "total_enters": "37",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 17",
            "period_hour": "17",
            "person_type": "PEOPLE",
            "total_enters": "88",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 17",
            "period_hour": "17",
            "person_type": "STAFF",
            "total_enters": "91",
            "total_exits": "72"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 17",
            "period_hour": "17",
            "person_type": "UNKNOWN",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 17",
            "period_hour": "17",
            "person_type": "VISITOR",
            "total_enters": "15",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 18",
            "period_hour": "18",
            "person_type": "PEOPLE",
            "total_enters": "106",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 18",
            "period_hour": "18",
            "person_type": "STAFF",
            "total_enters": "89",
            "total_exits": "128"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 18",
            "period_hour": "18",
            "person_type": "VISITOR",
            "total_enters": "6",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 19",
            "period_hour": "19",
            "person_type": "PEOPLE",
            "total_enters": "101",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 19",
            "period_hour": "19",
            "person_type": "STAFF",
            "total_enters": "69",
            "total_exits": "27"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 19",
            "period_hour": "19",
            "person_type": "VISITOR",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 20",
            "period_hour": "20",
            "person_type": "PEOPLE",
            "total_enters": "32",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 20",
            "period_hour": "20",
            "person_type": "STAFF",
            "total_enters": "62",
            "total_exits": "21"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 20",
            "period_hour": "20",
            "person_type": "VISITOR",
            "total_enters": "2",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 21",
            "period_hour": "21",
            "person_type": "PEOPLE",
            "total_enters": "39",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 21",
            "period_hour": "21",
            "person_type": "STAFF",
            "total_enters": "39",
            "total_exits": "13"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 21",
            "period_hour": "21",
            "person_type": "UNKNOWN",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 21",
            "period_hour": "21",
            "person_type": "VISITOR",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 22",
            "period_hour": "22",
            "person_type": "PEOPLE",
            "total_enters": "68",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 22",
            "period_hour": "22",
            "person_type": "STAFF",
            "total_enters": "62",
            "total_exits": "7"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 22",
            "period_hour": "22",
            "person_type": "VISITOR",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 23",
            "period_hour": "23",
            "person_type": "PEOPLE",
            "total_enters": "136",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 23",
            "period_hour": "23",
            "person_type": "STAFF",
            "total_enters": "77",
            "total_exits": "10"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-15 23",
            "period_hour": "23",
            "person_type": "VISITOR",
            "total_enters": "6",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 00",
            "period_hour": "00",
            "person_type": "PEOPLE",
            "total_enters": "16",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 00",
            "period_hour": "00",
            "person_type": "STAFF",
            "total_enters": "62",
            "total_exits": "26"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 01",
            "period_hour": "01",
            "person_type": "PEOPLE",
            "total_enters": "10",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 01",
            "period_hour": "01",
            "person_type": "STAFF",
            "total_enters": "33",
            "total_exits": "6"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 02",
            "period_hour": "02",
            "person_type": "PEOPLE",
            "total_enters": "6",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 02",
            "period_hour": "02",
            "person_type": "STAFF",
            "total_enters": "6",
            "total_exits": "1"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 03",
            "period_hour": "03",
            "person_type": "STAFF",
            "total_enters": "13",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 04",
            "period_hour": "04",
            "person_type": "PEOPLE",
            "total_enters": "7",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 04",
            "period_hour": "04",
            "person_type": "STAFF",
            "total_enters": "4",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 04",
            "period_hour": "04",
            "person_type": "VISITOR",
            "total_enters": "2",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 05",
            "period_hour": "05",
            "person_type": "PEOPLE",
            "total_enters": "6",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 05",
            "period_hour": "05",
            "person_type": "STAFF",
            "total_enters": "1",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 05",
            "period_hour": "05",
            "person_type": "VISITOR",
            "total_enters": "14",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 06",
            "period_hour": "06",
            "person_type": "PEOPLE",
            "total_enters": "328",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 06",
            "period_hour": "06",
            "person_type": "STAFF",
            "total_enters": "4",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 06",
            "period_hour": "06",
            "person_type": "VISITOR",
            "total_enters": "62",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 07",
            "period_hour": "07",
            "person_type": "PEOPLE",
            "total_enters": "1631",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 07",
            "period_hour": "07",
            "person_type": "STAFF",
            "total_enters": "111",
            "total_exits": "10"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 07",
            "period_hour": "07",
            "person_type": "VISITOR",
            "total_enters": "167",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 08",
            "period_hour": "08",
            "person_type": "PEOPLE",
            "total_enters": "224",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 08",
            "period_hour": "08",
            "person_type": "STAFF",
            "total_enters": "54",
            "total_exits": "7"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 08",
            "period_hour": "08",
            "person_type": "VISITOR",
            "total_enters": "82",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 09",
            "period_hour": "09",
            "person_type": "PEOPLE",
            "total_enters": "48",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 09",
            "period_hour": "09",
            "person_type": "STAFF",
            "total_enters": "17",
            "total_exits": "19"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 09",
            "period_hour": "09",
            "person_type": "VISITOR",
            "total_enters": "44",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 10",
            "period_hour": "10",
            "person_type": "PEOPLE",
            "total_enters": "43",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 10",
            "period_hour": "10",
            "person_type": "STAFF",
            "total_enters": "28",
            "total_exits": "20"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 10",
            "period_hour": "10",
            "person_type": "VISITOR",
            "total_enters": "20",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 11",
            "period_hour": "11",
            "person_type": "PEOPLE",
            "total_enters": "69",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 11",
            "period_hour": "11",
            "person_type": "STAFF",
            "total_enters": "40",
            "total_exits": "42"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 11",
            "period_hour": "11",
            "person_type": "VISITOR",
            "total_enters": "23",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 12",
            "period_hour": "12",
            "person_type": "PEOPLE",
            "total_enters": "172",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 12",
            "period_hour": "12",
            "person_type": "STAFF",
            "total_enters": "47",
            "total_exits": "33"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 12",
            "period_hour": "12",
            "person_type": "VISITOR",
            "total_enters": "15",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 13",
            "period_hour": "13",
            "person_type": "PEOPLE",
            "total_enters": "383",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 13",
            "period_hour": "13",
            "person_type": "STAFF",
            "total_enters": "54",
            "total_exits": "24"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 13",
            "period_hour": "13",
            "person_type": "VISITOR",
            "total_enters": "67",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 14",
            "period_hour": "14",
            "person_type": "PEOPLE",
            "total_enters": "199",
            "total_exits": "0"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 14",
            "period_hour": "14",
            "person_type": "STAFF",
            "total_enters": "56",
            "total_exits": "20"
          },
          {
            "park_code": "44030701",
            "date_time": "2023-02-16 14",
            "period_hour": "14",
            "person_type": "VISITOR",
            "total_enters": "69",
            "total_exits": "0"
          }
        ]

// var guradMap = new Map()
// for (let i of data) {
//   let guradId = i['GUARD_ID']
//   if (guradMap.has(guradId)) {
//     let b = guradMap.get(guradId);
//     b.push(i)
//   } else {
//     let a = [];
//     a.push(i);
//     guradMap.set(guradId, a)
//   }
// }

var dayMap = new Map();

for(let i of data){
  let key = i['date_time'];
  if (dayMap.has(key)) {
    // dayMap.set(key, dayMap[key].push(i))
  } else {
    let a = [];
    a.push(i)
    dayMap.set(key, a);
  }
}



