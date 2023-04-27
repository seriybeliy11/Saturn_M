from SaturiC import *

def main():
    while True:
        print('----------_--- -- - -- - -- -      - - - - - -- ---- -- -- -  -')
        print('- - -  --   ---    ---      --  -- - ------- ---- ---  --- ----')
        print('Hello! You are using the SaturiC Analyze System')
        print('1 - Show info contributors')
        print('2 - Show info issues')
        print('3 - Show info pulls')
        print('4 - Show average_time for issues')
        print('5 - Visual for contribution statistics')
        print('6 - Visual for issues statistics')
        print('7 - Visual for pulls statistics')
        print('8 - Visual relation issues/pulls')
        print('9 - Visual bar charts for contribution')
        print('10 - Visual with Heatmap for contribution')
        print('11 - Visual with Bubbles for contribution')
        print('12 - Trends Line')
        print('13 - Get AVG parameter')
        print('14 - Get KPI parameter (pulls)')
        print('15 - Get KPI parameter (contribute)')
        print('16 - Export CSV about contributors')
        print('17 - Export CSV about pulls')
        print('18 - Export CSV about issues')
        print('Choose an option (or q to quit):')
        print('----------------------------------------------------------------')
        print('- - -  --   ---    ---      --  -- - ------- ---- ---  --- -----')

        choice = input()

        if choice == '1':
            get_contributors()

        elif choice == '2':
            get_issues()

        elif choice == '3':
            get_pulls()

        elif choice == '4':
            average_time_issue()

        elif choice == '5':
            plot_contributors()

        elif choice == '6':
            plot_issues()

        elif choice == '7':
            plot_pulls()

        elif choice == '8':
            plot_pulls()

        elif choice == '9':
            viz_contributors()

        elif choice == '10':
            contributors_heatmap()

        elif choice == '11':
            contributors_bubbles()

        elif choice == '12':
            get_AVG()

        elif choice == '13':
            get_KPI_pulls()

        elif choice == '14':
            get_KPI_contribute()

        elif choice == '15':
            export_CSV_contribute()

        elif choice == '16':
            export_CSV_pulls()

        elif choice == '17':
            export_CSV_pulls()

        elif choice == '18':
            export_CSV_issues()

        elif choice == 'q':
            print('Exiting program.')
            break
        else:
            print('Invalid input. Please try again.')

if __name__ == "__main__":
    main()
