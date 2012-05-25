<?php

// heslo pro generovani certifikatu
define ('PASSWORD', "my secRet passw0rd_1");

// adresar pro docasne soubory (ip check)
define ('TMPDIR', '/tmp');

// omezit pocet pokusu za den
define ('LIMIT_TRIES_PER_DAY', false);

// pocet pokusu za den
define ('MAX_TRIES_PER_DAY', 2);


// velikost obrazku (perky)
define("PERK_WIDTH", 140);
define("PERK_HEIGHT", 140);


/** 
 *
 */
function over_platnost($U)
{
  $vstup = $U['keylist'];
  $v = true;
  $v &= PORADI($vstup, 1, 3, 5, 9);
  $v &= PORADI($vstup, 4, 5);
  
  return $v;
}


/**
 * Vyhodnoti zadany vstup a vrati seznam perku.
 * Vstup i vystup jsou pole identifikatoru indexovane poradim.
 * Perky by se mely pridavat jen jednou.
 */
function vyhodnot_klice($U)
{
	$vstup = $U['keylist'];

	$vystup = array();

	// pokud uziv. zadal 1 dej perk 102
	if (in_array(1, $vstup)) { 
	    $vystup[] = '102';
	    
	}

	if (in_array(2, $vstup)) {
	    $vystup[] = '101';
	}

	if (in_array(3, $vstup)) {
	    $vystup[] = '104';
	}

	// pokud uziv. zadal 6 dej perky 102, 104,101
	if (in_array(6, $vstup)) {
	    $vystup[] = '102';
	    $vystup[] = '104';
	    $vystup[] = '101';
	}

	// pokud uziv. zadal 1 a 9
	if (in_array(1, $vstup) && in_array(9, $vstup)) {

	    // odstranit 101; mazani je komplikovane
	    $key101 = array_search(101, $vystup);
	    if ($key101 !== FALSE) {
		unset($vystup[$key101]);
	    }
	    
	    $vystup[] = '104';
	}
  

	if (in_array(1, $vstup) && in_array(2, $vstup)) {
	    $vystup = array(104);
	}
  
	$U['perky'] = $vystup;
}

/**
 * spocita body
 */
function spocti_skore($U)
{
    $sk = count($U['perky']) + $U['karma'] + $U['penize'] + $U['jidlo'];

    $U['skore'] = $sk;
}
