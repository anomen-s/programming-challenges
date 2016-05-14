<?php


function ip_check()
{
 $ip = $_SERVER["REMOTE_ADDR"];
 $today = date('Y-m-d');
 $TODAY_FILE= TMPDIR . "/fallout_${today}.txt";
// echo $TODAY_FILE;

 if (file_exists ($TODAY_FILE)) {
    $fdata  = file($TODAY_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $data = array_count_values($fdata);
 }
 else {
    $data = array();
 }

// echo "\nRES = ";
 
 if (!isset($data[$ip]) || ($data[$ip] < MAX_TRIES_PER_DAY)) {
  // ok 
    $fh = fopen($TODAY_FILE, 'a');
    fwrite($fh, "$ip\n");
    fclose($fh);
  
    return true;
 } else {
    // error - forbidden
    return false;
 }
}
