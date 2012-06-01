<?php

require_once('config.php');

$link = mysql_connect ($DB_HOST, $DB_USER, $DB_PASS);

if (!$link) {
    echo 'Could not connect to database: ' . mysql_error();
    die();
}

Header('X-Status: Mysql Connected successfully');

mysql_select_db($DB_DB, $link) or die("Unable to select database: ". mysql_error());

if ($_REQUEST['db_create'] == $DB_CREATE) {
  echo 'creating db<br />';

 $result = mysql_query('DROP TABLE  fallout_stats')
	or die("Unable to drop table: ". mysql_error());

 $result = mysql_query('
	CREATE TABLE IF NOT EXISTS fallout_stats (
	id      integer not null AUTO_INCREMENT,
	cas	datetime,
	invalid	varchar(200),
	login	varchar(100),
	klice	varchar(200),
	penize	integer,
	jidlo	integer,
	karma	integer,
	perky	varchar(200),
	skore	integer,
	ip	varchar(20),
	ua	varchar(300),
	cert	varchar(200),
	PRIMARY KEY (id)
	)')
	or die("Unable to create table ". mysql_error());
}

$res=mysql_query("select count(*) from fallout_stats");

function dbstats_access(&$U)
{
    $params = array('login','klice','penize','jidlo','karma');
    foreach ($params as $p) {
	$U["${p}_mysql"] = mysql_real_escape_string($U["${p}"]);
    }
    $sql = 'INSERT INTO fallout_stats (cas, ip, ua, invalid ';
    foreach ($params as $p) {
	$sql .= ", $p";
    }
    $sql .= ") \nVALUES (now(), '${_SERVER['REMOTE_ADDR']}', '${_SERVER['HTTP_USER_AGENT']}', ${U['invalid']} ";
    foreach ($params as $p) {
	$sql .= ", '";
	$sql .= $U["${p}_mysql"] ;
	$sql .= "'";
    }
    $sql .= ")";
//    echo $sql;
    
    $result = mysql_query($sql)
	or die("Unable to execute insert: ". mysql_error());
    
    $id = mysql_insert_id();
    $U['id'] = $id;
    return $id;
}

function dbstats_update(&$U, $cert)
{
    $id = $U['id'];
    $invalid = empty($U['invalid']) ? 'null' : "'${U['invalid']}'";
    $perky = implode(',', $U['perky']);
    $sql = " UPDATE fallout_stats ";
    $sql .= " SET ";
    $sql .= "  skore = ${U['skore']}, ";
    $sql .= "  cert = '$cert', ";
    $sql .= "  invalid = $invalid, ";
    $sql .= "  perky = '$perky'" ;
    
    $sql .= " WHERE (skore IS NULL) AND (id = $id) ";
    
    $result = mysql_query($sql)
	or die("Unable to execute update: ". mysql_error());
    
}

