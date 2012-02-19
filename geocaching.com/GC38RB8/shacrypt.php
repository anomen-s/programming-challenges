<?php

function base64_url_encode($input) {
    return strtr(base64_encode($input), '+=', '_-');
}

function base64_url_decode($input) {
    return base64_decode(strtr($input, '_-', '+='));
}

function rand_iv()
{
    $t = time();
    $s = sha1($t);
    return substr($s, 0, 4);
}

function sha1_encrypt($iv, $pass, $plain)
{
 $i = 0;
 $len = strlen($plain);
 $cipher = $pass;
 $result = '';
 while ($i < $len) {
	$cipher = sha1("/$iv/$cipher/$i/$pass/", true);
#	echo "key: /$cipher/$i/$pass/<br />\n";
	$pool = strlen($cipher); // 20
	$chunk = substr($plain, $i, $pool);
	$i += $pool;
	$r = $cipher ^ $chunk;
	$result .= $r;
 }
 return $result;
}

$plaintext = 'test34543 ggopkp 45 34  56 4kl lkklklfwekjerkw rweklj lkj54iojfjddfklrjrltjertr etkrjekltjd';

$iv_r = rand_iv();
echo "iv_r: $iv_r <br />\n";
$iv ='abcdefghjklmnopqrst' ;

$enc = sha1_encrypt($iv_r, $iv, $plaintext);


echo  " <br />\n";
$benc = base64_url_encode($iv_r . $enc);
echo $benc . " <br />\n";
#echo ase64_url_encode($enc) . " <br />\n";

echo "\n<hr />\n";


$dbenc = base64_url_decode($benc);
$iv_r2 = substr($dbenc, 0,4);
echo "iv_r: $iv_r2 <br />\n";
echo substr($dbenc,4);
$dec = sha1_encrypt($iv_r, $iv, substr($dbenc,4));

echo "'$dec' <br />\n";
if ($dec == $plaintext) { echo ' OK '; }

echo "\n<br />\n";

echo urlencode("_-=,.");
