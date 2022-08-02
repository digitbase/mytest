<?php
function createSql($sql, $data) {
    foreach( $data AS $name => $value) {
        if(is_array($value)) {
            continue;
        }
        $value = mysql_real_escape_string($value);
        $sql = str_replace(":" . $name . ":", $value, $sql);
    }
    return $sql;
}

class Db_model {

    var $db = null;

    function Db_model ($db) {
        $this->db = $db;
    }

    function selectAll() {

            $sql = "select * from word_tbl";
            return $this->db->getAll($sql);
    }

    function selectOldFile($data) {
        $sql  = "";
        $sql .= " select * from temp_file_tbl ";
        $sql .= " where ";
        $sql .= " user_id = :user_id:";
        $sql .= " and token <> ':token:' ";

        $sql = createSql($sql, $data);

        return $this->db->getAll($sql);
    }

    function deleteTFbyID($data) {
        $sql = " delete from temp_file_tbl where fid = :fid: ";
        $sql = createSql($sql, $data);
        return $this->db->query($sql);
    }
	
	function searchWord($data) {
		$sql = "";
		
		$sql .= " select * from word_tbl ";
		$sql .= " where word = ':word:' ";
		
        $sql = createSql($sql, $data);
		//pr($sql);
        return $this->db->getAll($sql);
	}
	function autoSearch($data) {
		$sql = "";
		
		$sql .= " select * from word_tbl ";
		$sql .= " where word like '%:word:%' ";
		$sql .= " limit 0,30 ";
		
        $sql = createSql($sql, $data);
		//pr($sql);
        return $this->db->getAll($sql);
	}

    function searchWordin($data){
        $sql = " select id from mydict where word = '{$data}' ";
        $res = $this->db->getAll($sql);
        return $res;
    }
    function updateroot($id, $txt){
        $sql = "UPDATE mydict SET root = '{$txt}' WHERE id ={$id}; ";
        $res = $this->db->query($sql);
        return $res;
    }

    function searchAPI($data) {
        $sql = "";
        
        $sql .= " select * from mydict ";

        if ($data['ex'] == 2) {
            $sql .= " where word like '%:word:' ";
            $sql .= " and root is not null limit 0,30 ";
        } elseif($data['ex'] == 1) {
            $sql .= " where word like ':word:%' ";
            $sql .= " and root is not null limit 0,30 ";
        } elseif($data['ex'] == 3){
            $sql .= " where word like '%:word:%' ";
            $sql .= " and root is not null limit 0,30 ";
        } elseif($data['ex'] == 4){
            $sql .= " where root like '%:word:%' ";
            $sql .= " and root is not null limit 0,50 ";
        } else{
            $sql .= " where word = ':word:' ";
            $sql .= " and root is not null limit 0,1 ";
        }


        
        $sql = createSql($sql, $data);
        
        $res = $this->db->getAll($sql);
        $res['sql'] = $sql;
        //prs($sql);
        return $res;
    }

    function addSubWord($data) {
        $sql  = "";
        $sql .= " INSERT INTO  `userword_tbl` ( `user_id` ,`word` ,`up_word` ,`up_time`) ";
        $sql .= " VALUES ( ";
        $sql .=  $data['userid'] . " , '".$data['pword']."', '".$data['sword']."', now() )";
 

        $res = $this->db->query($sql);
        return $res; 

    }



    function searchListAPI($data) {
        $sql = "";
        
        $sql .= " select * from mydict ";

        if ($data['ex'] == 2) {
            $sql .= " where word like '%:word:' ";
            $sql .= " and root is not null limit 0,30 ";
        } elseif($data['ex'] == 1) {
            $sql .= " where word like ':word:%' ";
            $sql .= " and root is not null order by word_long limit 0,10 ";
        } elseif($data['ex'] == 3){
            $sql .= " where word like '%:word:%' ";
            $sql .= " and root is not null order by word_long limit 0,30 ";
        } elseif($data['ex'] == 4){
            $sql .= " where root like '%:word:%' ";
            $sql .= " and root is not null limit 0,50 ";
        } else{
            $sql .= " where word = ':word:' ";
            $sql .= " and root is not null limit 0,1 ";
        }


        
        $sql = createSql($sql, $data);
        
        $res = $this->db->getAll($sql);
        //prs($res);
        $res['sql'] = $sql;
        //prs($res);
        return $res;
    }

    function searchUserSubWord($data) {
        $sql = "";
        
        $sql .= " select * from userword_tbl ";
        $sql .= " where user_id = :userid: and word = ':word:' ";
        $sql .= " limit 0,30 ";
        
        $sql = createSql($sql, $data);

        $res = $this->db->getAll($sql);
        $res['sql'] = $sql;
        //prs($sql);
        return $res;
    }

        
    function delSubWordById($data) {
        $sql = "";
        
        $sql .= " delete  from userword_tbl ";
        $sql .= " where user_id = :userid: and id = ':id:' ";
        
        $sql = createSql($sql, $data);
        $res = $this->db->getAll($sql);
        $res['sql'] = $sql;
        //prs($sql);
        return $res;
    }

	function autoSearch3($data) {
        $sql = "";
        
        $sql .= " select * from word_tbl ";
        $sql .= " where word like '%:word:%' ";
        $sql .= " limit 0,30 ";
        
        $sql = createSql($sql, $data);
        //pr($sql);
        return $this->db->getAll($sql);
    }


    function autoSearch2($data) {
        $sql = "";
        
        $sql .= " select * from words ";
        $sql .= " where en = ':word:' ";
        $sql .= " limit 0,1 ";
        
        $sql = createSql($sql, $data);
        //pr($sql);
        return $this->db->getAll($sql);
    }
	
	function saveWord($data) {
        $sql = "";

        $sql .= " insert into word_tbl ";
        $sql .= " (";
        $sql .= " word, ";
        $sql .= " word_info) ";
        $sql .= " VALUES ( ";
        $sql .= " ':word:', ";
        $sql .= " ':info:'); ";

        $sql = createSql($sql, $data);
        return $this->db->query($sql);
	}





    function isword($s) {
 
        $sql    = " select count(*) as y from mydict ";
        $sql .= " where word = '{$s}' ";
        return $this->db->getAll($sql);  
    }

    function Searchallyq(){
      $sql = " select * from yq_tbl";
      return $this->db->getAll($sql);  
    }

    function insert_yp($data){
        $id = trim($data[0]);
        $sql  = " select count(id) as icount from yq_tbl where f1 ={$id} ";
 
        $c = $this->db->getAll($sql);
 
        $data[0] = trim($data[0]);
        $data[1] = mysql_escape_string($data[1]);
        $data[2] = mysql_escape_string($data[2]);
        $data[3] = mysql_escape_string($data[3]);
        $data[4] = mysql_escape_string($data[4]);
  
        

        if($c[0]['icount'] != 0){
            $sql = "UPDATE `yq_tbl` SET `f2` = '{$data[1]}',`f3` = '{$data[2]}',`f4` = '{$data[3]}',`f5` = '{$data[4]}'  WHERE `f1` ={$id}; ";
        } else {
            $sql = "INSERT INTO `yq_tbl` ( `f1`, `f2`, `f3`, `f4`, `f5`) VALUES ( '{$data[0]}', '{$data[1]}', '{$data[2]}', '{$data[3]}', '{$data[4]}');";
        }

        prs($sql);
        $r = $this->db->query($sql);

    }



            function searchWordyq($data) {
                $sql = "";
                
                $sql .= " select * from yq_tbl ";
                $sql .= " where f2 like '%:word:%' ";
                $sql .= " limit 0,30 ";
                
                $sql = createSql($sql, $data);
                //pr($sql);
                return $this->db->getAll($sql);
            }

}
?>