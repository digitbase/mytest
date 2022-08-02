
<?php
define('INCLUDE_PATH', 'myClass');
require_once INCLUDE_PATH."/config.inc.php";



$my_db = new Db_model($db);

$data['word'] = 'abacus';
$res = $my_db->searchWord($data);
var_dump($res);

return ;

if (($handle = fopen("350.csv", "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {


    	if (count($data) >= 5) {
    		$res = $my_db->insert_yp($data);
    	} else {
    		var_dump($data);
    		print('not count 5 field </br>');
    	}
  
    }
    fclose($handle);
}
echo "insert complete!";
?>

