"""Validate the local Teacher Workbench package without network access."""
from pathlib import Path
from zipfile import ZipFile
import ast
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    skills = sorted((ROOT / 'skills').glob('tw-*'))
    assert len(skills) == 45, 'Expected all 45 skill folders'
    names = {p.name for p in skills}
    assert 'Copyright (c) 2026 Jason Miles' in (ROOT/'license.md').read_text()
    assert (ROOT/'readme.md').is_file()
    catalog = json.loads((ROOT / 'skill-catalog.json').read_text())
    assert {row['name'] for row in catalog['skills']} == names
    assert catalog['skill_count'] == 45
    policies = set()
    link_count = 0
    for folder in skills:
        skill = (folder / 'SKILL.md').read_text()
        assert skill.startswith('---\n')
        front = skill.split('---', 2)[1]
        match = re.search(r'^name: ([a-z0-9-]+)$', front, re.M)
        assert match and match.group(1) == folder.name
        assert re.search(r'^description: .+', front, re.M)
        assert len(folder.name) < 64
        ui = (folder / 'agents/openai.yaml').read_text()
        assert 'Teacher Workbench' in ui and '$' + folder.name in ui
        policies.add(hashlib.sha256((folder/'references/grounding-and-citations.md').read_bytes()).hexdigest())
        for path in folder.rglob('*'):
            if not path.is_file():
                continue
            assert path.suffix != '.pyc' and '__pycache__' not in path.parts
            if path.suffix == '.py':
                ast.parse(path.read_text())
            if path.suffix == '.json':
                json.loads(path.read_text())
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            assert not re.search('tosagpt', text, re.I), path
            for ref in re.findall(r'\btw-[a-z0-9]+(?:-[a-z0-9]+)*', text):
                assert ref in names, (path, ref)
            if path.suffix == '.md':
                for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text):
                    if re.match(r'^[A-Za-z]+:', target) or target.startswith('#'):
                        continue
                    target = target.split('#')[0]
                    if target:
                        assert (path.parent / target).exists(), (path, target)
                        link_count += 1
    assert len(policies) == 1, 'Shared grounding policies have drifted'
    guide = (ROOT/'docs/USER_GUIDE.md').read_text()
    assert names <= set(re.findall(r'\btw-[a-z0-9]+(?:-[a-z0-9]+)*', guide))
    for extension in ('docx', 'pdf'):
        assert (ROOT/f'docs/USER_GUIDE.{extension}').stat().st_size > 10000
    archives = sorted((ROOT/'skill-packages').glob('*.zip'))
    assert {p.stem for p in archives} == names
    for archive in archives:
        with ZipFile(archive) as z:
            assert z.testzip() is None
            folder = ROOT/'skills'/archive.stem
            expected = {p.relative_to(folder).as_posix(): p.read_bytes()
                        for p in folder.rglob('*') if p.is_file()}
            expected['license.md'] = (ROOT/'license.md').read_bytes()
            assert set(z.namelist()) == set(expected)
            assert 'SKILL.md' in z.namelist()
            assert len(z.namelist()) <= 21, 'Conservative Cowork companion-file limit'
            assert archive.stat().st_size < 10 * 1024 * 1024
            assert sum(i.file_size for i in z.infolist()) < 10 * 1024 * 1024
            for member, content in expected.items():
                assert z.read(member) == content
    sums = (ROOT/'skill-packages/SHA256SUMS').read_text().splitlines()
    assert len(sums) == 45
    for line in sums:
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((ROOT/'skill-packages'/name).read_bytes()).hexdigest() == digest
    docs = [ROOT/'readme.md', ROOT/'docs/PUBLISHING.md', ROOT/'docs/VALIDATION.md']
    docs += list((ROOT/'docs/platforms').glob('*.md'))
    for path in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', path.read_text()):
            if re.match(r'^[A-Za-z]+:', target) or target.startswith('#'):
                continue
            assert (path.parent / target.split('#')[0]).exists(), (path, target)
    print(json.dumps({'status':'passed','skills':45,'skill_local_links':link_count,'individual_skill_archives':len(archives),'shared_policy_copies':45}))

if __name__ == '__main__':
    main()
