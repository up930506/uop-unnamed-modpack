#!/usr/bin/env python3
import requests
import json
import os
import tempfile
import zipfile

def api_req(endpoint):
  return requests.get('https://api.modrinth.com/v2/{0}'.format(endpoint), headers={
    'User-Agent': '1.18.2 plus+/v0.0.2'
  }).json()

def listdir(directory):
  items = []
  for item in os.listdir(directory):
    item_fpath = os.path.join(directory, item)
    items.append(item_fpath)
    if os.path.isdir(item_fpath):
      for item_nested in listdir(item_fpath):
        items.append(item_nested)
  return items

tmp_dir = tempfile.TemporaryDirectory()
with open('docs/mods.md', 'w') as fd0:
  fd0.write('# Mods\nIcon | Name | Version\n--- | --- | ---\n')
  for mod in os.listdir('mods'):
    print('Processing {0}...'.format(os.path.basename(mod).split('.')[0]))
    with open(os.path.join('mods', mod), 'r') as fd1:
      mod_json = json.loads(fd1.read())
    mod_project = api_req('project/{0}'.format(mod_json['project_id']))
    mod_version = api_req('version/{0}'.format(mod_json['version_id']))
    # Write docs
    fd0.write('<img src="{0}" width=64px height=64px> | [{1}](https://modrinth.com/project/{2}) | {3}\n'.format(
      mod_project['icon_url'],
      mod_project['title'],
      mod_json['project_id'],
      mod_version['version_number']
    ))
    # Download mod files
    for file in mod_version['files']:
      resp = requests.get(file['url'])
      tmp_loc = os.path.join(tmp_dir.name, file['filename'])
      with open(tmp_loc, 'wb') as fd1:
        fd1.write(resp.content)
      with zipfile.ZipFile('modpack.zip', 'a') as fd1:
        fd1.write(tmp_loc, os.path.join('mods', file['filename']))
# Clean up tmp directory
tmp_dir.cleanup()
# Write extra files to archive
with zipfile.ZipFile('modpack.zip', 'a') as fd0:
  for item in listdir('include'):
    fd0.write(item, item.split('include/', 1)[1])
