<?php
error_reporting( E_ALL );

require_once "db_config.php";
require_once "db_class.php";
require_once "db_model.php";


function prs($s){
	echo "<pre>";
	var_dump($s);
	echo "</pre>";
}

$db_config = new DATABASE_CONFIG();

$db = new Db($db_config);

?>