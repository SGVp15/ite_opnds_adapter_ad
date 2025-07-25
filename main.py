import os.path
import subprocess

from config import AD_LOGIN, AD_PASSWORD, GROUPS, CSV_HEADERS, DIR_OUT, DEBUG
from csv_ import save_users_csv, save_users_all_to_one_csv
from log_ import log
from parser import get_domain_from_group, parser_users, parser_members


# def get_members_in_group(group) -> str:
#     command_get_members = [
#         'ldapsearch',
#         '-x',
#         '-H', f'ldap://{get_domain_from_group(group)}',
#         '-D', f'{AD_LOGIN}',
#         '-w', f'{AD_PASSWORD}',
#         '-b', group,
#         # f'(memberOf={group})',
#         'member', 'dc',
#     ]
#     return run_ldapsearch(command=command_get_members)


def run_ldapsearch(command):
    try:
        # Запускаем команду и захватываем её вывод
        # capture_output=True - захватывает stdout и stderr
        # text=True - декодирует stdout и stderr как текст (UTF-8 по умолчанию)
        # check=True - вызывает CalledProcessError, если команда возвращает ненулевой код выхода
        # result = subprocess.run(command, capture_output=True, text=True, check=True)
        result = subprocess.run(command, text=True, capture_output=True, encoding='utf-8')

        ldap_output = result.stdout

        if DEBUG:
            log.debug('STDOUT ldapsearch:\n', ldap_output)

        return ldap_output

    except subprocess.CalledProcessError as e:
        log.error(f'Ошибка выполнения ldapsearch: {e}')
        log.error(f'Код выхода: {result.returncode}')
        log.error(f'STDOUT: {result.stdout}')
        log.error(f'STDERR: {result.stderr}')
    except FileNotFoundError:
        log.error('Ошибка: Команда ldapsearch не найдена.')
    except Exception as e:
        log.error(f'Произошла непредвиденная ошибка: {e}')


def get_users_from_ad(dc: str) -> str:
    command_get_user = [
        'ldapsearch',
        '-x',
        '-H', f'ldap://{get_domain_from_group(dc)}',
        '-D', f'{AD_LOGIN}',
        '-w', f'{AD_PASSWORD}',
        '-b', {get_domain_from_group(dc, 2)},
        f'(&(objectClass=user)(memberOf={dc}))',
        *CSV_HEADERS
    ]
    return run_ldapsearch(command=command_get_user)


def main():
    all_users = []
    for file_name, group_ad in GROUPS.items():
        log.info(f'Обработка группы: [{file_name}]')
        # members_users_ad_group = parser_members(get_members_in_group(group_ad))

        # users = []
        # for member_user_ad in members_users_ad_group:
        # r = get_users_from_ad(member_user_ad)
        users = get_users_from_ad(group_ad)
        # try:
        #     users.append(*parser_users(r))
        # except TypeError as e:
        #     pass

        for u in users:
            u['role'] = f'{file_name}'

        all_users.extend(users)

        save_users_csv(users_data=users, csv_filename=str(os.path.join(DIR_OUT, file_name)))
        log.info(f'Обработка группы завершена: [{file_name}]. Обработано {len(users)} записей')
    save_users_all_to_one_csv(all_users)


if __name__ == '__main__':
    main()
