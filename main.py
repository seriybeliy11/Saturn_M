import os
import sys
import time
import webbrowser
import platform
from SaturiC import *
from flask import Flask

app = Flask(__name__)


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


@app.route('/bpdn')
def app1():
    run_command('barplots_perm_duration_and_unique_commenters.py')
    return 'Barplots Perm Duration and Unique Commenters executed.'


@app.route('/moneyQ')
def app3():
    run_command('moneq.py')
    return 'MoneyQ executed.'


@app.route('/closedplanned')
def app4():
    run_command('closed_not_planned.py')
    return 'Closed Not Planned executed.'


@app.route('/DTS')
def app5():
    run_command('dts.py')
    return 'DTS executed.'


def main():
    install_requirements('requirements.txt')

    run_command('csv_g.py')
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

    app.run()


if __name__ == "__main__":
    main()
