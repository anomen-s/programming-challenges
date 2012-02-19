<?php
$plaintext = 'test';

$td = mcrypt_module_open('rijndael-256', '', 'ofb', '');
$iv = mcrypt_create_iv(mcrypt_enc_get_iv_size($td), MCRYPT_DEV_RANDOM);
$ks = mcrypt_enc_get_key_size($td);

/* Create key */
$key = substr(md5('very secret key'), 0, $ks);

/* Intialize encryption */
mcrypt_generic_init($td, $key, $iv);


$cipherdata = mcrypt_generic($td, $plaintext);


echo "Result: " . base64_encode ($cipherdata) . "<br />\n";

/* Terminate encryption handler */
mcrypt_generic_deinit($td);
        
/* Initialize encryption module for decryption */
mcrypt_generic_init($td, $key, $iv);
                
$res = mdecrypt_generic($td, $cipherdata);

$res = rtrim($res, "\0");

echo "Result: $res";

/* Terminate decryption handle and close module */
mcrypt_generic_deinit($td);
mcrypt_module_close($td);
