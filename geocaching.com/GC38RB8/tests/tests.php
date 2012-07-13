<?php
function assertEquals($expected, $value)
{
 if ($expected !== $value) {
   echo "Received \"" . $value . "\". Instead of expected value: \"" . $expected . "\".\n";
 }
}



function assertTrue($value)
{
 return assertEquals(true, $value);
}

function assertFalse($value)
{
 return assertEquals(false, $value);
}

