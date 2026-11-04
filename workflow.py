"""Portable simulation records. Python standard library only; never runs a solver."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def contained(root, name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Use a relative POSIX file path')
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Path must stay inside case directory')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Symlink escapes case directory')
    return path


def create(root, case_id, files):
    records = []
    for name in files:
        path = contained(root, name)
        if not path.is_file():
            raise ValueError(f'Not a file: {name}')
        records.append({'path': name, 'sha256': digest(path)})
    return {'schema_version': 1, 'case_id': case_id,
            'objective': 'Describe the intended calculation',
            'parameters': [], 'files': records, 'run_status': 'not_started',
            'checks': [], 'limitations': ['No physical validation has been recorded'],
            'next_action': 'Define acceptance checks before running'}


def review(root, data):
    issues = []
    if not isinstance(data, dict):
        return {'record_valid': False, 'validation': 'not_established',
                'issues': ['Manifest must be an object']}
    for key in ('case_id', 'objective', 'next_action'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            issues.append(f'Missing nonempty text: {key}')
    if data.get('schema_version') != 1:
        issues.append('Unsupported schema_version')
    status = data.get('run_status')
    if status not in ('not_started', 'running', 'completed', 'failed', 'stopped', 'unknown'):
        issues.append('Invalid run_status')
    files = data.get('files')
    indexed = set()
    if not isinstance(files, list) or not files:
        issues.append('files must be a nonempty list')
        files = []
    for item in files:
        try:
            if not isinstance(item, dict):
                raise ValueError('File record must be an object')
            name = item.get('path')
            path = contained(root, name)
            if name in indexed:
                issues.append(f'Duplicate file: {name}')
            indexed.add(name)
            if not path.is_file():
                issues.append(f'Missing file: {name}')
            elif digest(path) != item.get('sha256'):
                issues.append(f'Hash mismatch: {name}')
        except (ValueError, OSError) as error:
            issues.append(str(error))
    parameters = data.get('parameters')
    if not isinstance(parameters, list):
        issues.append('parameters must be a list')
    else:
        for item in parameters:
            if (not isinstance(item, dict) or not item.get('name')
                    or 'value' not in item or not item.get('unit')):
                issues.append('Each parameter needs name, value and unit (use 1 for dimensionless)')
    if not isinstance(data.get('limitations'), list):
        issues.append('limitations must be a list')
    checks = data.get('checks')
    if not isinstance(checks, list):
        issues.append('checks must be a list')
        checks = []
    passed = True
    failed = False
    for check in checks:
        if not isinstance(check, dict):
            issues.append('Check must be an object')
            passed = False
            continue
        outcome = check.get('status')
        if outcome not in ('pass', 'fail', 'not_run'):
            issues.append('Invalid check status')
        if not check.get('name') or not check.get('criterion'):
            issues.append('Check needs name and criterion')
        evidence = check.get('evidence')
        if outcome in ('pass', 'fail') and (not isinstance(evidence, str) or evidence not in indexed):
            issues.append('Executed check needs evidence in files')
        passed = passed and outcome == 'pass'
        failed = failed or outcome == 'fail'
    validation = 'not_established'
    if failed:
        validation = 'reported_checks_failed'
    elif not issues and status == 'completed' and checks and passed:
        validation = 'reported_checks_passed'
    return {'record_valid': not issues, 'validation': validation, 'issues': issues}


def handoff(data, result):
    files = data.get('files') if isinstance(data.get('files'), list) else []
    limitations = data.get('limitations') if isinstance(data.get('limitations'), list) else []
    return '\n'.join([
        '# Simulation handoff', '', f"Case: {data.get('case_id', 'unknown')}",
        f"Objective: {data.get('objective', 'unknown')}",
        f"Run status (reported): {data.get('run_status', 'unknown')}",
        f"Record integrity: {'valid' if result['record_valid'] else 'invalid'}",
        f"Validation: {result['validation']}", '',
        'This tool checks record structure and file hashes. It does not verify physical correctness.',
        '', '## Evidence files', *[f"- {f['path']}" for f in files if isinstance(f, dict) and 'path' in f],
        '', '## Record issues', *[f'- {x}' for x in result['issues']],
        '', '## Declared limitations', *[f'- {x}' for x in limitations],
        '', '## Next action', str(data.get('next_action', 'Not specified')), ''])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('case_dir', type=Path)
    init.add_argument('--id', required=True)
    init.add_argument('--files', nargs='+', required=True)
    init.add_argument('--output', type=Path, required=True)
    for name in ('check', 'handoff'):
        cmd = sub.add_parser(name)
        cmd.add_argument('manifest', type=Path)
        if name == 'handoff':
            cmd.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            if args.output.resolve().parent != args.case_dir.resolve():
                raise ValueError('Manifest must be saved directly inside case_dir')
            content = json.dumps(create(args.case_dir, args.id, args.files), indent=2) + '\n'
        else:
            data = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
            result = review(args.manifest.parent, data)
            if args.command == 'check':
                print(json.dumps(result, indent=2))
                return 0 if result['record_valid'] else 1
            if not isinstance(data, dict):
                raise ValueError('Manifest must be an object')
            content = handoff(data, result)
        with args.output.open('x', encoding='utf-8') as stream:
            stream.write(content)
        return 0
    except (OSError, ValueError, TypeError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
