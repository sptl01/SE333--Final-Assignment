#!/usr/bin/env python3
"""
Simple JaCoCo XML parser that extracts coverage counters and prints a summary.
Usage: python scripts/parse_jacoco.py [path/to/jacoco.xml]
If no path is given it will try `maven-projects/target/site/jacoco/jacoco.xml`.
"""
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

DEFAULT_PATH = Path('maven-projects/target/site/jacoco/jacoco.xml')

def parse_counters(elem):
    counters = {}
    for c in elem.findall('counter'):
        t = c.get('type')
        missed = int(c.get('missed', '0'))
        covered = int(c.get('covered', '0'))
        counters[t] = {'missed': missed, 'covered': covered}
    return counters


def summarize_report(path: Path):
    if not path.exists():
        print(f'File not found: {path}')
        return 2
    tree = ET.parse(path)
    root = tree.getroot()

    report = {'path': str(path), 'packages': []}
    total = {}

    for pkg in root.findall('package'):
        pkg_name = pkg.get('name')
        pkg_summary = {'name': pkg_name, 'classes': []}
        for cls in pkg.findall('class'):
            cls_name = cls.get('name')
            srcfile = cls.get('sourcefilename')
            cls_counters = parse_counters(cls)
            pkg_summary['classes'].append({
                'name': cls_name,
                'sourcefile': srcfile,
                'counters': cls_counters
            })
            # accumulate totals
            for k, v in cls_counters.items():
                if k not in total:
                    total[k] = {'missed': 0, 'covered': 0}
                total[k]['missed'] += v['missed']
                total[k]['covered'] += v['covered']
        report['packages'].append(pkg_summary)

    # also extract sourcefile counters if present at sourcefile level
    sourcefiles = []
    for sf in root.findall('.//sourcefile'):
        sf_name = sf.get('name')
        sf_counters = parse_counters(sf)
        sourcefiles.append({'name': sf_name, 'counters': sf_counters})

    # compute percentages for totals
    total_summary = {}
    for k, v in total.items():
        missed = v['missed']
        covered = v['covered']
        total_lines = missed + covered
        pct = (covered / total_lines * 100) if total_lines > 0 else 0.0
        total_summary[k] = {'missed': missed, 'covered': covered, 'total': total_lines, 'pct': round(pct,2)}

    # print human-readable summary
    print('\nJaCoCo coverage summary for:', path)
    print('Totals:')
    for k, v in total_summary.items():
        print(f" - {k}: {v['covered']}/{v['total']} covered ({v['pct']}%)")
    print('')

    for pkg in report['packages']:
        print(f"Package: {pkg['name']}")
        for cls in pkg['classes']:
            name = cls['name']
            sf = cls['sourcefile']
            ctr = cls['counters']
            line = ctr.get('LINE', {'covered':0,'missed':0})
            method = ctr.get('METHOD', {'covered':0,'missed':0})
            instr = ctr.get('INSTRUCTION', {'covered':0,'missed':0})
            branch = ctr.get('BRANCH', {'covered':0,'missed':0})
            print(f"  - Class {name} (source: {sf})")
            print(f"    * Lines: {line['covered']}/{line['covered']+line['missed']} covered")
            print(f"    * Methods: {method['covered']}/{method['covered']+method['missed']} covered")
            print(f"    * Instructions: {instr['covered']}/{instr['covered']+instr['missed']} covered")
            print(f"    * Branches: {branch['covered']}/{branch['covered']+branch['missed']} covered")
        print('')

    if sourcefiles:
        print('Sourcefile-level counters:')
        for sf in sourcefiles:
            lf = sf['counters'].get('LINE', {'covered':0,'missed':0})
            print(f" - {sf['name']}: {lf['covered']}/{lf['covered']+lf['missed']} lines covered")

    # output JSON summary to stdout as well
    output = {'totals': total_summary, 'packages': report['packages'], 'sourcefiles': sourcefiles}
    print('\nJSON summary:')
    print(json.dumps(output, indent=2))
    return 0


if __name__ == '__main__':
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    rc = summarize_report(path)
    sys.exit(rc)
