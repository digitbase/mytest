<?php
define('INCLUDE_PATH', 'myClass');
require_once INCLUDE_PATH."/config.inc.php";

$my_db = new Db_model($db);

$res["error"] = 0;
$res["msg"]   = "";
$res["data"]  = array();

if (isset($_GET["word"]) && $_GET["word"] != "") {
	$param["word"] = $_GET["word"];
	$word = $my_db->autoSearch2($param);

	if (count($word) > 0) {

			$res['error'] = 1;
			$data = array();
			$str = $word[0]['cn'];
			$res["data"] = $str;
		
	} else {
		$res["msg"] = "no word in DB";
	}
} else {
	$res["msg"] = "not get a word";
}

echo json_encode($res);
?>

