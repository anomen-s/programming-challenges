
/*
 http://stackoverflow.com/a/8545403/106786
 http://stackoverflow.com/questions/4414077/read-write-bytes-of-float-in-js/8545403#8545403
 https://gist.github.com/kg/2192799
*/

function arrayCheck() {
if (typeof Uint32Array == "undefined") {
  alert('You browser is not supported. Please try another.');
 }
}

function padZero(s){
    var c= '0';
    while(s.length < 8) s= c+ s;
    return s;

}

/**
   converts integer into float
*/
function Bytes2Float32(bytes) {
    var sign = (bytes & 0x80000000) ? -1 : 1;
    var exponent = ((bytes >> 23) & 0xFF) - 127;
    var significand = (bytes & ~(-1 << 23));

    if (exponent == 128) 
        return sign * ((significand) ? Number.NaN : Number.POSITIVE_INFINITY);

    if (exponent == -127) {
        if (significand == 0) return sign * 0.0;
        exponent = -126;
        significand /= (1 << 22);
    } else significand = (significand | (1 << 23)) / (1 << 23);

    return sign * significand * Math.pow(2, exponent);
}


/**
  UNUSED, but might be.
  Typed arrays are used in other functions anyway.
*/
function Bytes2Float32_a(intVal) {
    var arrayf = new Uint32Array([intVal]);
    var buf = arrayf.buffer;
    var view = new Float32Array( buf );
    var flVal = view[0];
    return flVal;
}

function floattobits(num) {
    var arrayf = new Float32Array([num]);
    var buf = arrayf.buffer;
    var view = new Uint32Array( buf );
    var intVal = view[0];
    //alert(intVal);
    return intVal.toString(2);
}


/**
    UNUSED
*/
function floattobits_n(num) {
        // Create 1 entry long Float32 array
        var a = new Float32Array([num]);
        //a.forEach(function(x) { alert(x)});
        //alert('A: ' + JSON.stringify(a))
        var fa = a.buffer;
        alert('FA:' + JSON.stringify(fa))
        //alert('FTB ' +fa.byteLength);
        
        //alert('a: ' + b[0] + ' ' + b[1]  + ' '+ b[2]  + ' '+ b[3]  + ' '+ b[4]  + ' '+ b[5]  + ' '+ b[6] + ' ' + b[7]);
        var res = '';
        for (i = 3; i >= 0 ; i--) {
          res = res + padZero(fa[i].toString(2));
        }
        return res;
}


/* this function is not used */
/*
function testF0() {
   var intVal = 2139095040;
   var c = '00000' + (intVal/17 + 2808133);
   c = c.substr(c.length-10);
   var tr0 = function(n) {
      if (n==4)
       return intVal * n;
      else 
       return intVal * 2 * n;
   }
   var tr = function(c) {
     var tmp1 = intVal;
     var tmp2 = (tmp1*4)/c & 0x3FF;
     return String.fromCharCode(tmp2 >> 2);
   }
   var idx = 0;
   var tr2 = function(len) {
     var res = c.substr(idx, len);
     idx += len;
     return res;
   }
   var coords = tr(95) + tr(126) + tr(151) + tr2(2) + tr(352) + tr2(3) +
                 tr(79) + tr(205) + tr(58) + tr(329) + tr2(2) + tr(110) + tr2(3);
    alert(coords);
}
*/

var currHash = '';

function hashwatch() {
    h = window.location.hash;
    if (h == ('#' + currHash)) {
      currHash = '#' + currHash;
    }
    else if (h != currHash) {
      //alert (h + " X "+  currHash + (h == currHash));
      //alert('rehash : X' + currHash + 'X : X' + h + 'X');
      currHash = h;
      next('WD^r[@]EQA', false);
    }
}

function next(buttonId, inc) {
//alert('next');
 if (window.location.hash == '') {
    var one = floattobits(0.0);
    currHash = window.location.hash = one;
    document.getElementById(decr(buttonId)).value = 'Start';
    return false;
 }
 
 var rawBin = window.location.hash;
 rawBin = rawBin.replace(/[^01]/g, '');
 
 var intVal = parseInt(rawBin, 2); 
 var flVal = Bytes2Float32(intVal);
 if (flVal > 1.5e320) {
   // THIS IS FAKE BRANCH
   var c = padZero('') + (intVal/17 + 33174843);
   c = c.substr(c.length-10);

   var tr = function(c) {
     var tmp1 = intVal;
     var tmp2 = (tmp1*6)/c & 0x3FF;
     return String.fromCharCode(tmp2 >> 3);
   }
   var coords = tr(56) + tr(18) + tr(54) + tr2(3) + tr(22) + tr2(3) +
                 tr(91) + tr(71) + tr(108) + tr(99) + tr2(3) + tr(120) + tr2(3);
   return false;
 }
 if (flVal == 1.4e320) {
   // infinity, c = coords
   var c = padZero('') + (intVal/17 - 55091897);
   c = c.substr(c.length-10);

   // returns char computed from binary result intVal
   // equiv: char(intVal/c & 0xFF)
   var tr = function(c) {
     var tmp1 = intVal;
     var tmp2 = (tmp1*4)/c & 0x3FF;
     return String.fromCharCode(tmp2 >> 2);
   }
   var idx = 0;
   // returns next len substring z c
   var tr2 = function(len) {
     var res = c.substr(idx, len);
     idx += len;
     return res;
   }
   // python generation of coefficients for given char, tr(y)=x
   // import itertools
   // list(itertools.ifilter(lambda(x,y): y==126, zip([chr((2139095040*4/n & 0x3FF) >> 2) for n in range(1,100) ], range(1,10000))))

   var coords = tr(95) + tr(126) + tr(151) + tr2(2) + tr(352) + tr2(3) +
                 tr(79) + tr(205) + tr(58) + tr(329) + tr2(2) + tr(110) + tr2(3);

   document.getElementById(decr(buttonId)).value = coords;
   return false;
 }
 if (inc) {
  // button was pressed, get next value
  var nextFloat = flVal + 1.0;
  //alert("INC: " + flVal + " - " + nextFloat);
  //alert('N: ' + nextFloat);
 
  if (floattobits(nextFloat) == floattobits(flVal)) {
    //alert("no change: curr " + flVal + " = " + nextFloat);
    var nextIntVal = intVal + 1;
    nextFloat = Bytes2Float32(nextIntVal);
  }
 } 
 else {
   // called from timer, just update button
   nextFloat = flVal;
 }
 var nextBits = floattobits(nextFloat);
 currHash = window.location.hash =  nextBits;
 //alert('set hash ' + currHash);
 if (nextFloat == 0.0) {
   nextFloat = 'Start';
 }
 //alert("SET: " +  nextBits + " / "+ nextFloat);
 document.getElementById(decr(buttonId)).value = nextFloat;
 return false;
}

/*
   THIS FUNCTION IS NOT USED, it was just test
*/
function nextFloat() {
  if (window.location.hash == '') {
    var one = floattobits(1.0);
    window.location.hash = one;
  }
 //alert('n');
 var rawBin = document.getElementById('res').value;
 rawBin = rawBin.replace(/[^01]/g, '');
 
 var intVal = parseInt(rawBin, 2); 
 var flVal = Bytes2Float32(intVal);
 if (flVal == Number.POSITIVE_INFINITY) {
   // 2139095040
   // 0128637253 <=> 50.01.286 14.37.253
   // compute as flVal/17 + 2808133
   //
   document.getElementById('res').value = '509019286 149379253'.replace('9','.');
 }
 
 var nextFloat = flVal + 1.0;
  //alert('N: ' + nextFloat);
 
 if (nextFloat == flVal) {
   var nextIntVal = intVal + 1;
   nextFloat = Bytes2Float32(nextIntVal);
 }
 var nextBits = floattobits(nextFloat);
 document.getElementById('res').value =  nextBits;
 document.getElementById('float').value =  nextFloat;
 
 return false;
}


// UNUSED
function convertToFloat() {
 //alert('b');
 var rawBin = document.getElementById('res').value;
 rawBin = rawBin.replace(/[^01]/g, '');
 
 var intVal = parseInt(rawBin, 2); 
 document.getElementById('int').value =  intVal;
 var flVal = Bytes2Float32(intVal);
 document.getElementById('float').value =  flVal;
 return false;
}

// UNUSED
function convertToBits () {
 // alert('b');
 var f = document.getElementById('float').value;
 var res = floattobits(parseFloat(f));
 document.getElementById('res').value =  res;
 return false;
}

function  decr(str)
{
 c = '';
 key = '50014531436773';
 for(i=0; i<str.length; i++) {
    c += String.fromCharCode(str.charCodeAt(i) ^ key.charCodeAt(i % key.length)); // XORing with key
 }
 return c;
}
/**
  unused
*/
/*
function testF() {
   alert(decr('WD^r[@]EQA') == 'btnCounter');
}
*/
