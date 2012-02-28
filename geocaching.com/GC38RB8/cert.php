<?php
header('Content-type: image/png');

require_once('toolbox.php');

if (empty($_SERVER["QUERY_STRING"])) {
 header('X-Error: no token');
 readfile('img/no.png');
 die;
}

$token = $_SERVER["QUERY_STRING"];


  
//$token = sha1_encrypt("my secret password", "$login/$klice");
//$token_b64 = base64_url_encode($token);
//$script="http://${_SERVER['SERVER_NAME']}:${_SERVER['SERVER_PORT']}${_SERVER['SCRIPT_NAME']}";
//echo "<tt>[url=$script?$token_b64][/url] </tt><br />\n";
//echo "</div>\n";

  $U = decodeToken($token);
  
// header('X-Token: ' . $token);
// DEV
//$perks = explode('!', $token);


$certimg = imagecreatetruecolor(PERK_WIDTH*3+100, PERK_HEIGHT*3+100);
$bg = imagecolorallocate($certimg, 0xd0, 0xd0, 0xd0);
imagefill($certimg, 0, 0, $bg);


$i = 0;
foreach($U['perky'] as $perk) {
 $p = imagecreatefromjpeg("perky/perk_$perk.jpg");
 $x = ($i % 3) * PERK_WIDTH;
 $y = floor($i / 3) * PERK_HEIGHT;
 imagecopy($certimg, $p, $x + 50 , $y + 50, 0, 0,  PERK_WIDTH, PERK_HEIGHT);
 imagedestroy($p);
 $i++;
}

$text_color = imagecolorallocate($certimg, 0xff, 0x00, 0x00);
for ($i=2; $i < 8; $i ++) {
    imagestring($certimg, 5, PERK_WIDTH * 3 / 2, PERK_HEIGHT * ( $i / 3) ,  'TEST', $text_color);
}

$text_color = imagecolorallocate($certimg, 0x00, 0xff, 0x00);
$ii = chr(0xED);
imagestring($certimg, 5, 20, 10,  "${U[login]}", $text_color);
imagestring($certimg, 5, 20, 30,  "Pen${ii}ze: ${U[penize]}   |   Karma: ${U[karma]}   |    J${ii}dlo: ${U[jidlo]}", $text_color);

//imagejpeg($certimg, NULL, 100);
imagepng($certimg);
imagedestroy($certimg);
