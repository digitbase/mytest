<?php
header('content-type:application/json');
if($_REQUEST['good'] == 'abf2f08cba584737a7d9b412508eca7f'){
$s = <<<s
{
    "code": "0",
    "message": "success",
    "data": {
        "goodInfo": {
            "image5": "",
            "amount": 1,
            "image3": "",
            "image4": "",
            "goodsId": "ed675dda49e0445fa769f3d8020ab5e9",
            "isOnline": "yes",
            "image1": "https://images.baixingliangfan.cn/shopGoodsImg/20190116/20190116162618_2924.jpg",
            "image2": "",
            "goodsSerialNumber": "6928804011173",
            "oriPrice": 1.11,
            "presentPrice": 1.11,
            "comPic": "https://images.baixingliangfan.cn/compressedPic/20190116162618_2924.jpg",
            "state": 1,
            "shopId": "402880e860166f3c0160167897d60002",
            "goodsName": "11111500ml/瓶",
            "goodsDetail": "<img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081109_5060.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081109_1063.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_8029.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_1074.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_8439.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_6800.jpg\" width=\"100%\" height=\"auto\" alt=\"\" />"
        },
        "goodComments": [
            {
                "SCORE": 5,
                "comments": "果断卸载，2.5个小时才送到",
                "userName": "157******27",
                "discussTime": 1539491266336
            }
        ],
        "advertesPicture": {
            "PICTURE_ADDRESS": "https://images.baixingliangfan.cn/advertesPicture/20190113/20190113134955_5825.jpg",
            "TO_PLACE": "1"
        }
    }
}
s;
} else {
$s = <<<s
{
    "code": "0",
    "message": "success",
    "data": {
        "goodInfo": {
            "image5": "",
            "amount": 2,
            "image3": "",
            "image4": "",
            "goodsId": "ed675dda49e0445fa769f3d8020ab5e9",
            "isOnline": "yes",
            "image1": "https://img2018.cnblogs.com/blog/1071013/201811/1071013-20181128163306484-132911894.png",
            "image2": "",
            "goodsSerialNumber": "6928804011173",
            "oriPrice": 1.11,
            "presentPrice": 1.11,
            "comPic": "https://images.baixingliangfan.cn/compressedPic/20190116162618_2924.jpg",
            "state": 1,
            "shopId": "402880e860166f3c0160167897d60002",
            "goodsName": "2222500ml/瓶",
            "goodsDetail": "<img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081109_5060.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081109_1063.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_8029.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_1074.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_8439.jpg\" width=\"100%\" height=\"auto\" alt=\"\" /><img src=\"https://images.baixingliangfan.cn/shopGoodsDetailImg/20171224/20171224081110_6800.jpg\" width=\"100%\" height=\"auto\" alt=\"\" />"
        },
        "goodComments": [
            {
                "SCORE": 5,
                "comments": "果断卸载，2.5个小时才送到",
                "userName": "157******27",
                "discussTime": 1539491266336
            }
        ],
        "advertesPicture": {
            "PICTURE_ADDRESS": "https://images.baixingliangfan.cn/advertesPicture/20190113/20190113134955_5825.jpg",
            "TO_PLACE": "1"
        }
    }
}
s;
}
echo json_encode($s); 
?>
