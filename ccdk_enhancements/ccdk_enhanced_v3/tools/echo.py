#!/usr/bin/env python3
import sys, json
print(json.dumps({"echo": sys.argv[1:]}))
