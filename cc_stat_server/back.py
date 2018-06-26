import os
import time
import datetime

from fabric import Connection
# from fabric.context_managers import shell_env
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
report_sh = os.path.join(dir_path, "get_report.sh")
USER='moniteur'
HOME = str(Path.home())

class InfoCluster(object):
    def __init__(self, hpc=None, cc_group=None, ldap_url=None, refresh_rate=24):
        self.host = hpc
        self.cc_group = cc_group
        self.ldap_url = ldap_url
        self._stdout = None
        self.refresh_rate = refresh_rate * 3600  # hours to sec
        self.report_dir = '../report'
        self.last_report_date = None

    def update_report(self, force=False):

        # execute(runit, host=self.host, user=USER, key_filename="{}/.ssh/id_rsa".format(HOME))
        # output = Connection(self.host).run(open(report_sh).read())
        report_path = os.path.join(dir_path, self.report_dir, self.host)

        if not os.path.isfile(report_path) or time.time() - os.path.getmtime(report_path) > self.refresh_rate :
            c = Connection(self.host, user='poq')
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


        page = """
Server: {} on {}
{}
        """.format(self.host,
                   datetime.datetime.fromtimestamp(self.last_report_date)
                   .strftime('%Y-%m-%d %H:%M:%S'), self._stdout)
        return page

        # re.findall(r'^def-bourqueg_cpu *([0-9]*)', stdout, flags=re.MULTILINE


    @property
    def report(self):
        self.update_report()
        self._report  = self.parse_report()

        return self._report



config = [
    {"hpc": "cedar.computecanada.ca",
     "ldap_url": "ldap1.int.cedar.computecanada.ca",
     "cc_group": "rrg-bourqueg-ad_cpu"},
    {"hpc": "graham.computecanada.ca",
     "ldap_url": "gra-ldap-slave.computecanada.ca",
     "cc_group": "def-bourqueg_cpu"}]



def reports():

    for c in config:

        c['report'] = InfoCluster(ldap_url=c['ldap_url'],
                                  hpc=c["hpc"], cc_group=c["cc_group"]).report

    return "{}\n".format(100*'*').join((c['report'] for c in config))


if __name__ == '__main__':

    ldap = "gra-ldap-slave.computecanada.ca"
    hpc = "graham.computecanada.ca"
    cc_group = "def-bourqueg_cpu"
    gra = InfoCluster(ldap_url=ldap, hpc=hpc, cc_group=cc_group)

    print(gra.report)
    import pprint
    # pprint.pprint(reports())
    print(reports())
