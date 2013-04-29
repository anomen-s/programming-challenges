<?php
header('Content-type: image/jpeg');

require_once('toolbox.php');
require_once('stats.php');

if (HAVE_DEBUG) {
    header("Cache-Control: no-cache, must-revalidate");
    header("Expires: Fri, 01 Jan 2010 05:00:00 GMT");
    header("Pragma: no-cache");
}


$img = imagecreatefromjpeg("img/tabule.jpg");
//$img = imagecreatetruecolor(600, 800);

$bg = imagecolorallocate($img, 0xd0, 0xd0, 0xd0);
$red_color = imagecolorallocate($img, 0xff, 0x00, 0x00);
$white_color = imagecolorallocate($img, 0xff, 0xff, 0xff);
$text_color = imagecolorallocate($img, 0x00, 0x7f, 0x00);
$ii = chr(0xED);
$aa = chr(0xE1);
$oo = chr(0xF3);
$zz = chr(0xBE);
$ss = chr(0xB9);

$stat_data = dbstats_read();
$i = 0;

foreach($stat_data as $row) {
 
 imagestring($img, 5, 150, 228 + $i*26, "${row['login']}", $white_color);

 imagestring($img, 5, 300, 228 + $i*26, "${row['perky_pocet']}", $white_color);

 imagestring($img, 5, 370, 228 + $i*26, "${row['penize']}", $white_color);

 imagestring($img, 5, 420, 228 + $i*26, "${row['karma']}", $white_color);

 imagestring($img, 5, 480, 228 + $i*26, "${row['jidlo']}", $white_color);

 imagestring($img, 5, 540, 228 + $i*26, "${row['skore']}", $white_color);
 
 $i++;
}

$row = dbstats_avg();
$AVG_Y=625;

 imagestring($img, 5, 300, $AVG_Y, round($row['pp']), $white_color);
 imagestring($img, 5, 370, $AVG_Y, round($row['p']), $white_color);
 imagestring($img, 5, 420, $AVG_Y, round($row['k']), $white_color);
 imagestring($img, 5, 480, $AVG_Y, round($row['j']), $white_color);
 imagestring($img, 5, 540, $AVG_Y, round($row['s']), $white_color);



/*
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
    imagestring($certimg, 5, 900, 740, "C ${U['cheater']}", $text_color);
}
if (!empty($U['perky'])) {
    imagestring($certimg, 5, 350, 400, "Z${ii}skano ${pperku} z 20 mo${zz}ných ocenìn${ii}/perkù", $text_color);
}
imagestring($certimg, 5, 350, 445, "Ocenìn${ii} nemusí být jen kladná a poctivì nelze získat v${ss}echny...", $text_color);
imagestring($certimg, 5, 350, 460, "Nìkteré perky jsou záporné a nez${ii}skáte za nì extra body", $text_color);

imagestring($certimg, 5, 350, 490, "Link na tento certifikát, prosím, pøilo${zz}te ke svému logu na GC.com", $text_color);
imagestring($certimg, 5, 410, 510, "Max score = cca 22000 pro záporáky, hodní získají o trochu ménì.", $text_color);
imagestring($certimg, 5, 595, 550, "It's a harsh world...", $red_color);

  */
imagejpeg($img, NULL, 80);
//imagepng($certimg);
imagedestroy($img);
