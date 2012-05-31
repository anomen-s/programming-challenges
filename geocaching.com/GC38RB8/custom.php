<?php

require_once('config.php');

// adresar pro docasne soubory (ip check)
define ('TMPDIR', './ipcheck');

// omezit pocet pokusu za den
define ('LIMIT_TRIES_PER_DAY', false);

// pocet pokusu za den
define ('MAX_TRIES_PER_DAY', 2);


// velikost obrazku (perky)
define("PERK_WIDTH", 140);
define("PERK_HEIGHT", 140);


/**
 * Otestuje platnost zadanych klicu
 */
function over_platnost(&$U)
{
  $vstup = $U['keylist'];
  $v = true;
  $v &= PORADI($vstup, 1,  5, 9);
  if (in_array(6, $vstup)) {
    $v &= PORADI($vstup, 5,  6, 9);
  } 
  else if (in_array(8, $vstup)) {
    $v &= PORADI($vstup, 5,  8, 9);
  }
  else {
    $v = false;
  }

  return $v;
}


/**
 * Vyhodnoti zadany vstup a vrati seznam perku.
 * Vstup i vystup jsou pole identifikatoru indexovane poradim.
 * Perky by se mely pridavat jen jednou.
 */
function vyhodnot_klice(&$U)
{
	// pokud uziv. zadal 1 dej perk 102
	if (MA_KLICE($U,1)) {
	    PRIDEJ_PERK($U, '102');
//	    $vystup[] = '102';
	    
	}

	if (MA_KLICE($U,2)) {
	    PRIDEJ_PERK($U, '101');
	}

	if (MA_KLICE($U,3)) {
	    PRIDEJ_PERK($U, '104');
	}

	// pokud uziv. zadal 6 dej perky 102, 104,101
	if (MA_KLICE($U,6)) {
	    PRIDEJ_PERK($U, '102', '104', '101');
	}

	// pokud uziv. zadal 1 a 9
	if (MA_KLICE($U,1,9)) {
	    ODEBER_PERK($U, '101');
	    PRIDEJ_PERK($U, '104');
	}
}

/**
 * spocita body
 */
function spocti_skore(&$U)
{
    
    $sk = 100*count($U['perky']) + 10*$U['karma'] + 20*$U['penize'] + $U['jidlo'];
    
    if (in_array(6, $U['keylist'])) {
	$sk +=200;
    }

    $U['skore'] = $sk;
}
