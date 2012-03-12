<?php

// heslo pro generovani certifikatu
define ('PASSWORD', "my secRet passw0rd_1");

// adresar pro docasne soubory (ip check)
define ('TMPDIR', '/tmp');

// pocet pokusu za den
define ('MAX_TRIES_PER_DAY', '2');

// velikost obrazku (perky)
define("PERK_WIDTH", 140);
define("PERK_HEIGHT", 140);


/**
 * Vyhodnoti zadany vstup a vrati seznam perku.
 * Vstup i vystup jsou pole, kde klic je identifikator a hodnota je true/false
 */
function vyhodnot_klice($vstup)
{
	$vystup = array();

	if ($vstup[1]) {
	    $vystup[102] = true;
	    
	}

	if ($vstup[2]) {
	    $vystup[101] = true;
	    
	}

	if ($vstup[3]) {
	    $vystup[104] = true;
	    
	}

	if ($vstup[6]) {
	    $vystup[102] = true;
	    $vystup[104] = true;
	    $vystup[101] = true;
	}


	if ($vstup[1] && $vstup[9]) {
	    $vystup[101] = false;
	    $vystup[104] = true;
	    
	}
  

	if ($vstup[1] && $vstup[2]) {
	    $vystup = array();
	    $vystup[104] = true;
	    
	}
  
  

	return $vystup;
}

/**
 * spocita body
 */
function spocti_skore($U)
{
    return count($U['perky']) + $U['karma'] + $U['penize'] + $U['jidlo'];
}
