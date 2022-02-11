from .models import Environment

ONBOARDING = Environment(base_url="http://onboarding.renaper.prod.vusecurity.com:8080/vu-onboarding-rest/",
                         domain='https://renaperpreprod.dnm.gob.ar/')


SID = Environment(base_url='https://apirenaper.idear.gov.ar/', 
                  domain='https://apirenaper.idear.gov.ar/')