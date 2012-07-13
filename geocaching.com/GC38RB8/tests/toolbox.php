<?php
 require_once "tests.php";
 require_once "../toolbox.php";
 

$zadano = array(10,20,30,40);
assertTrue(PORADI($zadano, 10, 20, 30, 40));

assertTrue(PORADI($zadano, 1, 10, 30, 40));

assertFalse(PORADI($zadano, 20, 10, 30, 40));
