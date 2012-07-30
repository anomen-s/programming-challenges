<?php
header('Content-type: image/jpeg');

require_once('toolbox.php');

if (HAVE_DEBUG) {
    header("Cache-Control: no-cache, must-revalidate");
    header("Expires: Fri, 01 Jan 2010 05:00:00 GMT");
    header("Pragma: no-cache");
}

if (empty($_SERVER["QUERY_STRING"])) {
 header('X-Error: no token');
 readfile('img/no.png');
 die;
}

$token = $_SERVER["QUERY_STRING"];

$U = decodeToken($token);

$C_WIDTH = PERK_WIDTH*PERK_COLS + (PERK_COLS-1)*PERK_PADDING + 2*CERT_BORDER;
$C_HEIGHT = PERK_HEIGHT*PERK_ROWS + (PERK_ROWS-1)*PERK_PADDING + 2*CERT_BORDER;
$certimg = imagecreatetruecolor($C_WIDTH, $C_HEIGHT);
$bg = imagecolorallocate($certimg, 0xd0, 0xd0, 0xd0);
$red_color = imagecolorallocate($certimg, 0xff, 0x00, 0x00);
$text_color = imagecolorallocate($certimg, 0x00, 0x7f, 0x00);
$ii = chr(0xED);
$aa = chr(0xE1);
$oo = chr(0xF3);

imagefill($certimg, 0, 0, $bg);

 $bg_img = imagecreatefrompng("img/cert_bg.png");
 imagecopy($certimg, $bg_img, 0, 0, 0, 0,  $C_WIDTH, $C_HEIGHT);


$i = 0;
foreach($U['perky'] as $perk) {
 if (file_exists("perky/$perk.png")) {
   $p = imagecreatefrompng("perky/$perk.png");
 }
 else if (file_exists("perky/$perk.jpg")) {
   $p = imagecreatefromjpeg("perky/$perk.jpg");
 }

 $x = ($i % PERK_COLS) * (PERK_WIDTH + PERK_PADDING);
 $y = floor($i / PERK_COLS) * (PERK_HEIGHT + PERK_PADDING);
 imagecopy($certimg, $p, $x + CERT_BORDER , $y + CERT_BORDER, 0, 0, PERK_WIDTH, PERK_HEIGHT);
 imagedestroy($p);
 $i++;
}

//for ($i=2; $i < 8; $i ++) {
//    imagestring($certimg, 5, PERK_WIDTH * 3 / 2, PERK_HEIGHT * ( $i / 3) ,  'TEST', $red_color);
//}

imagestring($certimg, 5, 250, 10, "${U['login']}", $red_color);
imagestring($certimg, 5, 550, 10, "Z${aa}tky: ${U['penize']}   |   Karma: ${U['karma']}   |    J${ii}dlo: ${U['jidlo']}", $text_color);
imagestring($certimg, 5, 50, 10, "Sk${oo}re ${U['skore']}", $text_color);
if (!empty($U['cheater'])) {
    imagestring($certimg, 5, 900, 740, "Ch ${U['cheater']}", $text_color);
}

imagejpeg($certimg, NULL, 90);
//imagepng($certimg);
imagedestroy($certimg);
