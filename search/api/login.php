<?php




define('INCLUDE_PATH', '../myClass');
require_once INCLUDE_PATH."/config.inc.php";

$my_db = new Db_model($db);

$res["code"] = 0;
$res["msg"]   = "";
$type = strtolower(($_REQUEST["type"]));

switch ($type) {
	case 'checklogin':
		$res["code"] = 1;
		$user = array('name'=> 'wangzhi', 'age'=> 23, 'login'=>1, 'avatar'=>"assets/imgs/avatar.jpg");
		$res['data']['user'] = $user;
		break;
	case 'teachers':
		$res["code"] = 1;
		$word = 'a';
		if (isset($_GET["q"]) && $_GET["q"] != "") {
			$word = $_GET['q'];
		}

			$param["word"] = $word;
			$param['ex']   = isset($_GET['ex'])? $_GET['ex']:3;
			$param['db']   = isset($_GET['db'])? $_GET['db']:null;
			$word = $my_db->searchListAPI($param);



			if(isset($word[0])) {
					$res['error'] = 1;
				
					$res['sql']   = $word['sql'];
					unset($word['sql']);
					$res["data"]  = $word;
			}
				
		 
	
		break;
	default:
		# code...
		break;
}



echo json_encode($res);
?>

