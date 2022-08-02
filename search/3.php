
<?php
define('INCLUDE_PATH', 'myClass');
require_once INCLUDE_PATH."/config.inc.php";
$my_db = new Db_model($db);


$path='you-apple.xml';
$books=new DOMDocument();
$books->load($path);

$bookElements=$books->getElementsByTagName('entry');
$a = 0;
foreach($bookElements as $book){
    foreach ($book->attributes as $attr) {
    	if ('d:title' == $attr->nodeName) {
            $a ++;
    		

    		//echo(htmlspecialchars($book->nodeValue));

 
            $count = $my_db->searchWordin($attr->nodeValue);
     
            if (isset($count[0])){
                echo "[ ".$a." ] " . $attr->nodeValue;

                $ssa = split($attr->nodeValue."\n", $book->nodeValue);

                $res = $my_db->updateroot($count[0]['id'], $ssa[1]);
                echo "    ";
                ob_flush();
            }
            break;
    	}
        
    }
    // if ($a >10) {
    //     break;
    // }

}


return 0;

?>

