import base64
import re

from config import DEBUG
from log_ import log


def get_domain_from_group(input_str: str, count=3) -> str:
    input_str = input_str.split(',')
    name_list = []
    for w in input_str:
        s = re.sub(r'\w+\=', '', w)
        s = re.sub(r'\s+', '', s)
        name_list.append(s)
    if len(name_list) >= count > 0:
        name_list = name_list[len(name_list) - count:]
    out_str = '.'.join(name_list)
    return out_str


def parser_users(ldap_output) -> []:
    ldap_output = f'{ldap_output}'
    ldap_output = re.sub('\n ', '', ldap_output)
    ldap_output = re.sub(':{2} ', ': ', ldap_output)
    users_data = []
    current_user = {}
    for line in ldap_output.splitlines():
        if line.startswith('dn:'):
            if current_user:  # Если уже есть данные по предыдущему пользователю, сохраняем
                users_data.append(current_user)
            current_user = {'dn': line[3:].strip()}  # Начинаем нового пользователя

        elif ':' in line and not line.startswith(' '):  # Проверяем, что это строка атрибута, а не продолжение
            try:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                current_user[key] = value
            except ValueError:
                pass
        elif line.strip() == '':  # Пустая строка разделяет записи
            if current_user and 'dn' in current_user.keys():  # Убедимся, что это конец записи
                users_data.append(current_user)
            current_user = {}
    for user in users_data:
        for k, v in user.items():
            text_data = v
            dn_match = re.search(r'\s*([a-zA-Z0-9+/=\s]+)', text_data)
            if dn_match:
                encoded_dn = re.sub(r'[\s\n\t]', '', dn_match.group(1))
                try:
                    user[k] = base64.b64decode(encoded_dn).decode('utf-8')
                except UnicodeDecodeError as e:
                    pass
    if DEBUG:
        log.debug(users_data)
    return users_data


def parser_members(ldap_output) -> []:
    ldap_output = f'{ldap_output}'
    ldap_output = re.sub('\n ', '', ldap_output)
    ldap_output = re.sub(':{2} ', ': ', ldap_output)

    users_data = []
    for line in ldap_output.splitlines():
        if line.startswith('member: '):
            s = re.sub('member: ', '', line)
            users_data.append(s)
    members = []
    for text_data in users_data:
        dn_match = re.search(r'\s*([a-zA-Z0-9+/=\s]+)', text_data)
        if dn_match:
            encoded_dn = re.sub(r'[\s\n\t]', '', dn_match.group(1))
            try:
                members.append(base64.b64decode(encoded_dn).decode('utf-8'))
            except UnicodeDecodeError as e:
                members.append(text_data)
    if DEBUG:
        log.debug(members)
    return members
