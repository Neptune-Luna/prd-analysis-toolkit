"""Read-only paginated GitHub organization inventory; requires authenticated gh."""
import argparse
import datetime as dt
import json
import subprocess
import shutil
import sys
from pathlib import Path


def inventory(org):
    if not org or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-' for c in org):
        raise ValueError('Invalid GitHub organization name')
    executable=shutil.which('gh')
    if not executable:
        raise RuntimeError('GitHub CLI (gh) is unavailable. Use the authenticated GitHub connector, or install/authenticate gh before inventory. No inventory was generated.')
    result = subprocess.run([executable, 'api', '--paginate', '--slurp',
        f'orgs/{org}/repos?type=all&per_page=100'], capture_output=True, text=True,
        encoding='utf-8', check=True)
    pages = json.loads(result.stdout)
    if not isinstance(pages, list) or any(not isinstance(p, list) for p in pages):
        raise ValueError('Unexpected repository pagination response')
    repos = [r for page in pages for r in page]
    if not repos:
        raise ValueError('No repositories returned; verify organization and access')
    keys = ['name', 'full_name', 'html_url', 'clone_url', 'ssh_url', 'default_branch',
            'private', 'archived', 'fork', 'disabled', 'pushed_at', 'description']
    return {'organization': org, 'collected_at': dt.datetime.now(dt.timezone.utc).isoformat(),
        'coverage': 'Repositories visible to the authenticated GitHub identity only',
        'count': len(repos), 'repositories': [dict({k:r.get(k) for k in keys},
            target_ref=None, target_sha=None, baseline_ref=None, baseline_sha=None,
            disposition='unreviewed') for r in sorted(repos,key=lambda x:x['full_name'])]}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--org', default='neptune-robotics')
    ap.add_argument('--out', type=Path, required=True)
    args=ap.parse_args()
    data=inventory(args.org)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"Inventoried {data['count']} accessible repositories: {args.out}")


if __name__=='__main__':
    try:
        main()
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'Inventory failed: {exc}',file=sys.stderr)
        sys.exit(1)
