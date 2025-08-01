#!/usr/bin/env python3
# Minimal Queen/Worker orchestrator stub
import argparse, pathlib, sqlite3, json, os, sys, subprocess, time

BASE = pathlib.Path('.ccd_hive')
BASE.mkdir(exist_ok=True)

def start(session):
    sesdir = BASE / session
    sesdir.mkdir(exist_ok=True)
    db = sqlite3.connect(sesdir/'memory.db')
    db.execute('CREATE TABLE IF NOT EXISTS notes(ts INTEGER, role TEXT, content TEXT)')
    db.commit()
    print(f'🐝 Hive "{session}" started. Memory DB at {sesdir}/memory.db')

def status():
    for ses in BASE.iterdir():
        if ses.is_dir():
            db = sqlite3.connect(ses/'memory.db')
            c = db.execute('SELECT COUNT(*) FROM notes').fetchone()[0]
            print(f'{ses.name}: {c} memory rows')
    if not any(BASE.iterdir()):
        print('No hives running.')

def stop(session):
    sesdir = BASE/session
    if sesdir.exists():
        print(f'Shutting down hive {session}')
        # compact / backup memory
        bkp = sesdir / f'memory_{int(time.time())}.db.bak'
        os.rename(sesdir/'memory.db', bkp)
        print(f'Memory backed up to {bkp}')
    else:
        print('Session not found')

parser = argparse.ArgumentParser()
parser.add_argument('cmd', choices=['start','status','stop'])
parser.add_argument('name', nargs='?')
args = parser.parse_args()

if args.cmd=='start':
    start(args.name or 'default')
elif args.cmd=='status':
    status()
elif args.cmd=='stop':
    stop(args.name or 'default')
