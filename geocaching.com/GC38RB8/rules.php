<?php



/**
 * Vyhodnoti zadany vstup a vrati seznam perku.
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


