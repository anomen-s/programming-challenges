<?php

require_once('config.php');

$link = mysql_connect ($DB_HOST, $DB_USER, $DB_PASS);

if (!$link) {
    echo 'Could not connect: ' . mysql_error();
    die();
}

Header('X-Status: Mysql Connected successfully');

//$res = mysql_query("SHOW DATABASES");
//while ($row = mysql_fetch_array($res)) { echo "DB: ".$row['Database'] . "<br />\n"; }

mysql_select_db($DB_DB, $link);
echo  "<br />ERROR:" . mysql_error();

//$res = mysql_query("SHOW TABLES");
//while ($row = mysql_fetch_array($res)) { echo "table: " . $row[0] . "<br />\n"; }

if ($_REQUEST['create'] == "1") {
echo 'creating';
 $result = mysql_query('
CREATE TABLE IF NOT EXISTS fallout_statistika (
login varchar(60),
klice varchar(1000),
penize  int,
jidlo int,
karma int
)');

}
echo  "ERROR:" . mysql_error();

$res=mysql_query("select count(*) from statistiky");
echo "rows:" . mysql_num_rows($res);

mysql_close($link);
