<?php
/* 
 * phpMyVisites : website statistics and audience measurements
 * Copyright (C) 2002 - 2006
 * http://www.phpmyvisites.net/ 
 * phpMyVisites is free software (license GNU/GPL)
 * Authors : phpMyVisites team
*/

// $Id: common.functions.php 43 2006-08-21 05:55:50Z matthieu_ $


define("PKEY", "656cd9b0af9435b0");

function getFilenameExtension( $name )
{
    $posDot = strrpos( $name, ".");
    if($posDot===false)
    {
        return $name;
    }
    
    return substr( $name, $posDot + 1);
}

function U2U($szstr)
{
    $matches = array();
    preg_match_all("/%u([0-9,A-F][0-9,A-F][0-9,A-F][0-9,A-F])/i", $szstr, $matches);

    $letters = 255;

    $found = count($matches[0]);
    
    while($found && $letters--)
    {
        $ustr = $matches[0][0];
        $ustrCode = str_replace("%u", "", $ustr);
        
        $astrCode = hexdec($ustrCode);
        $astr = sprintf("&#%d", $astrCode);
        
        $szstr = str_replace($ustr, $astr, $szstr);
        
        $matches = array();
        preg_match_all("/%u([0-9,A-F][0-9,A-F][0-9,A-F][0-9,A-F])/i", $szstr,
        $matches);
        
        $found = count($matches[0]);
    }
    
    return $szstr;
}

function databaseEscape($str)
{
    return mysql_real_escape_string($str);
}


function enCodePrize($text){

    $key = PKEY;   //key的长度必须16，32位,这里直接MD5一个长度为32位的key
    $iv='adkadf2sadaadfaa'; //加密的随机数
    $crypttext = mcrypt_encrypt(MCRYPT_RIJNDAEL_128, $key, $text, MCRYPT_MODE_CBC, $iv);
    $data = base64_encode($crypttext);
    $data = str_replace(array('+','/','='),array('-','_',''),$data);
    return $data;
}


function deCodePrize($text){
    $key = PKEY;
    $iv='adkadf2sadaadfaa';
    $data = str_replace(array('-','_'),array('+','/'),$text);
    $mod4 = strlen($data) % 4;
    if ($mod4) {
        $data .= substr('====', $mod4);
    }
    $crypttext = base64_decode($data);
    return mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $key, $crypttext, MCRYPT_MODE_CBC, $iv); 
}



function uncompress( $data, $compressed )
{
    if($compressed == 1)
    {
        //var_dump($data);
        
        // normal case
        if( $return = gzuncompress($data) )
        {
            return $return;
        }
        // case backward compatibility for cookie between 2.1 base64encode and between 2.2
        else
        {
            return base64_decode($data);
        }
    }
    return $data;
}
function compress( $data, $compressed )
{
    if($compressed == 1)
    {
        return gzcompress($data);
    }
    return $data;
}
/**
 * returns the SQL-format date of the timestamp $ts
 * 
 * @param timestamp $ts
 * 
 * @return string date
 */
function getDateFromTimestamp($ts)
{
    return date("Y-m-d", $ts);
}


/**
 * get a variable from the $_REQUEST superglobal
 * 
 * it tests the var type and exit if the variable doesn't have default value and
 * if the type doesn't match
 * 
 * @param string $varName name of the variable
 * @param string $varDefault default value. If '', and if the type doesn't match, exit() !
 * @param string $varType variable type
 */
function getRequestVar($varName, $varDefault=null, $varType="string")
{

    $varDefault = secureVar(stripslashesPmv($varDefault));
    
    if(!isset($_REQUEST[$varName]) || empty($_REQUEST[$varName]))
    {
        if($varDefault===null)
        {
            exit();
            return;
        }
        else
        {
            if($varType=="numeric")
            {
                 $varType="string";
            }
            settype($varDefault, $varType);
            return $varDefault;
        }
    }
    else
    {
        $content = secureVar(stripslashesPmv($_REQUEST[$varName]));
        
        if($varType == 'string')
        {
            if(is_string($content)) $ok = true;
        }           
        elseif($varType == 'numeric' || $varType == 'int' || $varType == 'float')
        {
                if(is_numeric($content)) $ok = true;
        }
        elseif($varType == 'array')
        {
                if(is_array($content)) $ok = true;
        }
        else
        {
            $ok=true;
        }
        
        if(!isset($ok))
        {
            if($varDefault===null) 
            {   
                trigger_error("Error : \$varName '$varName' doesn't have a correct type in \$_REQUEST and doesn't " .
                        "have a \$varDefault value", E_USER_ERROR);
                exit();
                return;
            }
            else
            {
                if($varType=="numeric")
                {
                     $varType="string";
                }
                settype($varDefault, $varType);
                return $varDefault;
            }
        }
        else
        {
            return $content;
        }
    }
}

/**
 * print message or array in debug mode
 * 
 * @param string $message
 */
function printDebug ($message) {
    if(DEBUG)
    {
        if(!is_scalar($message))
        {
            print("<pre>");
            var_dump($message);
            print("</pre>");
        }
        else
        {
            print($message);
        }
    }
}

/**
 * log page generation performances (queries number and time)
 * 
 * @param int $idSite
 * 
 * @param bool true
 */
function recordDbQueryCount($idSite)
{
    // records query count and time to compute this page
    $res = substr(getMicrotime()-$GLOBALS['time_start'], 0, 4);
    $r = query("INSERT INTO ".T_QUERY_LOG." (idsite, query, time, date, daytime)" .
        " VALUES ('$idSite', '".$GLOBALS['query_count']."', '$res', CURRENT_DATE(), CURRENT_TIME())");
        
    return true;
}



/**
 * operation called by secureVar
 * 
 * @param int|string $var
 * 
 * @return int|string
 */
function secureVarOperation($var)
{
    if(is_array( $var ))
    {
        foreach($var as $key => $value)
        {
            if(is_array($value))
            {
                $var[$key] = secureVarOperation($value);
            }
            else
            {
                $var[$key] = htmlspecialchars(trim($value));
            }
        }
    }
    else
    {
        $var = htmlspecialchars(trim($var));
    }
    
    return databaseSecure($var);
}

function databaseSecure($var)
{

    if(1)
    {
        if(is_array($var))
        {
            foreach($var as $key => $value)
            {
                if(is_array($value))
                {
                    $var[$key] = databaseSecure($value);
                }
                else
                {
                    $var[$key] = databaseEscape($value);
                }
            }
        }
        else
        {
            $var = databaseEscape($var);
        }
    }
    return $var;
}
/**
 * secures the variable from SQL injection and from cross site scripting
 * 
 * @param int|string|array $var
 * @param int|string|array var secured 
 */
function secureVar($var)
{
    if(is_scalar($var))
    {
        return secureVarOperation($var);
    }
    else if(is_array($var))
    {
        foreach($var as $key => $value)
        {
            $var[$key] = secureVarOperation($value);
        }
        return $var;
    }
    else
    {
        return $var;
    }
}

/**
 * special stripslashes managing fucking magic_quotes
 * 
 * @param string|array $str
 * 
 * @return string|array stripslashed, or not
 */
function stripslashesPmv($str)
{
    if (get_magic_quotes_gpc())
    {
        if(is_array($str))
        {
            foreach($str as $key => $value)
            {
                $str[$key] = stripslashes($value);
            }
            return $str;
        }
        else
        {
            return stripslashes($str);
        }
    }
    else
    {
        return $str;
    }
}


/**
 * set an int or string to a precise length, completing on the left with zero (O)
 * 
 * @param all $id
 * @param int $length
 * 
 * @return string string to length $length
 */
function setToLength($id, $length)
{
    settype($id, 'string');
    $l = strlen($id);
    for($i=0;$i<$length-$l;$i++)
    {
        $id='0'.$id;
    }
    return $id;
}


/**
 * returns seconds since midnight today
 * 
 * @return int seconds since midnight today
 */
function todayTime()
{
    return date("H") * 3600 + date("i") * 60 + date("s");
}

//------------------------------------------------------------------------------
    function getURLVar($varName, $varDefault="") {
        if(!isset($_REQUEST["{$varName}"]) || empty($_REQUEST["{$varName}"])) {
            return $varDefault;
        }
        else {
            return $_REQUEST["{$varName}"];
        }
    }
    function getDateTime() {
        return date("Y-m-d H:i:s");
    }


    function getDateNoTime() {
        return date("Y-m-d");
    }

    function SearchEngineDetect($referer = '')
    {
        /*
         * Search Engine detecting
         * phpMyVisites
         */
        global $db_model, $GLOBALS;

        $searchEngines = $GLOBALS['searchEngines'];
        $detection_result = array();

        if($referer) {
            $ref_cpts = parse_url($referer);
            $url_queries = array();
            $queries = array();
            $from_search = false;
            $keyword = '';
            $se_name = '';
            $keyword_p = '';
            $key_encoding = 'UTF-8';

            $sesback = array();
            $ses = array();

            // Fetch the searching engines from database
            if($GLOBALS["SESOURCE"] === 1) {
                $sesback = $db_model->getSearchEgns();

                if(is_array($sesback) && count($sesback)) {
                    foreach($sesback as $se) {
                        $domain = $se["search_domain"];
                        if(ereg("^http", $se["search_domain"])) {
                            $domains = parse_url($se["search_domain"]);
                            $domain  = $domains['host'];
                        }

                        if(isset($domain)) {
                            $ses[$domain] = array(strtolower($se["search_name"]), $se["search_query"]);
                        }
                    }
                }

                if(is_array($ses) && count($ses)) {
                    $searchEngines = $ses;
                }
            }


            if(is_array($searchEngines) && count($searchEngines)) {
                if(array_key_exists($ref_cpts['host'], $searchEngines)) {
                    $from_search = true;
                    $se_name     = strtolower($searchEngines[$ref_cpts['host']][0]);
                    // searching key url param
                    if(isset($searchEngines[$ref_cpts['host']][1]))
                        $keyword_p   = explode(",", $searchEngines[$ref_cpts['host']][1]);

                    if(isset($searchEngines[$ref_cpts['host']][2])) {
                        $key_encoding = $searchEngines[$ref_cpts['host']][2];
                    }
                }
            }

            if($from_search) {
                if(isset($ref_cpts['query']))
                    $url_queries = explode("&", $ref_cpts['query']);

                if(is_array($url_queries) && count($url_queries)) {
                    foreach($url_queries as $query) {
                         $query = explode("=", $query);
                         $queries[$query[0]] = $query[1];
                    }
                }

                if(is_array($keyword_p)) {
                    foreach($keyword_p as $url_p) {
                        if(array_key_exists($url_p, $queries)) {
                            $keyword = urldecode($queries[$url_p]);

                            break;
                        }
                    }
                }
                else if(array_key_exists($keyword_p, $queries))
                    $keyword = urldecode($queries[$keyword_p]);
            }

            $detection_result['from_search'] = $from_search;
            $detection_result['se_id']       = $se_name;
            $detection_result['keyword']     = $keyword;
            $detection_result['se_encoding'] = $key_encoding;
        }

        return $detection_result;
    }



    function get_referer($start_key, $end_key)
    {
        $referer = '';

        if(is_array($_GET) && count($_GET)) {
            $queries = $_GET;
            $start = false;

            if($start_key && $end_key) {
                foreach($queries as $key=>$value) {

                    if($key == $start_key) {
                        $start = true;
                        $referer = $value;

                        continue;
                    }

                    if($key == $end_key)
                        break;

                    if($start)
                        $referer .= "&".$key."=".$value;
                }
            }
        }

        return $referer;
    }

    /*
     * order statistics
     */
    function orderPageSave($params = array())
    {
        global $db_model;

        if(is_array($params) && count($params)) {
            if(isset($params['PAGE_TYPE']) && $params['PAGE_TYPE'] == 2) {
                $db_model->insertCV($params);

                // increment the cv num of the custom by custom_cookie
                $db_model->incrementCVNum($params);
            }
        }
    }

    function getCvParam($params = array(), $name = '', $value='')
    {
        if(isset($name) && is_array($params)) {
            if(isset($params[$name])) {
                return urldecode($params[$name]);
            }
        }
        else {
            return $value;
        }
    }

    function jumptToAdPage($data)
    {
        $ad_url = '';

        if(is_array($data) && isset($data["ad_url"])) {
            $ad_url .= $data["ad_url"];
        }

        if(is_array($data) && isset($data["ad_seq"]) && isset($data["ad_type"])) {
            if(!empty($data["ad_seq"])) {
                $ad_url .= "?adclick_advpage=1";
            }
        }

        if($ad_url) {
            echo '<script type="text/javascript">window.location.href="'.$ad_url.'";</script>';
            exit;
        }
    }

    function getUrlQuery($url='', $query_name='')
    {
        $value = '';
        $queries = array();

        if($url) {
            $queries = getUrlParts($url, "query");
        }

        if(is_array($queries) && count($queries)) {
            if($query_name) {
                if(isset($queries["{$query_name}"]))
                    $value = $queries["{$query_name}"];
            }
        }

        return $value;
    }

    function checkUrlQueryExists($url='', $query_name='')
    {
        $value = false;
        $queries = array();

        if($url) {
            $queries = getUrlParts($url, "query");
        }

        if(is_array($queries) && count($queries)) {
            if($query_name) {
                if(isset($queries["{$query_name}"]))
                    $value = true;
            }
        }

        return $value;
    }

    function getUrlParts($url, $part_name)
    {
        $cv_params = array();

        if($url) {
            $referer_parts = parse_url($url);
        }

        if(isset($referer_parts["{$part_name}"])) {
            switch($part_name) {
                case "query":
                    $query= $referer_parts["{$part_name}"];
                    $queries = explode("&", $query);

                    if(is_array($queries) && count($queries)) {
                        foreach($queries as $query) {
                            $a_query = explode("=", $query);

                            $cv_params[$a_query[0]] = $a_query[1];
                        }
                    }

                    break;

                case "host":
                    $cv_params = $referer_parts["{$part_name}"];
                    break;

                default:
                    break;
            }
        }

        return $cv_params;
    }

/**
 * SQLｶ舌・
 *
 * @param string $sql SQL
 * @param array $data f[^
 * @return string 黷ｽSQL
 * @access public
 */
// function CreateSQL($sql, $data)
// {
//     foreach( $data AS $name => $value) {
//         if(is_array($value)) {
//             continue;
//         }

//         $value = mysql_escape_string($value);
//         $sql = str_replace(":" . $name . ":", $value, $sql);
//     }

//     return $sql;
// }

function EncodingConvert($inEnc = "UTF-8", $str, $toEnc="UTF-8")
{
    $inEnc=strtoupper($inEnc);
    $result = $str;

    if($inEnc != "UTF-8") {
        switch($inEnc) {
            case "SHIFT_JIS":
                $result = mb_convert_encoding($str, $toEnc, "SJIS");
                break;

            case "EUC-JP":
                $result = mb_convert_encoding($str, $toEnc, "EUC-JP");
                break;

            case "GB2312":
                $result = mb_convert_encoding($str, $toEnc, "GB2312");
                break;

            default:
                $result = mb_convert_encoding($str, $toEnc, "auto");
                break;
        }
    }

    return $result;
}


/**
 * parse the ip to get the country and province into the ip belongs to
 **/
function CvIp($ip='')
{
    if(empty($ip)) $ip = _Cv_Get_Ip();
    if(!preg_match("/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/", $ip)) { return false; }

    if($fd = @fopen(dirname(__FILE__).'/QQWry.Dat', 'rb')) {
        $ip = explode('.', $ip);
        $ipNum = $ip[0]*16777216 + $ip[1]*65536 + $ip[2]*256 + $ip[3];
        $DataBegin = fread($fd, 4);
        $DataEnd = fread($fd, 4);
        $ipbegin = implode('', unpack('L', $DataBegin));

        if($ipbegin < 0) $ipbegin += pow(2, 32);
        $ipend = implode('', unpack('L', $DataEnd));
        if($ipend < 0) $ipend += pow(2, 32);
        $ipAllNum = ($ipend - $ipbegin) / 7 + 1;
        $BeginNum = 0;
        $EndNum = $ipAllNum;

        $ip1num = 0;
        $ip2num = 0;

        while($ip1num > $ipNum || $ip2num < $ipNum) {
            $Middle= intval(($EndNum + $BeginNum) / 2);

            fseek($fd, $ipbegin + 7 * $Middle);
            $ipData1 = fread($fd, 4);
            if(strlen($ipData1) < 4) {
                fclose($fd);

                return 'System Error';
            }

            $ip1num = implode('', unpack('L', $ipData1));
            if($ip1num < 0) $ip1num += pow(2, 32);

            if($ip1num > $ipNum) {
                $EndNum = $Middle;
                continue;
            }

            $DataSeek = fread($fd, 3);
            if(strlen($DataSeek) < 3) {
                fclose($fd);
                return 'System Error';
            }

            $DataSeek = implode('', unpack('L', $DataSeek.chr(0)));
            fseek($fd, $DataSeek);
            $ipData2 = fread($fd, 4);
            if(strlen($ipData2) < 4) {
                fclose($fd);
                return 'System Error';
            }

            $ip2num = implode('', unpack('L', $ipData2));
            if($ip2num < 0) $ip2num += pow(2, 32);
            if($ip2num < $ipNum) {
                if($Middle == $BeginNum) {
                    fclose($fd);
                    return 'Unknown';
                }
                $BeginNum = $Middle;
            }
        }

        $ipFlag = fread($fd, 1);
        if($ipFlag == chr(1)){
            $ipSeek = fread($fd, 3);
            if(strlen($ipSeek) < 3) {
                fclose($fd);
                return 'System Error';
            }

            $ipSeek = implode('', unpack('L', $ipSeek.chr(0)));
            fseek($fd, $ipSeek);
            $ipFlag = fread($fd, 1);
        }

        if($ipFlag == chr(2)) {
            $AddrSeek = fread($fd, 3);
            if(strlen($AddrSeek) < 3) {
                fclose($fd);
                return 'System Error';
            }
            $ipFlag = fread($fd, 1);
            if($ipFlag == chr(2)) {
                $AddrSeek2 = fread($fd, 3);
                if(strlen($AddrSeek2) < 3) {
                    fclose($fd);
                    return 'System Error';
                }
                $AddrSeek2 = implode('', unpack('L', $AddrSeek2.chr(0)));
                fseek($fd, $AddrSeek2);
            } 
            else {
                fseek($fd, -1, SEEK_CUR);
            }

            $ipAddr1 = '';
            $ipAddr2 = '';
            while(($char = fread($fd, 1)) != chr(0))
                $ipAddr2 .= $char;

            $AddrSeek = implode('', unpack('L', $AddrSeek.chr(0)));
            fseek($fd, $AddrSeek);

            while(($char = fread($fd, 1)) != chr(0))
                $ipAddr1 .= $char;
        }
        else {
            $ipAddr1 = '';
            $ipAddr2 = '';

            fseek($fd, -1, SEEK_CUR);
            while(($char = fread($fd, 1)) != chr(0))
                $ipAddr1 .= $char;

            $ipFlag = fread($fd, 1);
            if($ipFlag == chr(2)) {
                $AddrSeek2 = fread($fd, 3);
                if(strlen($AddrSeek2) < 3) {
                    fclose($fd);
                    return 'System Error';
                }
                $AddrSeek2 = implode('', unpack('L', $AddrSeek2.chr(0)));
                fseek($fd, $AddrSeek2);
            }
            else {
                fseek($fd, -1, SEEK_CUR);
            }
            while(($char = fread($fd, 1)) != chr(0))
                $ipAddr2 .= $char;
        }

        fclose($fd);

        if(preg_match('/http/i', $ipAddr2)) {
            $ipAddr2 = '';
        }

        $ipaddr = "$ipAddr1 $ipAddr2";
        $ipaddr = preg_replace('/CZ88\.NET/is', '', $ipaddr);
        $ipaddr = preg_replace('/^\s*/is', '', $ipaddr);
        $ipaddr = preg_replace('/\s*$/is', '', $ipaddr);
        if(preg_match('/http/i', $ipaddr) || $ipaddr == '') {
            $ipaddr = 'Unknown';
        }

        return $ipaddr;
    }
}


function _Cv_Get_Ip()
{
    //$_IpArray = array($_SERVER['HTTP_X_FORWARDED_FOR'], $_SERVER['HTTP_CLIENT_IP'], $_SERVER['REMOTE_ADDR'], getenv('REMOTE_ADDR'));
    $_IpArray = array($_SERVER['REMOTE_ADDR'], getenv('REMOTE_ADDR'));
    rsort($_IpArray);
    reset($_IpArray);
    return $_IpArray[0];
}

function CvIpInfo($ip)
{
    //$ip = "221.219.117.159";

    $geometryInfo = array("country"=>"unknown", "province"=>"unknown");

    $dir = dirname(__FILE__);
    if (!function_exists('geoip_country_code_by_name')) {
        include($dir."/geoipcity.inc");
        include($dir."/geoipregionvars.php");
        $gi = geoip_open($dir."/GeoLiteCity.dat",GEOIP_STANDARD);
        $record = geoip_record_by_addr($gi,$ip);
        if( trim(@$record->country_name) != "") {
            $country = $record->country_name;
        }
        if( trim(@$GEOIP_REGION_NAME[$record->country_code][$record->region]) != "") {
            $city = trim(strtolower($GEOIP_REGION_NAME[$record->country_code][$record->region]));
        }
        geoip_close($gi);
        if(isset($country) && isset($city)) {
            $geometryInfo['country']  = trim(strtolower($country));
            $geometryInfo['province'] = $city;
        }
    } else {
        $ipInfo = @geoip_record_by_name($ip);

        if ($ipInfo && is_array($ipInfo)) {
            $country = trim(strtolower($ipInfo['country_name']));
            $city    = trim(strtolower($ipInfo['city']));

            if($country && $city) {
                $geometryInfo['country']  = $country;
                $geometryInfo['province'] = $city;
            }
        }
    }
    return $geometryInfo;
}




function CvIpInfoChina($ip)
{
    $geometryInfo = array("country"=>"China", "province"=>"unknown");
    $ipInfo = CvIp($ip);

    if ($ipInfo) {
        $geometryInfo['province'] = mb_convert_encoding(mysubstr($ipInfo, 0, 4), "UTF-8", "GB2312");

        foreach($GLOBALS['zh_province'] as $e_province=>$province) {
            if(mb_strpos($geometryInfo['province'], $province) !== FALSE) {
                $geometryInfo['province'] = $province;
                break;
            }
        }
    }

    return $geometryInfo;
}


function mysubstr($str, $start, $len) {
    $tmpstr = "";
    $strlen = $start + $len;

    for($i = $start; $i < $strlen; $i++) {
        if(ord(substr($str, $i, 1)) > 0xa0) {
            $tmpstr .= substr($str, $i, 2);
            $i++;
        }
        else
            $tmpstr .= substr($str, $i, 1);
    }

    return $tmpstr;
}






//yh 20101119

//ip验证函数checkIp($ip,$limit,$flag)
//
function checkIpy($ip,$limit,$type="white"){
//检查设置的IP规则是否正确
    $limitIp_arr=explode(",",$limit);
    $limitIp_count=count($limitIp_arr);
    for($i=0;$i<$limitIp_count;$i++){
        if(!checkIPformat($limitIp_arr[$i])){
            unset($limitIp_arr[$i]);
//            echo "设置的IP规则错误！".$limitIp_arr[$i]."<br/>";
        }
    }
//ip规则通过验证后进行ip匹配 match()
    $flag=false;
    for($i=0;$i<$limitIp_count;$i++){
        if(!empty($limitIp_arr[$i])){
            $rs=IPmatch($ip,$limitIp_arr[$i]);
            if($rs){
                $flag=true;
            }
        }
    }
//白名单

    if( $type == "black" ){
        if($flag == 1){
            return false;
        }else{
            return true;
        }
//黑名单 
    }/*elseif( $type == "white" ){
        if($flag){
            return false;
        }else{
            return true;
        }
    }*/
}

//验证ip格式是否为 a.a.a.* 或a.a.a.a或a.a.a.a.a-b
//^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$ 
function checkIPformat($ip){
    if(ereg("^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$",$ip)) { 
        return true;
    }elseif(ereg("^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.[*]{1}$",$ip)) { 
        return true;
    }elseif(ereg("^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)[-]{1}(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)$",$ip)){
        return true;
    }else{
        return false;
    } 
    
}

function IPmatch($ip,$ip2){
    $lip = explode(".", $ip);
    $rip = explode(".", $ip2);
    if($lip[0]==$rip[0]){
        if($lip[1]==$rip[1]){
            if($lip[2]==$rip[2]){
                if($lip[3]==$rip[3]){
                    return true;
                }elseif($rip[3]=="*"){
                    return true;
                }else{
                    if(ereg("^[0-9]{1,3}[-]{1}[0-9]{1,3}$",$rip[3])){
                        $rip_4=explode("-",$rip[3]);
                        if($rip_4[0]<=$lip[3]&&$lip[3]<=$rip_4[1]){
                            return true;
                        }elseif($rip_4[1]<=$lip[3]&&$lip[3]<=$rip_4[0]){
                            return true;
                        }
                    }
                }
            }
        }
    }else{
        return false;
    }
}




    function changePass($content){
        $temp_true = "";
        $temp_pass = array();
        $temp_pass = explode("/web2/?p=",$content);
        if( isset( $temp_pass[1] ) && !empty( $temp_pass[1] ) ){
            $KEYZ  = "FPSTARjm";
            $crypt = new Des($KEYZ);
            $temp_true = $crypt->decrypt($temp_pass[1]);
            $content = str_replace($temp_pass[1],$temp_true,$content);
            return $content;
        }

    }











?>