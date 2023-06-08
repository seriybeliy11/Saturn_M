import os
import sys
import time
import webbrowser
import platform
from SaturiC import *


def install_requirements(requirements_file):
    os.system(f"{sys.executable} -m pip install -r {requirements_file}")


def run_command(command):
    if platform.system() == 'Windows':
        os.system(command)
    elif platform.system() == 'Darwin':  # Для macOS
        os.system(f"python3 {command}")
    else:
        print("Unsupported operating system.")
        sys.exit(1)


def main():
    install_requirements('requirements.txt')

    run_command('csv_g.py')

    time.sleep(7)
    print('--------------------------------------------')
    print('Hello! You are using the SaturiC Analyze System')
    print('--------------------------------------------')

    get_contributors()
    print('About issues:')
    get_issues()
    get_pulls()
    average_time_issue()
    get_AVG()
    get_KPI_pulls()
    get_KPI_contribute()
    print('About timelines:')
    # get_time_ad()
    print('About commenters:')
    get_commenters()

    run_command('dts.py')
    run_command('app.py')

    url = 'http://127.0.0.1:8050/'
    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    main()
