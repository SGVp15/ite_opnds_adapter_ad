import csv
import os.path
import subprocess

from config import AD_LOGIN, AD_PASSWORD, GROUPS, CSV_HEADERS, DIR_OUT, DELIMITER_CSV
from log_ import log
from parser import get_domain_from_group, parser_users


def get_members_in_group(group) -> str:
    command_get_members_sid = [
        'ldapsearch',
        '-x',
        '-H', f'ldap://{get_domain_from_group(group)}',
        '-D', f'{AD_LOGIN}',
        '-w', f'{AD_PASSWORD}',
        # ЭТО МОЖЕТ БЫТЬ ОШИБКОЙ !!!
        '-b', f'{group}',
        f'(memberOf=CN={group})',
        'members',
    ]
    try:
        # Запускаем команду и захватываем её вывод
        # capture_output=True - захватывает stdout и stderr
        # text=True - декодирует stdout и stderr как текст (UTF-8 по умолчанию)
        # check=True - вызывает CalledProcessError, если команда возвращает ненулевой код выхода
        # result = subprocess.run(command, capture_output=True, text=True, check=True)
        result = subprocess.run(command_get_members_sid, text=True, capture_output=False)

        # Выводим стандартный вывод команды
        ldap_output = result.stdout

        # log.info('STDOUT ldapsearch:')
        # log.info(ldap_output)

        return ldap_output
        # Если есть ошибки, они будут в result.stderr (если check=False)
        # log.error('STDERR ldapsearch:')
        # log.error(result.stderr)

    except subprocess.CalledProcessError as e:
        log.error(f'Ошибка выполнения ldapsearch: {e}')
        log.error(f'Код выхода: {result.returncode}')
        log.error(f'STDOUT: {result.stdout}')
        log.error(f'STDERR: {result.stderr}')
    except FileNotFoundError:
        log.error('Ошибка: Команда ldapsearch не найдена.')
    except Exception as e:
        log.error(f'Произошла непредвиденная ошибка: {e}')
        return ''


def save_users_csv(users_data: list[dict], csv_filename: str = 'ldap_users.csv'):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS, delimiter=DELIMITER_CSV)
        writer.writeheader()
        for user in users_data:
            row = {header: user.get(header, '') for header in CSV_HEADERS}
            writer.writerow(row)


def get_users_from_ad(dc: str) -> str:
    command_get_members_sid = [
        'ldapsearch',
        '-x',
        '-H', f'ldap://{get_domain_from_group(dc)}',
        '-D', f'{AD_LOGIN}',
        '-w', f'{AD_PASSWORD}',
        '-b', dc,
        # f'(&(objectClass=user)(memberOf=CN={group},OU=Confluence,{domain}))',
        *CSV_HEADERS
    ]
    try:
        # Запускаем команду и захватываем её вывод
        # capture_output=True - захватывает stdout и stderr
        # text=True - декодирует stdout и stderr как текст (UTF-8 по умолчанию)
        # check=True - вызывает CalledProcessError, если команда возвращает ненулевой код выхода
        # result = subprocess.run(command, capture_output=True, text=True, check=True)
        result = subprocess.run(command_get_members_sid, text=True, capture_output=False)

        # Выводим стандартный вывод команды
        ldap_output = result.stdout

        # log.info('STDOUT ldapsearch:')
        # log.info(ldap_output)

        return ldap_output
        # Если есть ошибки, они будут в result.stderr (если check=False)
        # log.error('STDERR ldapsearch:')
        # log.error(result.stderr)

    except subprocess.CalledProcessError as e:
        log.error(f'Ошибка выполнения ldapsearch: {e}')
        log.error(f'Код выхода: {result.returncode}')
        log.error(f'STDOUT: {result.stdout}')
        log.error(f'STDERR: {result.stderr}')
    except FileNotFoundError:
        log.error('Ошибка: Команда ldapsearch не найдена.')
    except Exception as e:
        log.error(f'Произошла непредвиденная ошибка: {e}')


def main():
    for file_name, group_ad in GROUPS.items():
        log.info(f'Обработка группы: [{file_name}]')
        members_users_ad_group = parser_users(get_members_in_group(group_ad))
        users = []
        for member_user_ad in members_users_ad_group:
            users.append(parser_users(get_users_from_ad(member_user_ad)))
        save_users_csv(users_data=users, csv_filename=str(os.path.join(DIR_OUT, file_name)))
        log.info(f'Обработка группы завершена: [{file_name}]. '
                 f'Обработано {len(users)} записей')


if __name__ == '__main__':
    main()
