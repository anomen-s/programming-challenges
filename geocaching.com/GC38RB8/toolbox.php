<?php
require_once('rules.php');

function base64_url_encode($input) {
    return strtr(base64_encode($input), '+=', '_-');
}

function base64_url_decode($input) {
    return base64_decode(strtr($input, '_-', '+='));
}


function sha1_encrypt($pass, $plain)
{
 $i = 0;
 $len = strlen($plain);
 $cipher = $pass;
 $result = '';
 while ($i < $len) {
	$cipher = sha1("/$cipher/$i/$pass/", true);
#	echo "key: /$cipher/$i/$pass/<br />\n";
	$pool = strlen($cipher); // 20
	$chunk = substr($plain, $i, $pool);
	$i += $pool;
	$r = $cipher ^ $chunk;
	$result .= $r;
 }
 return $result;
}


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