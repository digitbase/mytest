
<?php
define('INCLUDE_PATH', 'myClass');
require_once INCLUDE_PATH."/common.functions.php";
require_once INCLUDE_PATH."/config.inc.php";

$my_db = new Db_model($db);
 

 
 

if (isset($_POST['myword'])) :


	$patt = '/\b[a-zA-Z]+\b/';
	preg_match_all($patt,$_POST["myword"],$res);

 

 
	$w_array = array();
	foreach ($res[0] as $key => $value) {

		$res = $my_db->isword($value);
		if(isset($res[0]['y']) && $res[0]['y'] == 1)
		$w_array[] = $value;

	}

	$s = join($w_array,',');
	

endif;
?>

<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body>
<form name="my" method="post">
	
	<textarea name='myword' cols="80" rows="20"><?php if (isset($_POST['myword'])) echo $_POST['myword'];?>
	</textarea>
	<input type="submit" value="提交"/>
</form>
<textarea   cols="80" rows="20">
	<?php if (isset($s)) echo $s;?>
</textarea>
</body>
</html>