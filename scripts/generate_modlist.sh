#!/bin/bash
cat << EOF > mods.md
# Mods
Name | Local file | Hash
--- | --- | ---
EOF
for mod in ../mods/*.toml; do
  mod=$(cat "${mod}")
  mod_name=$(echo "${mod}" | sed -nr "s/^name = \"(.*)\"$/\1/p")
  mod_filename=$(echo "${mod}" | sed -nr "s/^filename = \"(.*)\"$/\1/p")
  mod_hash_format=$(echo "${mod}" | sed -nr "s/^hash-format = \"(.*)\"$/\1/p")
  mod_hash=$(echo "${mod}" | sed -nr "s/^hash = \"(.*)\"$/\1/p")
  echo "${mod_name} | ${mod_filename} | ${mod_hash} (${mod_hash_format})" >> mods.md
done
