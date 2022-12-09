#!/usr/bin/env python3
import requests
import json
import os
import tempfile

def api_req(endpoint):
  return requests.get('https://api.modrinth.com/v2/{0}'.format(endpoint), headers={
    'User-Agent': '1.18.2 plus+/v0.0.2'
  }).json()

tmp_dir = tempfile.TemporaryDirectory()
working_dir = os.path.join(tmp_dir.name, 'mods')
os.mkdir(working_dir)
with open('docs/mods.md', 'w') as fd0:
  fd0.write('# Mods\nIcon | Name | Version\n--- | --- | ---\n')
  for mod in os.listdir('mods'):
    print('Processing {0}...'.format(os.path.basename(mod).split('.')[0]))
    with open(os.path.join('mods', mod), 'r') as fd1:
      mod_json = json.loads(fd1.read())
    mod_project = api_req('project/{0}'.format(mod_json['project_id']))
    mod_version = api_req('version/{0}'.format(mod_json['version_id']))
    #print(mod_version['files'])
    # Write docs
    fd0.write('<img src="{0}" width=64px height=64px> | [{1}](https://modrinth.com/project/{2}) | {3}\n'.format(
      mod_project['icon_url'],
      mod_project['title'],
      mod_json['project_id'],
      mod_version['version_number']
    ))
    for file in mod_version['files']:
      resp = requests.get(file['url'])
      with open(os.path.join(working_dir, file['filename']), 'wb') as fd1:
        fd1.write(resp.content)
print(os.listdir(working_dir))
tmp_dir.cleanup()
