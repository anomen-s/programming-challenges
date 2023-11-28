#!/bin/sh

echo '###################################'
ls -la *.avi
echo '###################################'

mkdir -p target

for PART in ""
do

TITLE=""
#DIVX=".divx"

if [ -n "$PART" ] ; then PART_PREFIX=".CD" ; fi
TITLE_FULL="${TITLE}${PART_PREFIX}${PART}"

mkvmerge --engage native_mpeg4 --default-language eng -o "target/mkvmerge-${TITLE_FULL}.mkv" \
      --title "$TITLE"  \
      *${PART}.avi

ffmpeg -analyzeduration 200M -probesize 200M  \
       -i *${PART}.avi \
       -i *${PART}.en*.srt \
       -i *${PART}.cz*.srt \
       -attach "cover/dvd-front.jpg"  \
       -attach "info/nfo"  \
       -map 0 -map 1 \
       -map 2  \
       -map 3  \
       -c copy \
       -bsf:v mpeg4_unpack_bframes \
       -metadata:s:a:0 language=eng \
       -metadata:s:s:0 language=eng \
       -metadata:s:s:1 language=cze \
\
       -metadata:s:t:0 mimetype="image/jpeg" \
       -metadata:s:t:0 filename="dvd-front.jpg" \
\
       -metadata:s:t:1 mimetype="text/plain" \
       -metadata:s:t:1 filename="nfo" \
\
       -metadata title="${TITLE_FULL}" \
       -max_interleave_delta 0 \
       "target/${TITLE_FULL}${DIVX}.mkv"
 

done

exit
       -fflags +genpts  \
       -default_mode infer_no_subs \

       -disposition:s:0 default \
       -disposition:s:1 0 \

       -aspect:0 16:9 \

       -codec:v copy \
       -codec:s copy \
       -codec:a libmp3lame -qscale:a 2 \
exit

mkvmerge --engage native_mpeg4 --default-language eng -o "target/${TITLE}.mkv" \
      --title "$TITLE"  \
      *${PART}.avi \
      --language 0:eng *${PART}.eng.srt  \
      --language 0:cze *${PART}.cze.srt  \
      --attachment-mime-type image/jpeg  --attach-file cover/dvd-front.jpg \
      --attachment-mime-type text/plain  --attach-file 'info.txt' \
exit
      --default-track-flag 0:0 \
      --aspect-ratio 0:16/9 \

exit
    application/x-bittorrent
