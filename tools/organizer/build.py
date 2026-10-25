"""Build organize-Personal.bat: a one-click Windows command that rearranges F:\\Personal to match Personal/.

The .bat carries organize.ps1 plus a manifest of every file under Personal/ (SHA-256, size, path),
the hashes of every older file this repo ever held (so stale copies get set aside), and the text
files themselves (READMEs, HTML pages) so it can write the ones the user doesn't have yet.

Usage: python3 -I tools/organizer/build.py <out.bat>
"""
import base64
import hashlib
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EMBED_EXT = ('.md', '.csv', '.html')
MIN_OBSOLETE = 64  # tiny blobs (empty files, one-line configs) could match unrelated files

HEADER = (
    '@echo off\r\n'
    'chcp 65001 >nul\r\n'
    'set "ORG_SELF=%~f0"\r\n'
    'powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=[IO.File]::ReadAllText($env:ORG_SELF,[Text.Encoding]::UTF8);'
    "$a=$s.IndexOf('#PS'+'-START');$b=$s.IndexOf('#PS'+'-END');iex $s.Substring($a,$b-$a)\"\r\n"
    'echo.\r\n'
    'pause\r\n'
    'exit /b\r\n'
)


def git(*args):
    return subprocess.check_output(['git', '-C', REPO, *args])


def main(out):
    rows, current = [], set()
    for rel in git('-c', 'core.quotepath=off', 'ls-files', '-z', 'Personal').decode().split('\0'):
        if not rel:
            continue
        with open(os.path.join(REPO, rel), 'rb') as f:
            body = f.read()
        h = hashlib.sha256(body).hexdigest()
        current.add(h)
        win = rel[len('Personal/'):].replace('/', '\\')
        rows.append(f'M\t{h}\t{len(body)}\t{win}')
        if rel.endswith(EMBED_EXT):
            rows.append(f'E\t{win}\t{base64.b64encode(body).decode()}')

    blobs = [l.split()[0] for l in git('rev-list', '--objects', '--all').decode().splitlines()]
    p =subprocess.run(['git', '-C', REPO, 'cat-file', '--batch-check=%(objecttype) %(objectname) %(objectsize)'],
                       input='\n'.join(blobs).encode(), capture_output=True, check=True)
    old = set()
    for line in p.stdout.decode().splitlines():
        kind, oid, size = line.split()
        if kind != 'blob' or int(size) < MIN_OBSOLETE:
            continue
        h = hashlib.sha256(git('cat-file', 'blob', oid)).hexdigest()
        if h not in current and h not in old:
            old.add(h)
            rows.append(f'O\t{h}\t{size}')

    with open(os.path.join(REPO, 'tools', 'organizer', 'organize.ps1'), encoding='utf-8') as f:
        ps = f.read()
    with open(out, 'w', encoding='utf-8', newline='') as f:
        f.write(HEADER + '#PS-START\r\n' + ps + '\r\n#PS-END\r\n#DATA\r\n' + '\r\n'.join(rows) + '\r\n')
    print(out, len(current), 'files,', len(old), 'old versions')


if __name__ == '__main__':
    main(sys.argv[1])
