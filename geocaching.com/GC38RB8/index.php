<html>
<head>
 <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
 <link rel='stylesheet' type='text/css' href='styles.css' />
</head>
<body>

<?php

require_once('toolbox.php');

$login = $_REQUEST['login'];
$login_safe = htmlentities($login, ENT_QUOTES);

$klice = $_REQUEST['klice'];
$klice_safe = htmlentities($klice, ENT_QUOTES);

?>

<?php if (empty($klice)) { ?>
<form method="post">
<div id="input_div">

<div id="form_login">
<label for="login" title="Login na geocaching.com:">Jméno</label><br />
<input type="text" name="login" id="login" value="<?php echo $login_safe; ?>" />
</div>

<div id="form_klice">
<label for="klice" >Nalezené klíče:</label>
<br />
<textarea cols="30" rows=8" name="klice" id="klice"><?php echo $klice_safe;  ?></textarea>
</div>

<div>
<input type="submit" id="form_submit" />
</div>

</div>
</form>

<?php } ?>

<br />
<p>
<?php

if (!empty($klice)) {
  echo "<div id=\"result\">\n";

  echo "volam  ohodnot_hrace($klice)"; // DEBUG
  $perky = ohodnot_hrace($klice);
  foreach($perky as $perk => $val) {
	if (!empty($val)) {
		echo "<br /><img src='perky/perk_$perk.jpg'/>\n";
	}
  }
  

  echo "<hr /> odkaz pro zalogovani:<br />\n";
  
  $token = sha1_encrypt("my secret password", "$login/$klice");
  $token_b64 = base64_url_encode($token);
  $script="http://${_SERVER['SERVER_NAME']}:${_SERVER['SERVER_PORT']}${_SERVER['SCRIPT_NAME']}";
  echo "<tt>[url=$script?$token_b64][/url] </tt><br />\n";
  echo "</div>\n";

}



?>

</p>

</body>
</html>



