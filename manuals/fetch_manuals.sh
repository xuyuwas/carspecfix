#!/usr/bin/env bash
# carspecfix: download owner manuals that are blocked from the shared box.
# Run on 队长's own Mac (bash 3.2 + BSD tools OK; also Windows Git Bash):
#   bash ~/Downloads/fetch_manuals.sh
# Output: ~/Downloads/carspecfix-manuals/from-captain/ (PDFs + fetch_log.txt + candidates.txt).
# Never aborts on a single failure. 小码 copies the folder to the box afterwards.
set -u
OUT="$HOME/Downloads/carspecfix-manuals/from-captain"; mkdir -p "$OUT" || exit 1
LOG="$OUT/fetch_log.txt"; CAND="$OUT/candidates.txt"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
echo "# run $(date -u +%FT%TZ)  (url<TAB>http_status<TAB>saved_as<TAB>note)" >> "$LOG"
log(){ printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "${4:-}" >> "$LOG"; echo "[$2] $1 -> ${3:--}" >&2; }

# fetch URL to file; keep file only if it is a PDF (or keep as .unknown if non-HTML)
get(){ local url="$1" name="$2" tmp="$OUT/.tmp.$$" code
  code=$(curl -sSL -m 120 --retry 2 -A "$UA" -o "$tmp" -w "%{http_code}" "$url" 2>/dev/null) || code="${code:-000}"
  if [ -s "$tmp" ] && head -c 5 "$tmp" | grep -q '%PDF'; then mv -f "$tmp" "$OUT/$name"; log "$url" "$code" "$name" "pdf"; return 0
  elif [ -s "$tmp" ] && ! head -c 512 "$tmp" | grep -qi '<html\|<!doctype'; then mv -f "$tmp" "$OUT/$name.unknown"; log "$url" "$code" "$name.unknown" "not pdf, kept"; return 1
  else rm -f "$tmp"; log "$url" "$code" "" "html/empty"; return 1; fi; }

# fetch a page, list every .pdf link on it into candidates.txt, print them
pdf_links(){ local page="$1" tag="$2" html code
  html=$(curl -sSL -m 60 -A "$UA" -w $'\n%{http_code}' "$page" 2>/dev/null); code="${html##*$'\n'}"; html="${html%$'\n'*}"
  log "$page" "$code" "" "page scan ($tag)"
  printf '%s' "$html" | grep -oiE 'https?:[^"'"'"' <>]+\.pdf[^"'"'"' <>]*|/[^"'"'"' <>]+\.pdf' | sed 's#\\/#/#g' | sort -u | while read -r u; do
    case "$u" in /*) u="$(echo "$page" | grep -oE '^https?://[^/]+')$u";; esac
    printf '%s\t%s\n' "$tag" "$u" >> "$CAND"; echo "$u"; done; }

try_list(){ local name="$1"; shift; local u; for u in "$@"; do get "$u" "$name" && return 0; done; return 1; }

# 1) Ford F-150 2021 / 2023: scan ford.com manual pages for PDF links, download all candidates
for y in 2021 2023; do n=0
  for page in "https://www.ford.com/support/owner-manuals-details/f150/$y/" \
              "https://www.fordservicecontent.com/Ford_Content/Catalog/owner_information/" ; do
    for u in $(pdf_links "$page" "ford-f150-$y"); do
      case "$u" in *[Oo]wner*|*OM*|*om*|*manual*|*Manual*) n=$((n+1)); get "$u" "ford-$y-f150-owner-manual-$n.pdf";; esac
    done
  done
  [ "$n" -eq 0 ] && log "ford.com/$y" "-" "" "NO PDF LINKS FOUND: open https://www.ford.com/support/owner-manuals-details/f150/$y/ in browser, download 'Owner's Manual' PDF into $OUT/ manually"
done

# 2) Honda 2022 Accord (known pub ATVA2222OM)
try_list "honda-2022-accord-ATVA2222OM.pdf" \
  "https://techinfo.honda.com/rjanisis/pubs/OM/AH/ATVA2222OM/enu/ATVA2222OM.PDF" \
  "http://techinfo.honda.com/rjanisis/pubs/OM/AH/ATVA2222OM/enu/ATVA2222OM.PDF"

# 3) Honda 2022 CR-V: guess pub IDs from Honda's naming, then scan owner pages for PDF links
try_list "honda-2022-crv-owner-manual.pdf" \
  "https://techinfo.honda.com/rjanisis/pubs/OM/AH/A3A02222OM/enu/A3A02222OM.PDF" \
  "https://techinfo.honda.com/rjanisis/pubs/OM/AH/ATMA2222OM/enu/ATMA2222OM.PDF" || {
  n=0
  for page in "https://owners.honda.com/vehicles/information/2022/CR-V/manuals" \
              "https://mygarage.honda.com/s/owners-manuals?vehicle=CR-V&year=2022" \
              "https://techinfo.honda.com/rjanisis/pubs/web/ATM02222.htm"; do
    for u in $(pdf_links "$page" "honda-crv-2022"); do n=$((n+1)); get "$u" "honda-2022-crv-candidate-$n.pdf"; done
  done
  [ "$n" -eq 0 ] && log "honda-crv-2022" "-" "" "NO PDF LINKS FOUND: download 2022 CR-V Owner's Manual PDF from owners.honda.com manually into $OUT/"; }

# 4) Chevrolet 2022 Silverado 1500 / 2022 Equinox: scan Chevrolet manual pages
for m in "silverado-1500:Silverado 1500" "equinox:Equinox"; do slug="${m%%:*}"; n=0
  for page in "https://www.chevrolet.com/support/vehicle/manuals-guides" \
              "https://my.chevrolet.com/how-to-support/manuals-and-guides/2022/$slug"; do
    for u in $(pdf_links "$page" "chevy-$slug-2022"); do
      case "$u" in *2022*|*22*) n=$((n+1)); get "$u" "chevrolet-2022-$slug-candidate-$n.pdf";; esac
    done
  done
  [ "$n" -eq 0 ] && log "chevrolet-$slug-2022" "-" "" "NO PDF LINKS FOUND: download 2022 ${m#*:} Owner's Manual PDF manually into $OUT/"
done

echo; echo "Done. Files in $OUT/:"; ls -la "$OUT"; echo "Log: $LOG"
