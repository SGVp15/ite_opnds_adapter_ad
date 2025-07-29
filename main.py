import os.path
import subprocess

from config import AD_LOGIN, AD_PASSWORD, GROUPS, CSV_HEADERS, DIR_OUT, DEBUG, DOMAINS
from csv_ import save_users_csv
from log_ import log
from parser import get_domain_from_group, parser_users


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
            log.debug('[ STDOUT ldapsearch ]\n', ldap_output)

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


def get_users_from_ad(domain: str, dc: str) -> str:
    command_get_user = [
        'ldapsearch',
        '-x',
        '-H', f'ldap://{domain}',
        '-D', f'{AD_LOGIN}',
        '-w', f'{AD_PASSWORD}',
        '-b', f'{get_domain_from_group(dc)}',
        f'(&(objectClass=user)(memberOf={dc}))',
        *CSV_HEADERS
    ]
    return run_ldapsearch(command=command_get_user)


def main():
    all_users = []
    for file_name, group_ad in GROUPS.items():
        log.info(f'Обработка группы: [{file_name}]')
        group_users = []
        users = []
        for domain in DOMAINS:
            r = get_users_from_ad(domain=domain, dc=group_ad)
            if DEBUG:
                log.debug(f'[ get_users_from_ad ]\n{r}')
            try:
                users = parser_users(r)
            except TypeError as e:
                pass
            group_users.extend(users)

        for user in group_users:
            user['role'] = f'{file_name}'
        if DEBUG:
            log.debug(f'[ USER ]{user}')
        all_users.extend(group_users)
        save_users_csv(users_data=all_users, csv_filename=str(os.path.join(DIR_OUT, file_name)))
        log.info(f'Обработка группы завершена: [{file_name}]. Обработано {len(users)} записей')
    save_users_csv(all_users, csv_filename='all_users.csv')


if __name__ == '__main__':
    main()
