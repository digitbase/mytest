<?php
define('INCLUDE_PATH', '../myClass');
require_once INCLUDE_PATH."/config.inc.php";

$my_db = new Db_model($db);

$res["error"] = 0;
$res["msg"]   = "";
$res["data"]  = array();

if (isset($_GET["word"]) && $_GET["word"] != "") {

	$param["word"] = $_GET["word"];
	$param['ex']   = isset($_GET['ex'])? $_GET['ex']:3;
	$param['db']   = isset($_GET['db'])? $_GET['db']:null;
	$word = $my_db->searchListAPI($param);



	if(isset($word[0])) {
			$res['error'] = 1;
		
			$res['sql']   = $word['sql'];
			unset($word['sql']);
			$res["data"]  = $word;
	}
		
 
} else {
	$res["msg"] = "not get a word";
}

echo json_encode($res);
?>
