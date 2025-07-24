import os

# Логин и пароль для доступа в Active Directory
AD_LOGIN = ''
AD_PASSWORD = ''

# Соотношение файлов для 1с с Группами Active Directory
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

# Название полей пользователя в Active Directory
CSV_HEADERS = [
    'objectSid', 'dn',
    'name', 'sn', 'sAMAccountName', 'displayName', 'givenName',
    'mail',
    'description', 'info', 'description', 'department',
    'phone', 'homePhone', 'pager', 'mobile', 'telephoneNumber', 'ipPhone', 'otherTelephone'
]

# Файл Логов
LOG_FILE = 'log.txt'

# Расположение папки для выгрузки файлов CSV
DIR_OUT = './out'

os.makedirs(DIR_OUT, exist_ok=True)
