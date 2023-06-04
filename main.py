import subprocess
subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

from SaturiC import *
import webbrowser


def main():
    subprocess.run(['python', 'csv_g.py'])
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    while True:
        time.sleep(7)
        print('----------_--- -- - -- - -- -      - - - - - -- ---- -- -- -  -')
        print('- - -  --   ---    ---      --  -- - ------- ---- ---  --- ----')
        print('Hello! You are using the SaturiC Analyze System')
        print('----------------------------------------------------------------')
        print('- - -  --   ---    ---      --  -- - ------- ---- ---  --- -----')
        print('----------------------------------------------------------------')
        print('- - -  --   ---    ---      --  -- - ------- ---- ---  --- -----')
        get_contributors()
        print('About issues:')
        get_issues()
        get_pulls()
        average_time_issue()
        get_AVG()
        get_KPI_pulls()
        get_KPI_contribute()
        print('About timelines:')
        #get_time_ad()
        print('About commenters:')
        get_commenters()
        break

    subprocess.call(['python', 'app.py'])
    url = 'http://127.0.0.1:8050/'
    webbrowser.open_new_tab(url)

if __name__ == "__main__":
    main()
