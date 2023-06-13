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
    elif platform.system() == 'Darwin':  # macOS
        os.system(f"python3 {command}")
    else:
        print("Unsupported operating system.")
        sys.exit(1)


def main():
    install_requirements('requirements.txt')

    run_command('csv_g.py')
    run_command('parser_rewards.py')
    print('Cooling Space Engines...')
    time.sleep(14)
    run_command('just_closed_getter.py')
    time.sleep(6)
    run_command('approved_closed_getter.py')
    time.sleep(7)
    run_command('all_issues_getter.py')
    time.sleep(8)
    run_command('approved_timelines.py')
    time.sleep(9)
    run_command('q_comment_getter.py')


    time.sleep(2)
    print('--------------------------------------------')
    print('Hello! You are using the SaturiC Analyze System')
    print('--------------------------------------------')

    get_contributors()
    time.sleep(4)
    print('About issues:')
    get_issues()
    time.sleep(4)
    get_pulls()
    time.sleep(4)
    average_time_issue()
    time.sleep(4)
    get_AVG()
    time.sleep(4)
    get_KPI_pulls()
    time.sleep(4)
    get_KPI_contribute()
    print('About timelines:')
    # get_time_ad()
    print('About commenters:')
    time.sleep(4)
    get_commenters()

    run_command('graphs.py')



if __name__ == "__main__":
    main()
