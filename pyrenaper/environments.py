from collections import namedtuple

Environment = namedtuple('Environment', ['base_url', 'domain'])

ONBOARDING = Environment(base_url="http://onboarding.renaper.prod.vusecurity.com:8080/vu-onboarding-rest/",
                         domain='https://renaperpreprod.dnm.gob.ar/')