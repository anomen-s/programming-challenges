<?php
 require_once "tests.php";
 require_once "../token.php";

{
 $perky = StrToPerky("038zz1999abc");
 $diff = array_diff($perky, array('038','zz1','999','abc'));
 assertEquals(0, count($diff));
}

{
 $perky = StrToPerky("");
 $diff = array_diff($perky, array());
 assertEquals(0, count($diff));
}

$U=array('login'=>'l','karma'=>11, 'penize'=>10,'jidlo'=>3,'skore'=>100);
$U['perky'] = array(10,20,40);
//$U['perky'] = array();

$t = getToken($U);
//echo $t;

$U2=decodeToken($t);

echo "$t\n";
print_r($U2);

