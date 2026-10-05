#!/usr/bin/env python3
"""Small honest integration corpus; not a compiler-conformance claim."""
import json
from pathlib import Path
import subprocess
import sys

binary = str(Path(sys.argv[1]).resolve())
root = Path(__file__).resolve().parents[1]
cases = json.loads((root / 'fixtures/cases.json').read_text())

def run(command, path):
    return subprocess.run([binary, command, str(path)], capture_output=True, text=True)

symbols_seen = 0
for filename, expected in cases['good'].items():
    path = root / 'fixtures' / filename
    raw = path.read_bytes()
    result = run('symbols', path)
    assert result.returncode == 0, (filename, result.stderr)
    data = json.loads(result.stdout)
    assert data['schema_version'] == 1 and data['complete'] is True
    rows = data['symbols']
    assert [row['name'] for row in rows] == expected, (filename, rows)
    for row in rows:
        start, end = row['start_byte'], row['end_byte']
        assert 0 <= start < end <= len(raw), (filename, row)
        raw[start:end].decode('utf-8')
        assert row['start'] == raw[:start].count(b'\n') + 1, (filename, row)
        assert row['end'] == raw[:end].count(b'\n') + 1, (filename, row)
    symbols_seen += len(rows)
    for command in ['tokens', 'parse', 'outline', 'tags']:
        result = run(command, path)
        assert result.returncode == 0, (filename, command, result.stderr)
    result = run('check', path)
    assert result.returncode != 0, 'Reader-only package must not advertise check'
    result = run('symbols-recovered', path)
    assert result.returncode != 0, 'No recovered-symbol capability without an oracle'
for filename in cases['bad']:
    path = root / 'fixtures' / filename
    for command in ['symbols']:
        result = run(command, path)
        assert result.returncode != 0, (filename, command, 'malformed source accepted')
        if command == 'symbols':
            assert not result.stdout.strip(), (filename, 'partial declarations leaked as strict symbols')
print(f"{len(cases['good'])} valid files, {len(cases['bad'])} malformed files, {symbols_seen} symbol ranges verified")
