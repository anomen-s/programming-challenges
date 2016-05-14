<?php

require_once('config.php');

if (HAVE_MYSQL) {
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
	klice	varchar(300),
	penize	integer,
	jidlo	integer,
	karma	integer,
	perky	varchar(300),
	skore	integer,
	ip	varchar(20),
	ua	varchar(300),
	cert	varchar(500),
	PRIMARY KEY (id)
	)')
	or die("Unable to create table ". mysql_error());
  }

  //$res=mysql_query("select count(*) from fallout_stats");
}

function dbstats_access(&$U)
{
    $params = array('login','klice','penize','jidlo','karma');
    foreach ($params as $p) {
        if (HAVE_MYSQL) {
	    $U["${p}_mysql"] = mysql_real_escape_string($U["${p}"]);
	}
	else {
	    $U["${p}_mysql"] = $U["${p}"];
	}
    }
    $sql = 'INSERT INTO fallout_stats (cas, ip, ua, invalid ';
    foreach ($params as $p) {
	$sql .= ", $p";
    }
    $sql .= ") \nVALUES (now(), '${_SERVER['REMOTE_ADDR']}', '${_SERVER['HTTP_USER_AGENT']}', 'submit' ";
    foreach ($params as $p) {
	$sql .= ", '";
	$sql .= $U["${p}_mysql"] ;
	$sql .= "'";
    }
    $sql .= ")";
    
    sql_log($sql);
    if (HAVE_MYSQL) {
      $result = mysql_query($sql)
	or die("Unable to execute insert: ". mysql_error());
    
      $id = mysql_insert_id();
    } 
    else {
      $id = rand(1, 10000000);
    }  
    $U['id'] = $id;
    return $id;
}

function dbstats_update(&$U, $cert, $invalid)
{
    $id = $U['id'];
    $invalid = empty($invalid) ? 'null' : "'$invalid'";
    $cert = empty($cert) ? 'null' : "'$cert'";
    $skore = empty($U['skore']) ? 'null' : "'${U['skore']}'";
    $perky = empty($U['perky']) ? 'null' : "'" . implode(' ', $U['perky']) . "'" ;
    $sql = " UPDATE fallout_stats ";
    $sql .= " SET ";
    $sql .= " invalid = $invalid, ";
    $sql .= " cert = $cert, ";
    $sql .= " skore = $skore, ";
    $sql .= " perky = $perky " ;
    
    $sql .= " WHERE id = $id ";

    sql_log($sql);
    if (HAVE_MYSQL) {
      $result = mysql_query($sql)
	or die("Unable to execute update: ". mysql_error());
    }
    
}

function dbstats_read($limit = 15)
{
    if (HAVE_MYSQL) {
	$sql = "SELECT *, (LENGTH(perky) - LENGTH(REPLACE(perky, ' ', '')) + 1) AS perky_pocet FROM fallout_stats ";
	$sql .= " WHERE (invalid = '') OR (invalid IS NULL) ";
	$sql .= " ORDER BY skore DESC";
	$sql .= " LIMIT $limit";

        $result = mysql_query($sql)
	    or die("Unable to execute update: ". mysql_error());

	$r = array();
	while ($row = mysql_fetch_assoc($result)) {
	    $r[] = $row;
	}
        return $r;
    }
    else {
	return array();
    }
    
}

function dbstats_avg($limit = 15)
{
    if (HAVE_MYSQL) {
	$sql = "SELECT AVG(perky_pocet) AS pp, AVG(penize) AS p, AVG(jidlo) AS j, AVG(karma) AS k, AVG(skore) AS s FROM (";

	$sql .= " SELECT *, (LENGTH(perky) - LENGTH(REPLACE(perky, ' ', '')) + 1) AS perky_pocet FROM fallout_stats ";
	$sql .= " WHERE (invalid = '') OR (invalid IS NULL) ";
	$sql .= " ORDER BY skore DESC";
	$sql .= " LIMIT $limit";
	$sql .= ") AS topskore";

        $result = mysql_query($sql)
	    or die("Unable to execute update: ". mysql_error());

	return mysql_fetch_assoc($result);
    }
    else {
	return array();
    }
    
}

function sql_log($sql)
{
 $SQL_FILE= TMPDIR . "/sql.txt";

 $fh = fopen($SQL_FILE, 'a');
 fwrite($fh, "$sql;\n");
 fclose($fh);
}
