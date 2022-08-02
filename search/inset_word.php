<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<?php
define('INCLUDE_PATH', 'myClass');
require_once INCLUDE_PATH."/config.inc.php";


$my_db = new Db_model($db);

$crlf = "\r\n";
$str = file_get_contents('my_word.txt');
$res = explode($crlf, $str);

$i=1;
foreach($res as $row) {
	if ($row != ""){
		$list = explode(",", $row);

		$params = array();
		if (count($list) == 3) {
			$params["word"] = str_replace('"', "", $list[1]);
			$params["info"] = $list[2];
			$res = $my_db->saveWord($params);
			ob_start();
			echo $i."<br/>";
			 ob_end_flush();
			$i++;
		}
	}
}
echo "end";
?>
</html>