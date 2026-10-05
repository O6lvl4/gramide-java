#!/usr/bin/env python3
"""Parse-only javac fixture oracle; never resolve dependencies or execute input."""
from pathlib import Path
import json, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/'fixtures/cases.json').read_text())
with tempfile.TemporaryDirectory() as temp:
    subprocess.run(['java','-m','jdk.compiler/com.sun.tools.javac.Main','-d',temp,str(ROOT/'ci/JavaParseOracle.java')],check=True)
    count=0
    for valid,paths in [(True,cases['good']), (False,cases['bad'])]:
        for relative in paths:
            p=subprocess.run(['java','-cp',temp,'JavaParseOracle',str(ROOT/'fixtures'/relative)],capture_output=True,text=True,check=True)
            result=json.loads(p.stdout)
            assert result['valid']==valid,(relative,result)
            count+=1
print(f'javac parse-only oracle: {count} valid/malformed fixtures agree; no type checking or source execution')
