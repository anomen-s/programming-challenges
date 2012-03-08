<?php

require_once('custom.php');
require_once('token.php');
require_once('ipcheck.php');


function ohodnot_hrace($klice_str)
{
  $keys = array();
  $keys_nums = preg_match_all('/\b\d+\b/', $klice_str, $keys);
  $klice = array();
  
  foreach ($keys[0] as $k) {
//    echo "<br />klic" . intval($k); // DEBUG
    $klice[intval($k)] = true;
  }
  $vystup = vyhodnot_klice($klice);

  return $vystup;
}

function array_keys_true($keys)
{
  $res = array();
  foreach ($keys as $k => $v) {
    if ($v) {
	$res[] = $k;
    }
  }
  return $res;
}
