<html>
<head>
<link   type="text/css" href="./src/base.css" rel="stylesheet" />
<script src="./src/jquery-2.1.0.min.js"></script>
<script src="./src/base2.js"></script>
<link rel="icon" href="http://i1.haidii.com/favicon.ico" type="/image/x-icon">
<title>汉语初学者构式词典</title>
</head>
<body>
<style>

 
</style>
<audio  id="dictVoice" autoplay="autoplay" ></audio>

<div class="out_input">
    <div><img width="400px" src="logo.jpg"></div>
    <div class="my_title">汉语初学者构式词典</div>
    <div class="in_input">
    <div style="width:400px;float:left;">
        <input type="text" id="my_search_bar" value="" class="ui-autocomplete-input" />
    </div>

    <div id="btn_search" style="float:left;padding-left:10px;">
        <a class="button" onclick="" href="#">
        <i class="search_icon_symbol">
            <img src="./src/search-white.png" style="height:20px;width:20px;">
        </i>
        </a>
       
    </div>
    </div>
</div>
<div style="clear:both;"></div>
    <div ><h2 class="tword"></h2></div>
<div class="kubox" style="display:none;">

</div>
<div id="list_div"><ul id="word_list"></ul></div>
<div id="res_div">
</div>
    <div style="text-align: center;margin:20px 50px 20px 0">
        <span>出品：豆蔻词工</span>
    </div>

</body>
</html>