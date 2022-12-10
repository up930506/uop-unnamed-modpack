#!/usr/bin/env python3
import sys
import os
import json

if len(sys.argv) < 4:
  print('Usage: {0} <name> <project_id> <version_id>'.format(sys.argv[0]))
  exit(1)

with open(os.path.join('mods', '{0}.json'.format(sys.argv[1])), 'w') as fd:
  fd.write(json.dumps({
    'project_id': sys.argv[2],
    'version_id': sys.argv[3]
  }, indent=2))
