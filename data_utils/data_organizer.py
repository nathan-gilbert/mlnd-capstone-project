import argparse
import os
import shutil


def do_2003_summaries():
    pass


def do_2003(in_dir, out_dir):
    """
    Grab all 60 documents, create a dir for each, along with their 4 human summaries
    :return:
    """

    # check that out dir exists
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    dir_items = os.listdir(in_dir)
    dir_items = list(filter(lambda x: os.path.isdir(in_dir + os.path.sep + x), dir_items))
    dir_items.sort()
    for idx, item in enumerate(dir_items):
        full_path = in_dir + os.path.sep + item
        print(f"{item} -> {idx}")
        full_out_path = out_dir + os.path.sep + str(idx)
        if not os.path.isdir(full_out_path):
            os.mkdir(full_out_path)

        with open(full_out_path + os.path.sep + "original_dir_name.txt", 'w') as orig_dir_name:
            print("Writing orig_dir_name file...")
            orig_dir_name.write(item)

        folder_items = os.listdir(full_path)
        folder_items = list(
            filter(lambda x: not os.path.isdir(in_dir + os.path.sep + x), folder_items))
        folder_items.sort()
        for jdx, f_item in enumerate(folder_items):
            print(f"{f_item} -> {jdx}.sgml")
            full_file_out_path = full_out_path + os.path.sep + str(jdx)
            if not os.path.isdir(full_file_out_path):
                os.mkdir(full_file_out_path)
            with open(full_file_out_path + os.path.sep + "original_file_name.txt",
                      'w') as orig_dir_name:
                print("Writing origFileName file...")
                orig_dir_name.write(f_item)
            final_file_name = full_file_out_path + os.path.sep + str(jdx) + ".sgml"
            shutil.copy2(in_dir + os.path.sep + item + os.path.sep + f_item, final_file_name)


def do_2004():
    """

    :return:
    """


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
    # print(args.in_data_directory)
    # print(args.out_data_directory)

    if args.is2003:
        do_2003(args.in_data_directory, args.out_data_directory)
    elif args.is2004:
        do_2004()
