<?php

require_once('custom.php');
require_once('token.php');
require_once('ipcheck.php');


function over_poradi()
{
    $numargs = func_num_args();
    if ($numargs < 3) {
	return false;
    }
    $vstup = func_get_arg(0);
    
    $current = 1;
    $current_val = func_get_arg($current);

    foreach ($vstup as $v) {
	    if ($v == $currentval) {
		$current ++;
		if ($current > $numargs) {
			return true;
		}
		$current_val = func_get_arg($current);
	    }
     }
     return false;
}

function parse_keys($klice_str)
{
  $keys = array();
  $keys_nums = preg_match_all('/\b\d+\b/', $klice_str, $keys);
  $klice = array();
  
  foreach ($keys[0] as $k) {
//    echo "<br />klic" . intval($k); // DEBUG
    $klice[] = intval($k);
  }
  return $klice;
}

function ohodnot_hrace($klice_str)
{
  $klice = parse_keys($U['klice']);

  $U['perky'] = vyhodnot_klice($klice);
  
  if(!over_platnost($U)) {
   /// cheater
   echo "cheater";
   die();
  }
  $U['skore'] = spocti_skore($U, $klice);
}

/**
 * Vrati pole obsahujici klice vstupniho pole, ktere maji hodnotu true.
 *
 * Example: 
 * $v = array( 1=>true, 2=>false, 13=>true);
 * $res = array_keys_true($v);
 * // $res == array(1, 13);
 */
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
