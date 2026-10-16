# Individual skill uploads

Each `tw-*.zip` contains `SKILL.md` at its root, the complete skill resources, and `license.md`. Use these archives for hosts that accept single-skill ZIPs. See the [platform installation guides](../docs/platforms/readme.md).

The canonical editable files live in `../skills/`. Rebuild uploads from the repository root with:

```sh
python3 -B tools/build_skill_archives.py
```

`SHA256SUMS` records the ZIP hashes. The package validator checks these hashes and compares every archive member with its source. A complete repository download contains 45 skills; it is not a single-skill upload.
