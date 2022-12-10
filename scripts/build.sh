#!/bin/bash
cd modpack
packwiz curseforge export -o curseforge-client.zip -s client
packwiz curseforge export -o curseforge-server.zip -s server
mv curseforge-*.zip ..
