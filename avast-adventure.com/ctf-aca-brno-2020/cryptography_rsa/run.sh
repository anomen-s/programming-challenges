#!/bin/sh

### setup
mkdir -p target

wget -O target/rsatool.py https://github.com/ius/rsatool/raw/master/rsatool.py

### extract key
openssl rsa -in rsa.public -pubin -text -modulus > target/rsa.detail.pem
#gives
E=1594693
N=0x175ADB7387753EB83F84D25A59BED5C5C9AB7706F74F25F1C9B64AC920CFABF9

### factorize
# online
# https://www.alpertron.com.ar/ECM.HTM

# tool: https://sourceforge.net/projects/yafu/
# factor(0x175ADB7387753EB83F84D25A59BED5C5C9AB7706F74F25F1C9B64AC920CFABF9)

Q=102779990028966175942724097182047923667
P=102779990028966175942723097882046923651

### create private key
python3 target/rsatool.py -v -p "$P" -q "$Q" -e "$E" > target/private.pem


### decrypt
openssl rsautl -decrypt -in encrypted -inkey target/private.pem


exit



λ(n) = lcm(p − 1, q − 1)
     =  lcm(2 × 3 × 482 251727 × 11 841663 031921 × 2999 651703 292733 ,
            2 × 5**2 × 43 × 439 × 699 974981 × 155569 004856 914809 963129 )
     =  (2 * 3 * 482251727 * 11841663031921 * 2999651703292733) *
            (5 * 5 * 43 * 439 * 699974981 * 155569004856914809963129 )
     = 5281863175177193274150891601480268530201747873734808735490059339232665050450



# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

d = 1442925105216642664833130466251794586235890327606049870653036284036710262457

#od encrypted -t x1 -A none | tr -d '[[:space:]]' > target/c
c ???

#python
pow(c,d,λ)


