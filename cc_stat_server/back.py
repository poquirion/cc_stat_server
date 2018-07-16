import copy
import datetime
import json
import os
import re
import time

from pathlib import Path

from fabric import Connection

dir_path = os.path.dirname(os.path.realpath(__file__))
report_sh = os.path.join(dir_path, "get_report.sh")
USER = 'poq'
HOME = str(Path.home())

class InfoCluster(object):
    def __init__(self, hpc=None, cc_group=None, ldap_url=None, refresh_rate=1):
        self.host = hpc
        self.cc_group = cc_group
        self.ldap_url = ldap_url
        self._stdout = None
        self.refresh_rate = refresh_rate * 3600  # hours to sec
        self.report_dir = '../report'

        try:
            os.makedirs(self.report_dir, exist_ok=True)
        except PermissionError:
            self.report_dir = '/tmp/report'
            os.makedirs(self.report_dir, exist_ok=True)

        self.last_report_date = None
        self._raw = None
        self._report = {}

    def update_report(self, force=False):

        report_path = os.path.join(dir_path, self.report_dir, self.host)

        if not os.path.isfile(report_path) or time.time() - os.path.getmtime(report_path) > self.refresh_rate :
            c = Connection(self.host, user=USER)
            env = {"LDAP_URL": self.ldap_url, "CCGROUP": self.cc_group}
            p = "&&".join(['{}={}'.format(k, v) for k, v in env.items()])
            with c.prefix(p):
                outputs = c.run(open(report_sh).read(),
                                replace_env=True)

                self._stdout = outputs.stdout
                with open(report_path, 'w') as fp:
                    fp.write(self._stdout)
        else:

            self._stdout = open(report_path).read()

        self.last_report_date = os.path.getmtime(report_path)



    def parse_report(self):


        raw = """
Server: {} on {}
{}
        """.format(self.host,
                   datetime.datetime.fromtimestamp(self.last_report_date)
                   .strftime('%Y-%m-%d %H:%M:%S'), self._stdout)
        # return raw
        iterline = iter(self._stdout.split('\n'))
        report_update = {}
        fair_share = {}
        for block in iterline:
            if "sshare go" in block:
                for line in iterline:
                    s_line = line.split('|')
                    s_line = [s.strip() for s in s_line]
                    if 'Account' == s_line[0]:
                        headers = s_line
                    elif "sshare stop" in line:
                        report_update["fair_share"] = fair_share
                        break
                    elif not s_line[1]:
                       fair_share[s_line[0]] = dict(zip(headers, s_line))
                       fair_share[s_line[0]]['User'] = []
                    else:
                        fair_share[s_line[0]]['User'].append(dict(zip(headers, s_line)))

            if "sdiag go" in block:
                for line in iterline:
                    if "sdiag stop" in line:
                        report_update["scheduler_load"] = scheduler_load
                        break
                    scheduler_load = int(line)
                    if scheduler_load >= 3000:
                        scheduler_load = " very heavy"
                    elif scheduler_load >= 1000:
                        scheduler_load = "heavy"
                    elif scheduler_load >= 500:
                        scheduler_load = "moderate"
                    else:
                        scheduler_load = 'light'

            if "partition-stats go" in block:
                total = None
                for line in iterline:
                    if "partition-stats stop" in line:
                        report_update["usage"] = total
                        break
                    if 'Totals:' in line:
                        total = dict(re.findall(r'(\w+ \w+): +([1-9]+)', line))


        return report_update

    @property
    def report(self):
        self.update_report()
        self._report.update(self.parse_report())

        return self._report



config = [
    {"hpc": "cedar.computecanada.ca",
     "ldap_url": "ldap1.int.cedar.computecanada.ca",
     "cc_group": "bourque"},
    {"hpc": "graham.computecanada.ca",
     "ldap_url": "gra-ldap-slave.computecanada.ca",
     "cc_group": "bourque"},
    {"hpc": "mp2.ccs.usherbrooke.ca",
     "ldap_url": "ldap-usherbrooke.computecanada.ca",
     "cc_group": "bourque"}]



def reports():

    conf = copy.copy(config)
    yield '['

    n_machines = len(conf)
    for i, c in enumerate(conf):

        c['report'] = InfoCluster(ldap_url=c['ldap_url'],
                                  hpc=c["hpc"], cc_group=c["cc_group"]).report
        comma = ', '
        if i + 1 == n_machines:
            comma = ''

        yield json.dumps(c) + comma

    # return "{}\n".format(100*'*').join((c['report'] for c in config))

    yield ']'


if __name__ == '__main__':

    # ldap = "gra-ldap-slave.computecanada.ca"
    # hpc = "graham.computecanada.ca"
    # cc_group = "def-bourqueg_cpu"

    # gra = InfoCluster(ldap_url=ldap, hpc=hpc, cc_group=cc_group)

    # print(gra.report)
    # pprint.pprint(reports())
    print(reports())
