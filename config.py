import os

AD_LOGIN = ''
AD_PASSWORD = ''

GROUPS = {
    'administrator.csv': 'CN=SupportPortalUsers,OU=Support,DC=ITExpert,DC=ru,DC=local',
    'administrator_ib.csv': '',
    'kontroler_ekspluatacii.csv': '',
    'operator_obmena.csv': '',
    'menedzher_planirovaniya.csv': '',
    'rukovoditel_trenirovki.csv': '',
    'menedzher_scenariev_vosstanovleniya.csv': '',
    'uchastnik_trenirovki.csv': '',
    'koordinator_ons.csv': '',
    'auditor.csv': '',
}

CSV_HEADERS = [
    'objectSid', 'dn',
    'name', 'sn', 'sAMAccountName', 'displayName', 'givenName',
    'mail',
    'description', 'info', 'description', 'department',
    'phone', 'homePhone', 'pager', 'mobile', 'telephoneNumber', 'ipPhone', 'otherTelephone'
]

LOG_FILE = 'log.txt'
DIR_OUT = './out'

os.makedirs(DIR_OUT, exist_ok=True)
