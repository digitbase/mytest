var w_i = 0;
var test = 0;
$(function (){

	var _test = test
	$('.out_radio').click(function(){
		console.log($(this));
		test = $(this);
		$("input[name='ex']").attr('checked',false);
		$(this).find('input').prop('checked','checked');
	})



var search2 = function(index){
	var url = "./autoSearch2.php";
	var keyWord = $('.s_word').eq(index).html();
	console.log('search2'+keyWord);

	$.get(url, { word: keyWord},
	function(data){
		console.log(data);
		if (data.error == 1) {
			$('.s_word').eq(index).next().html(data.data);
		}
	}, 'json');
}


$('.ls_div').click(function(obj){
	
	var name = ($(this).attr('id'));
	var o = eval(name);
	
	var res_div = $("#res_div");
	res_div.html("");
	for (var i=0; i <= o.length - 1; i++) {

		res_div.append('<h2 class="addone">'+i+'</h2><h2 class="s_word" data-rel="'+o[i]+'" id="imp">'+o[i]+'</h2><h2 class="tra_span" style="color:blue"></h2>');
		res_div.append("<hr/>");
	}
});


$(document).keyup(function(event){

	if(event.keyCode == 70){
		search2(w_i);
	}


	if(event.keyCode == 186){
		var url = "https://www.baidu.com/s?wd=";
		var keyWord = $('.s_word').eq(w_i).html();
		console.log(w_i);console.log(keyWord);
		window.open(url+keyWord);
	}

	if(event.keyCode == 38){
		w_i--;
		$('.s_word').eq(w_i).show().trigger('mouseover');
		var ii  = $('.s_word').eq(w_i).offset().top-60;
		$(document).scrollTop(ii);
		
	}


  if(event.keyCode == 32 || event.keyCode == 40){
  	w_i++;
  	$('.s_word').hide();
  	$('.s_word').eq(w_i).show().trigger('mouseover');
  	search2(w_i-1);
  	var ii  = $('.s_word').eq(w_i).offset().top-60;
  	$(document).scrollTop(ii);
  	console.log(ii);
  }
  if(event.keyCode == 67){
  	$('.s_word').eq(w_i).trigger('mouseover');
  }

});

var oldkey = "";

$("#my_search_bar").focus();
$("#my_search_bar").mouseover(function (){
$("#my_search_bar").select();
});

$("#my_search_bar").keyup(function (e){


});

var keyWord = "";

var Qsearch = {
	ul:null,
	init : function (){
		$('.li_word').mouseover(function (){
			$('.kubox .current').removeClass('current');
			$(this).addClass('current');
		});
	
		$('.li_word').click(function(){
			$("#my_search_bar").val($(this).attr('word'));
			search();
			selecli('down');
			$(this).hide();
		});
	}
};
$('html,body').click(function(e){
	var a= (e.target);

	if (a.className != 'li_word') {
		$(".kubox").hide();
	}
});

document.onkeyup = function(e){

	if (e.keyCode == 13){
		$("#res_div").html("");
	
		search();
	} else if (e.keyCode == 38){
		selecli('up');
	} else if (e.keyCode == 40){
		selecli('down');
	}
};

$("#btn_search").click(function (){
	$("#res_div").html("");
	search();
});


$('body').on('mouseover', "#imp", function(){
	//var key = $(this).attr('data-rel');
	//var url = 'http://dict.youdao.com/dictvoice?audio='+key+'&type=2'
	//$("#dictVoice").attr('src', url);
})

$('body').on('click', "#my_search_bar", function(){
	$(this).select();
})



$('body').on('click', "#imp", function(){
	var key = $(this).attr('data-rel');
	var url = 'http://dict.youdao.com/dictvoice?audio='+key+'&type=2'
	$("#dictVoice").attr('src', url);
})

var search = function (){
	keyWord = $("#my_search_bar").val();
	if ($('.kubox').css('display') == 'block') {
		keyWord = $('.kubox .current').html();
		$("#my_search_bar").val($('.kubox .current').html());
	}
	var res_div = $("#res_div");
    var url = "./searchapi.php";
    var ex = $("input[name='ex']:checked").val();

    var db = $('.db_select').val()


    if (keyWord.length > 0) {
        
		$.get(url, { word: keyWord, ex: ex, db:db},
		function(data){
			console.log(data.data);
		 	_test = data;
			if (data.error ==1) {
				let ar = (data.data);

				let tb = $("<table class='table dataTable table-striped table-bordered table-hover'>");
				let tr = $('<tr class="t_tr"><td width="180px">字</td><td>词义</td></tr>');

				tb.append(tr);

                for (let i=0; i <ar.length; i++) {
                	
                	
                	let th = $('<tr>');
                	let td1= $('<td  class="myowrdlist">').html(ar[i]['word']);
                	let td2= $('<td  >').html(ar[i]['root']);
 
 					console.log(ar[i]['root']);

                	th.append(td1).append(td2) 
                	tb.append(th);
                }
                $('#res_div').append(tb);
                $('.myowrdlist').on('click', function(){

                	let key = $(this).html();

                	$('#my_search_bar').val(key).select();
                	document.execCommand("copy");
                	let keyWord = key;
                	let url  = 'https://s.ohltr.com/searchapi.php?word='+keyWord;
                	var aurl = 'http://dict.youdao.com/dictvoice?audio='+keyWord+'&type=2';
                	var burl = 'https://sp0.baidu.com/-rM1hT4a2gU2pMbgoY3K/gettts?lan=en&text='+keyWord+'&spd=2&source=alading'
                	$("#dictVoice").attr('src', burl);
                	//window.location= 'dict://'+key;
                });

			} else {
				let dd = $('<div>').html('没有找到您要的数据!').css({'margin-right':'50px','margin-bottom':'50px','font-size':'18px','color':'#595959'});
				res_div.html(dd).css('text-align','center');
			}
		}, 'json');

        $("#my_search_bar").select();


    }
    
}

var selecli = function (flg) {
	$("#my_search_bar").blur();
	 var box = $('.kubox>ul>li');
	 if (box.length > 1) {
		var current = $('.kubox .current');
		if (flg == "down") {
			if ($('.kubox .current').attr("index") < box.length-1) {
				$('.kubox .current').next().addClass("current");
				current.removeClass("current");
			}
		} else {
			if ($('.kubox .current').attr("index") > 0) {
				$('.kubox .current').prev().addClass("current");
				current.removeClass("current");
			}
		}
		$("#my_search_bar").val($('.kubox .current').html());
	 }
}

});



