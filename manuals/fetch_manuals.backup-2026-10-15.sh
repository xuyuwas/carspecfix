#!/bin/bash
# 在队长电脑上一次性下载手册。用法: bash fetch_manuals.sh urls.txt
# urls.txt 每行: 文件名<TAB>官方URL
out="$HOME/Downloads/carspecfix-manuals"; mkdir -p "$out"
log="$out/sources.tsv"; echo -e "file\turl\tfetched_at\thttp" > "$log"
while IFS=$'\t' read -r name url; do
  [ -z "$url" ] && continue
  code=$(curl -sSL -m 60 -A "Mozilla/5.0" -o "$out/$name" -w "%{http_code}" "$url")
  echo -e "$name\t$url\t$(date -u +%FT%TZ)\t$code" >> "$log"
done < "$1"
cat "$log"
