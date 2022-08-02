<?php
define('INCLUDE_PATH', 'myClass');
require_once INCLUDE_PATH."/config.inc.php";

$my_db = new Db_model($db);

$res["error"] = 0;
$res["msg"]   = "";
$res["data"]  = array();

if (isset($_GET["word"]) && $_GET["word"] != "") {
	$param["word"] = $_GET["word"];
	$word = $my_db->searchWord($param);
	if (isset($word[0]) && isset($word[0]["word_info"])) {
		$res['error'] = 1;
		$res["data"]['info'] = htmlspecialchars($word[0]["word_info"]);
		//$res["data"]['info'] = htmlspecialchars("【】");
	} else {
		$res["msg"] = "no word in DB";
	}
} else {
	$res["msg"] = "not get a word";
}

echo json_encode($res);
?>
