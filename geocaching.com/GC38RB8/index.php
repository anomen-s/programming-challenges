<?php

header("Cache-Control: no-cache, must-revalidate");
header("Expires: Fri, 01 Jan 2010 05:00:00 GMT");
header("Pragma: no-cache");

require_once('toolbox.php');

$U = array();
$params = array('login','klice','penize','jidlo','karma');

foreach ($params as $p) {
    if (isset($_REQUEST[$p])) {
        $U[$p] = $_REQUEST[$p];
        $U["${p}_safe"] = htmlentities($U[$p], ENT_QUOTES);
        
    }
}

?>
<html>
<head>
 <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
 <link rel='stylesheet' type='text/css' href='styles.css' />
</head>
<body>

<?php if (empty($_REQUEST['form_submit'])) { ?>

<form method="post">
<div id="input_div">

<div id="form_login">
<label for="login" title="Login na geocaching.com:">Jméno</label><br />
<input type="text" name="login" id="login" value="<?php echo $U['login_safe']; ?>" />
</div>

<div id="form_karma">
<label for="karma">Karma:</label>
<br />
<input type="text" name="karma" id="karma" value="<?php echo $U['karma_safe']; ?>" />
</div>

<div id="form_penize">
<label for="penize">Vydělané peníze:</label>
<br />
<input type="text" name="penize" id="penize" value="<?php echo $U['penize_safe']; ?>" />
</div>

<div id="form_jidlo">
<label for="jidlo">Jídlo:</label>
<br />
<input type="text" name="jidlo" id="jidlo" value="<?php echo $U['jidlo_safe']; ?>" />
</div>

<div id="form_klice">
<label for="klice">Nalezené klíče:</label>
<br />
<textarea cols="30" rows=8" name="klice" id="klice"><?php echo $U['klice_safe'];  ?></textarea>
</div>

<div>
<input type="submit" name="form_submit" id="form_submit" />
</div>

</div>
</form>

<?php } else {

 dbstats_access($U);
 
 // TODO: check integers
 //	dbstats_update($U, '', 'invalid values');

 echo "<div id=\"result\">\n";

 if (!ip_check()) {
	echo "<p><span style=\"color:red;font-weight:bold\">OPAKOVANY POKUS</span></p>\n";
	dbstats_update($U, '', 'retry_limit_reached');
    if (LIMIT_TRIES_PER_DAY) {
	echo "</div></body></html>\n";
	die;
    }
 }

//  echo "volam  ohodnot_hrace(${U['klice']})"; // DEBUG
  ohodnot_hrace($U);

  echo '<div id="perky_preview">';
  foreach($U['perky'] as $perk) {
	echo "<img src='perky/perk_$perk.jpg'/>\n";
  }
  echo '</div>';

  echo "<hr /> odkaz pro zalogovani:<br />\n";

 //echo "<pre>U=";print_r($U);echo "</pre>";
   
  $token_b64 = getToken($U);
  
  dbstats_update($U, $token_b64, '');
  
  $script="http://${_SERVER['SERVER_NAME']}:${_SERVER['SERVER_PORT']}"
       . str_replace('index.php','cert.php', $_SERVER['SCRIPT_NAME']) 
       . "?$token_b64";
       

    if (HAVE_DEBUG) {
	echo "<pre>";
	print_r($U);
	echo "</pre>";
    }
//  $script="http://${_SERVER['SERVER_NAME']}:${_SERVER['SERVER_PORT']}/~guppy/fallout/cert.php?$token_b64";
  
  //TEST
//  $script = 'http://guppy.zemeplocha.info:10080/~guppy/fallout/cert.php?' . implode('/', array_keys($perky));
  
//  echo "<a href=\"$script\">[url=$script][/url] </a><br />\n";
  echo "<a href=\"$script\">CERTIFIKÁT</a><br />\n";

  echo "</div>\n";

//  print_r(decodeToken($token_b64));


}
?>

</body>
</html>
