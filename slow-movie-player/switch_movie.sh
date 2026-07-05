#!/bin/bash
# Schaltet den Slow Movie Player auf einen anderen Film um.
# Auf dem Pi ablegen unter ~/SlowMovie/switch_movie.sh (chmod +x nicht vergessen).
#
# Aufruf:  ./switch_movie.sh "Pulp Fiction"     (Teilname reicht, Gross/Klein egal)
#          ./switch_movie.sh                    (listet alle verfuegbaren Filme)

set -e
cd "$(dirname "$0")"

if [ -z "$1" ]; then
    echo "Verfuegbare Filme:"
    ls -1 Videos/
    exit 0
fi

MATCH=$(find Videos/ -maxdepth 1 -type f -iname "*$1*" | head -n 1)

if [ -z "$MATCH" ]; then
    echo "Kein Film gefunden fuer: $1"
    echo "Verfuegbare Filme:"
    ls -1 Videos/
    exit 1
fi

# 'file'-Eintrag in der Conf setzen (oder anhaengen, falls nicht vorhanden)
if grep -q "^file" slowmovie.conf 2>/dev/null; then
    sed -i "s|^file.*|file = $MATCH|" slowmovie.conf
else
    echo "file = $MATCH" >> slowmovie.conf
fi

sudo systemctl restart slowmovie
echo "Laeuft jetzt: $MATCH"
