#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os

BASE = '/Users/christopherblaisdell/Documents/continuous-architecture-platform-poc-2/services'

for svc in ['svc-check-in','svc-emergency-response','svc-gear-inventory','svc-guide-management',
            'svc-inventory-procurement','svc-payments','svc-reservations','svc-scheduling-orchestrator']:
    report = os.path.join(BASE, svc, 'build/reports/jacoco/test/jacocoTestReport.xml')
    if not os.path.exists(report):
        print(f'{svc}: no report')
        continue
    tree = ET.parse(report)
    root = tree.getroot()
    total_missed = 0
    total_covered = 0
    gaps = []
    for pkg in root.findall('.//package'):
        for cls in pkg.findall('class'):
            name = cls.get('name').split('/')[-1]
            for ctr in cls.findall('counter'):
                if ctr.get('type') == 'LINE':
                    missed = int(ctr.get('missed'))
                    covered = int(ctr.get('covered'))
                    total_missed += missed
                    total_covered += covered
                    if missed > 0:
                        gaps.append(f'  {name}: missed={missed}, covered={covered}')
    ratio = total_covered/(total_missed+total_covered) if (total_missed+total_covered) > 0 else 0
    print(f'{svc}: ratio={ratio:.2f} (missed={total_missed})')
    for g in gaps:
        print(g)
