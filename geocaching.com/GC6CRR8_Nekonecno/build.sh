#!/bin/sh

mkdir -p target

if [ ! -f target/yuicompressor.jar ]
then
 wget 'https://github.com/yui/yuicompressor/releases/download/v2.4.8/yuicompressor-2.4.8.jar' -O target/yuicompressor.jar  || exit 1
fi

cp -v infinity.css target/i.css

for IMGFILE  in images/*.png
do
 echo "$IMGFILE"
 IMGDATA=`base64 -w 0 "$IMGFILE"`

 sed -i -e "s@url(\"$IMGFILE\")@url(\"data:image/png;base64,$IMGDATA\")@" target/i.css
done

echo "CSS.."
java -jar target/yuicompressor.jar target/i.css > target/io.css
echo "JavaScript.."
java -jar target/yuicompressor.jar infinity.js > target/io.js

head -n 5 infinity.html > target/i.html
echo '<!-- ' >> target/i.html
#git rev-parse HEAD >> target/i.html
git describe --always >> target/i.html
echo " // "  >> target/i.html
date >> target/i.html

echo ' -->' >> target/i.html

echo '<style type="text/css">' >> target/i.html
cat target/io.css >> target/i.html
echo '</style>' >> target/i.html

echo '<script>' >> target/i.html
echo '/* <![CDATA[ */' >> target/i.html
cat target/io.js >> target/i.html
echo '/* ]]> */' >> target/i.html
echo '</script>' >> target/i.html

tail -n +10 infinity.html >> target/i.html

#xmllint --noblanks --xmlout --dropdtd  target/i.html -o target/ix.html
tr -d '\n' < target/i.html > target/infinity.html

echo DONE
sleep 1
