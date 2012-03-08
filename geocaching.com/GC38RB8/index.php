<html>
<head>
 <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
 <link rel='stylesheet' type='text/css' href='styles.css' />
</head>
<body>

<?php

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

<?php if (empty($U['klice'])) { ?>
<form method="post">
<div id="input_div">

<div id="form_login">
<label for="login" title="Login na geocaching.com:">Jméno</label><br />
<input type="text" name="login" id="login" value="<?php echo $U['login_safe']; ?>" />
</div>

<div id="form_karma">
<label for="karma" >Karma:</label>
<br />
<input type="text" name="karma" id="karma" value="<?php echo $U['karma_safe']; ?>" />
</div>

<div id="form_penize">
<label for="penize" >Vydělané peníze:</label>
<br />
<input type="text" name="penize" id="penize" value="<?php echo $U['penize_safe']; ?>" />
</div>

<div id="form_jidlo">
<label for="jidlo" >Jídlo:</label>
<br />
<input type="text" name="jidlo" id="jidlo" value="<?php echo $U['jidlo_safe']; ?>" />
</div>

<div id="form_klice">
<label for="klice" >Nalezené klíče:</label>
<br />
<textarea cols="30" rows=8" name="klice" id="klice"><?php echo $U['klice_safe'];  ?></textarea>
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


if (!empty($U['klice'])) {
  echo "<div id=\"result\">\n";

if (!ip_check()) {
    echo "<span style=\"color:red;font-weight:bold\">OPAKOVANY POKUS</span>";
}

//	  echo "volam  ohodnot_hrace(${U['klice']})"; // DEBUG
  $perky = ohodnot_hrace($U['klice']);
  foreach($perky as $perk => $val) {
	if (!empty($val)) {
		echo "<br /><img src='perky/perk_$perk.jpg'/>\n";
	}
  }

  echo "<hr /> odkaz pro zalogovani:<br />\n";
  
  $token_b64 = getToken($U, array_keys_true($perky));
  $script="http://${_SERVER['SERVER_NAME']}:${_SERVER['SERVER_PORT']}" .  str_replace('index.php','cert.php', $_SERVER['SCRIPT_NAME']) . "?$token_b64";
//  $script="http://${_SERVER['SERVER_NAME']}:${_SERVER['SERVER_PORT']}/~guppy/fallout/cert.php?$token_b64";
  
  //TEST
//  $script = 'http://guppy.zemeplocha.info:10080/~guppy/fallout/cert.php?' . implode('/', array_keys($perky));
  
//  echo "<a href=\"$script\">[url=$script][/url] </a><br />\n";
  echo "<a href=\"$script\">$token_b64</a><br />\n";
  echo "</div>\n";

//  print_r(decodeToken($token_b64));
}


?>

</p>

</body>
</html>
