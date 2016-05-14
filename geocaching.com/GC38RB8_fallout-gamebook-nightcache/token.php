<?php

require_once('phpseclib/AES.php');

define('SEED_LENGTH', 3);

function base64_url_encode($input) {
    return strtr(base64_encode($input), '+', '_');
}

function base64_url_decode($input) {
    return base64_decode(strtr($input, '_', '+'));
}

function aes_encrypt($pass, $plaintext)
{
    $aes = new Crypt_AES(CRYPT_AES_MODE_CTR);

    $size = 32;
    $i = 'a';
    while (strlen($pass) < $size) {
            $pass .= $i;
            $i++;
    }
    $aes->setKey($pass);

    return $aes->encrypt($plaintext);
}

function aes_decrypt($pass, $cipher)
{
    $aes = new Crypt_AES(CRYPT_AES_MODE_CTR);

    $size = 32;
    $i = 'a';
    while (strlen($pass) < $size) {
            $pass .= $i;
            $i++;
    }
    $aes->setKey($pass);

    return $aes->decrypt($cipher);
}

function perkyToStr($U)
{
  $res = '';
  foreach ($U['perky'] as $perk) {
     $i = substr($perk,0,3);
     $res .= $i;
  }
  return $res;
}

function StrToPerky($strlist)
{
 $perky = array();
 $count = strlen($strlist) / 3;
 for ($i = 0; $i < $count; $i++) {
    $perky[] = substr($strlist, $i*3, 3);
 }
 //print_r($perky);
 return $perky;
}

function getToken($U)
{
  $perkyStr = perkyToStr($U);
  $seed = str_pad('', SEED_LENGTH, 'x');
  $plain = "$seed${U['login']}!${U['karma']}!${U['penize']}!${U['jidlo']}!${U['skore']}!${U['cheater']}!$perkyStr";
  while (strlen($plain) % 3 != 0) { // pad to base64 block
   $plain .= ' ';
  }
  $sha = sha1(PASSWORD . $plain, true);
  for ($i = 0; $i < SEED_LENGTH; $i++) {
    $plain{$i} = $sha{$i};
  }

  $token = aes_encrypt(PASSWORD, $plain);
  $token_b64 = base64_url_encode($token);
  return $token_b64;
}

function decodeToken($token)
{
  $U = array();
  $token_raw = base64_url_decode($token);
  $token_dec = aes_decrypt(PASSWORD, $token_raw);

  $token_check = $token_dec;
  for ($i = 0; $i < SEED_LENGTH; $i++) {
    $token_check{$i} = 'x';
  }
  header('X-Token: '.$token_check );
  $sha = sha1(PASSWORD . $token_check, true);

  if (substr($token_dec,0,SEED_LENGTH) != substr($sha,0,SEED_LENGTH)) {
    // error
    header('X-Error: sha1fail');
    readfile('img/no.png');
    die;
  }
  header('X-Token: ' . $token_check);
  
  $U['token'] = $token;
  $U['token_dec'] = $token_check;
  
  $data = substr($token_check, SEED_LENGTH);
  $token_list = explode('!', trim($data));
  $U['login'] = array_shift($token_list);
  $U['karma'] = array_shift($token_list);
  $U['penize'] = array_shift($token_list);
  $U['jidlo'] = array_shift($token_list);
  $U['skore'] = array_shift($token_list);
  $U['cheater'] = array_shift($token_list);
  $p = StrToPerky(array_shift($token_list));
  $U['perky'] = expandPerks($p);
  
  return $U;
}

function readPerkdir()
{
    $files = array();
    if ($handle = opendir('perky')) {
    /* This is the correct way to loop over the directory. */
    while (false !== ($f = readdir($handle))) {
        if (strlen($f) >= 7) {
            $idx = substr($f, 0, 3);
            $ext = substr($f, -4);
            $name = substr($f, 0, -4);
    	    if (($ext == '.jpg') || ($ext == '.png')) {
        	 $files[$idx] = $name;
        	 $files[$name] = $name;
    	    }
        }
    }
    }
    closedir($handle);
    return $files;
}

function expandPerks($perks)
{
  $files = readPerkdir();
  $res = array();
  foreach ($perks as $p) {
    $res[] = $files[$p];
  }
  return $res;
}
