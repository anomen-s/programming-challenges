<?php
 require_once "tests.php";
 require_once "../token.php";
 define('PASSWORD', 'pass12345678');


$U=array('login'=>'l','karma'=>11, 'penize'=>10,'jidlo'=>3,'skore'=>100);
$U['perky'] = array(10,20,40);
//$U['perky'] = array();

$t = getToken($U);
//echo $t;

$U2=decodeToken($t);

echo "$t\n";
print_r($U2);

