#!/bin/bash
# publish.sh KEY : build spec KEY and copy outputs into the repo series folder
set -e
W=/tmp/claude-0/-home-user-Deyaa/8ad431fe-808a-58d4-bc96-46a0f1f04d0c
REPO="/home/user/Deyaa/ملخصات تراث ابن تيمية - الشيخ حسين عبد الرازق"
K=$1
rm -rf "$W/work/out/$K"
python3 -I "$W/scripts/build.py" "$W/work/specs/$K.json" "$W/work/out/$K"
F=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['folder'])" "$W/work/specs/$K.json")
mkdir -p "$REPO/$F"
cp "$W/work/out/$K/"*.pdf "$W/work/out/$K/"*.png "$REPO/$F/"
echo "$REPO/$F"
