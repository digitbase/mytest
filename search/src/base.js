var w_i = 0;
var test= null;
$(function (){

var newsearch = function(){
	var keyWord = $("#my_search_bar2").val();
	console.log(keyWord);

	var url = "./autoSearch3.php";


	$.get(url, { word: keyWord},
	function(data){
		console.log(data);
		test = data;
		if (data.error == 1) {
			
		} else {
			var res_chi =	$("#res_chi");
			var res_gou =	$("#res_gou");
			var res_jie = 	$("#res_jie");

			res_chi.html("");
			res_gou.html("");
			res_jie.html("");

			$("#res_word").html(keyWord);
			res_gou.html(data.data.jieshi);
			res_chi.html(data.data.jiegou);
			res_jie.html(data.data.word_info);

		}
	}, 'json');
}


var isearch = function(){
	var keyWord = $("#my_search_bar").val();
	console.log(keyWord);

	var url = "./autoSearch2.php";


	$.get(url, { word: keyWord},
	function(data){
		
		if (data.error == 1) {
			var res_div = $("#res_div");
			res_div.html("");
			res_div.append('<h2 class="s_word" data-rel="'+keyWord+'" id="imp">'+keyWord+'</h2><h2 class="tra_span" style="color:blue">'+data.data+'</h2>');
			res_div.append("<hr/>");

		}
	}, 'json');
}

var search2 = function(index){
	var url = "./autoSearch2.php";
	var keyWord = $('.s_word').eq(index).html();
	console.log(keyWord);

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

	console.log(event.keyCode);



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
	//$("#my_search_bar").select();
});

$("#my_search_bar").keyup(function (e){
	if (e.keyCode > 64 || e.keyCode < 91) {
		$("#res_div").html("");
		if (oldkey != $("#my_search_bar").val().trim()) {
			var url = "./autoSearch.php";
			if ($("#my_search_bar").val().length > 0) {
				keyWord = $("#my_search_bar").val();
				$.get(url, { word: keyWord},
				function(data){
					if (data.error == 1) {
						$(".kubox").html(data.data);
						$(".kubox").show();
						Qsearch.init();

					} else {
						$(".kubox").hide();
					}
					
				}, 'json');
			}
			oldkey = $("#my_search_bar").val();
		}
	}
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
		isearch();
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


$('body').on('click', "#imp", function(){

	$(this).animate({'font-size':'1.7em'},'fast');
    let key = $(this).attr('data-rel');
	$('#c_txt').attr('value',key).select();
	document.execCommand("copy");
	$(this).animate({'font-size':'1.5em'},'fast');
	//$(this).css('font-size','1.5em');
	console.log(key);

})


$('body').on('click', "#my_search_bar", function(){
	$(this).select();
})


$('body').on('click','#my_search_btn', function(){
	var key = $('#my_search_bar2').val();
	
	if (key.length < 1){
		alert('没有输入');
	} else{
		newsearch();
	}
});

$('body').on('click','.c_btn', function(){
	
	$('#c_txt').attr('value',).select();

	var key = $(this).html();
	var url = 'https://www.baidu.com/s?ie=UTF-8&wd='+key;


	var tempwindow=window.open('_blank');
	tempwindow.location=url ;
   
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
    var url = "./search.php";
    if (keyWord.length > 0) {
        
		$.get(url, { word: keyWord},
		function(data){
			if (data.error ==1) {
				re = new RegExp("\u3010", "g");
				str  = data.data.info.replace(re, "<br/>\u3010");
				re = new RegExp("&quot;", "g");
				str  = str.replace(re, "");


				
				res_div.append('<h2 style="cursor: pointer;" data-rel="'+keyWord+'" id="imp">'+keyWord+'</h2>');
				//res_div.append('<div style="cursor: pointer;" class="c_btn" >'+keyWord+'</div>');
				res_div.append("<a target='_blank' href=https://www.youdict.com/ciyuan/s/"+keyWord+">root</a>");

				res_div.append(str);
				res_div.append("<hr/>");
				
				$("#word_list").insertBefore("<li>"+keyWord+"</li>");
			} else {
				res_div.html(data.msg);
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

var copy_word = function (obj){
	var key = ($(obj).attr('word'));
	$(obj).css({'color':'red'});
	copy_clip(key);
}

var s1 = ['brand','firebrand','band','disband','abandon','aboundant','abound','squander','conserve','hundred','thousand','hour','four','sour','tour','minute','average','coverage','storage','rage','beverage','averse','verity','veracious','voracious','mendacious','vivacious','deny','belie','avert','divert','advert','advertisement','introvert','oppose','controversy','avenge','revenge','revenue','avenue','honour','humour','rumour','colour','odour','village','pillage','colleage','collage','collect','villa','villain','bounce','rebounce','bound','aboundant','rebound','announce','pronounce','renounce','denouce','enounce','claim','aim','race','brace','embrace','renounce','author','authority','authorize','athlete','appendage','appendix','auxiliary','pendulum','curriculum','schedule','scheme','independence','pendent','suspension','chassis','compendium','dependable','expend','spend','expensive','impending','expension','ear','hear','fear','pear','gear','sear','shear','scissors','assistant','chassis','sister','garden','guard','garage','severe','several','general','sever','serious','federal','funeral','tourism','entourage','enter','tournament','wrong','strong','prong','throng','die','diy','oxygen','dioxide','watermelon','lemon','melody','pocket','rock','rocket','socket','picket','jacket','picker','ticket'];
var s2 = ['stadium','reply','imply','multiply','plus','minus','divide','divorce','comply','straw','beg','marry','carry','beyond','gesture','digest','digestion','congestion','ingest','pregnant','stagnant','indignant','dignity','pressure','compression','depresse','detractor','impress','oppress','together','altogether','road','street','avenue','salt','farm','arm','harm','warm','heat ','hot','component','exponent','opponent','proponent','detractor','successful','access','cessation','excess ','incessant','intercessor','predecessor','recess','recessive','permanent','permanence','pertinent','immanent','germane','prominent','deep','dip','dig','deeg','it','eat'];
var s3 = ['similar', 'assimilate', 'simulate', 'facsimile', 'similarity', 'verisimilar', 'monger', 'mongrel', 'warmonger', 'among', 'quest', 'bequest', 'conquest', 'question', 'request', 'sequester', 'sequestrate', 'conserve', 'deserve', 'situation', 'lassitude', 'sentence', 'dissent', 'sentiment', 'dissenter', 'essential', 'essence', 'insentient', 'persentation', 'presentiment', 'premonition', 'resent', 'resentful', 'resentment', 'assent', 'sentient', 'deform', 'conformism', 'dissent', 'deform', 'formation', 'formula', 'inform', 'informal', 'information', 'uniform', 'formula', 'contrast', 'contract', 'detract', 'abstract', 'attract', 'extract', 'intract', 'protract', 'retract', 'subtraction', 'tractable'];

