import json
import glob
import os
import itertools
import numpy as np

def get_json(fn):
    with open(fn) as f:
        return json.loads(f.read())

def consolidate_edge_reports(pairs, input, output):

    report = {}
    # for each edge report, create key based on filename
    for pair, fn in zip(pairs, input):
        report[pair] = get_json(fn)

    with open(output, 'w') as jsonfile:
        json.dump(report, jsonfile)

    return

def report_template():
    report = {}
    report['reps'] = -1

    report['num-edges-dist'] = []

    report['avg-num-edges'] = -1
    report['std-num-edges'] = -1

    report['avg-edges-removed'] = -1
    report['std-edges-removed'] = -1

    report['avg-cycles-removed'] = -1
    report['std-cycles-removed'] = -1

    report['avg-spurious'] = -1
    report['std-spurious'] = -1

    report['avg-cycle-spurious'] = -1
    report['std-cycle-spurious'] = -1

    report['avg-wrongfully-purged'] = -1
    report['std-wrongfully-purged'] = -1

    report['avg-cycle-wrongfully-purged'] = -1
    report['std-cycle-wrongfully-purged'] = -1
    return report


def consolidate_replicates(files):
    report = {}

    report['reps'] = [ get_json(files[i]) for i in range(len(files)) ]

    report['num-edges-dist'] = [f['filter-report']['num_edges'] + f['filter-report']['num_edges_removed'] for f in report['reps']]

    report['avg-num-edges'] = np.mean([f['filter-report']['num_edges'] + f['filter-report']['num_edges_removed'] for f in report['reps']])
    report['std-num-edges'] = np.std([f['filter-report']['num_edges']  + f['filter-report']['num_edges_removed'] for f in report['reps']])

    report['avg-edges-removed'] = np.mean([f['filter-report']['num_edges_removed'] for f in report['reps']])
    report['std-edges-removed'] = np.std([f['filter-report']['num_edges_removed'] for f in report['reps']])

    report['avg-cycles-removed'] = np.mean([f['cycle-report']['num_edges_removed'] for f in report['reps']])
    report['std-cycles-removed'] = np.std([f['cycle-report']['num_edges_removed'] for f in report['reps']])

    report['avg-spurious'] = np.mean([len(f['filter-report']['spurious_edges']) for f in report['reps']])
    report['std-spurious'] = np.std([len(f['filter-report']['spurious_edges']) for f in report['reps']])

    report['avg-cycle-spurious'] = np.mean([len(f['cycle-report']['spurious_edges']) for f in report['reps']])
    report['std-cycle-spurious'] = np.std([len(f['cycle-report']['spurious_edges']) for f in report['reps']])

    report['avg-wrongfully-purged'] = np.mean([len(f['filter-report']['wrongfully_purged_edges']) for f in report['reps']])
    report['std-wrongfully-purged'] = np.std([len(f['filter-report']['wrongfully_purged_edges']) for f in report['reps']])

    report['avg-cycle-wrongfully-purged'] = np.mean([len(f['cycle-report']['wrongfully_purged_edges']) for f in report['reps']])
    report['std-cycle-wrongfully-purged'] = np.std([len(f['cycle-report']['wrongfully_purged_edges']) for f in report['reps']])


    return report

def get_all_chain_reports():
    return glob.glob("./p*/data/hivtrace/8*edge_report.json")

if __name__ == "__main__":

    report_files = get_all_chain_reports()
    report_files = sorted(report_files, key=os.path.basename)

    groups = []
    uniquekeys = []

    for k, g in itertools.groupby(report_files, os.path.basename):
        groups.append(list(g))      # Store group iterator as a list
        uniquekeys.append('_'.join(k.split('_')[0:4]))

    grouped = list(zip(uniquekeys,groups))

    # Get any keys that aren't found
    network_sizes = list([8])
    TIP_LENGTH = list(np.arange(0.001, 0.015, 0.001))
    INTERNAL_LENGTH = list(np.arange(0.001, 0.015, 0.001))

    sims = 1
    number_of_sims = [[i]*sims for i in network_sizes]
    flatten = [j for i in number_of_sims for j in i]

    INDEX = []
    for i in number_of_sims:
        for pos, item in enumerate(i):
            INDEX.append(str(pos))

    PAIRS = list(zip(flatten,INDEX))
    temp = [str(p[0])+'_'+p[1] for p in PAIRS]

    items = itertools.product(temp, INTERNAL_LENGTH, TIP_LENGTH)
    items = list(filter(lambda x: x[1] + x[2], items))
    temp = ['{}_{:.3f}_{:.3f}'.format(*x) for x in items]

    reports = {}

    for k,g in grouped:
        reports[k] = consolidate_replicates(g)

    for t in temp:
        if t not in reports.keys():
            reports[t] = report_template()

    with open('all-report.json', 'w') as jsonfile:
        json.dump(reports, jsonfile)

