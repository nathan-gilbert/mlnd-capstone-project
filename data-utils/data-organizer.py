import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Format DUC Data.')
    parser.add_argument('in_data_directory', metavar='in', type=str,
                        help='The raw data directory')
    parser.add_argument('out_data_directory', metavar='out', type=str,
                        help='The output data directory')
    parser.add_argument('--2003', dest='is2003', action='store_true',
                        help='Format DUC 2003 Task 1 Data', default=False)
    parser.add_argument('--2004', dest='is2004', action='store_true',
                        help='Format DUC 2004 Task 2 Data', default=False)

    args = parser.parse_args()
    print(args.in_data_directory)
    print(args.out_data_directory)
    print(args.is2003)
    print(args.is2004)
