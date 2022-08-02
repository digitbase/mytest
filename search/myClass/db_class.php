<?php
error_reporting(E_ALL ^ E_DEPRECATED);

class Db {

    var $config;
    var $con = null;

    function Db ($config) {
        $this->config = $config->default;
        $this->init();
    }

    function init () {
        $this->con = $this->dbConnection();
    }

    function dbConnection(){

        $con = mysql_connect($this->config['host'],$this->config['login'],$this->config['password']);
        if (isset($this->config['encoding']))
        mysql_query("set names '".$this->config['encoding']."'");
        else 
        mysql_query("set names 'utf8'");
       

        mysql_select_db($this->config["database"], $con);
        if( !$con ){
            print "connection error";
        }
        return $con;
    }


    function querym($string){
       return  mysql_query($string);
    }   

    function sqlError(){
        return mysql_error();
    }


    function getAll($sql){
        $result = mysql_query($sql, $this->con);
        if (!$result) {
            return null;
        }
        $results = array();
        while($row = mysql_fetch_assoc( $result)) {
            $results[] = $row;
        }
        return $results;
    }

    function query($sql){
        $select_result = mysql_query($sql, $this->con);
        if (!$select_result) {
            return null;
        } else {
            return  $select_result;
        }
    }

    function esc_str( $str ) {
        return mysql_escape_string($str);
    }

    function close () {
        mysql_close($this->con);
    }
    function lastInsertId(){
        return mysql_insert_id($this->con);
    }
    function affectedRows(){
        return mysql_affected_rows($this->con);
    }
}
?>