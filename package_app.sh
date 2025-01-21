#!/bin/bash
set -euo pipefail

DATA_FLAG=""
STYLE_DATA_FLAG=""

case "$(uname -sr)" in

   Darwin*|Linux*)
     DATA_FLAG='--add-data=src/resources:resources'
     STYLE_DATA_FLAG='--add-data=src/frontend/style.qss:frontend'
     ;;

   CYGWIN*|MINGW*|MSYS*)
     DATA_FLAG='--add-data=src/resources;resources'
     STYLE_DATA_FLAG='--add-data=src/frontend/style.qss;frontend'
     ;;

   *)
     echo 'OS Not Supported'
     exit 1;
     ;;
esac

pyinstaller \
  --name='Sensor Data Visualiser' \
  "$DATA_FLAG" \
  "$STYLE_DATA_FLAG" \
  --windowed \
  --icon='icon.icns' \
  --paths="src" \
  src/app.py