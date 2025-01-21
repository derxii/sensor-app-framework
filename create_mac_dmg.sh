#!/bin/bash
set -euo pipefail

APP_NAME="Sensor Data Visualiser"
APP_PATH="dist/$APP_NAME.app"
DMG_SRC_PATH="dist/dmg"
DMG_OUTPUT_PATH="dist/$APP_NAME Installer.dmg"

VOL_ICON="icon.icns"


mkdir -p "$DMG_SRC_PATH"
rm -rf "${DMG_SRC_PATH:?}/"*
cp -r "$APP_PATH" "$DMG_SRC_PATH"

test -f "$DMG_OUTPUT_PATH" && rm "$DMG_OUTPUT_PATH"

create-dmg \
  --volname "$APP_NAME Installer" \
  --volicon "$VOL_ICON" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "$APP_NAME" 175 120 \
  --hide-extension "$APP_NAME" \
  --app-drop-link 425 120 \
  "$DMG_OUTPUT_PATH" \
  "$DMG_SRC_PATH"