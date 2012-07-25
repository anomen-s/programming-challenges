<?php
 require_once "tests.php";
 require_once "../toolbox.php";
 

$zadano = array(10,20,30,40);
assertTrue(PORADI($zadano, 10, 20, 30, 40));

assertTrue(PORADI($zadano, 1, 10, 30, 40));

assertFalse(PORADI($zadano, 20, 10, 30, 40));

assertTrue(PORADI(array(20), 20, 10, 30, 40));
assertTrue(PORADI(array(10), 20, 10, 30, 40));


$U = array();
$U['keylist'] = $zadano;
assertTrue(MA_KLICE($U, 20, 10, 30, 40));
assertFalse(MA_KLICE($U, 20, 10, 30, 50));
assertFalse(MA_KLICE($U, 50));
assertTrue(MA_KLICE($U));
