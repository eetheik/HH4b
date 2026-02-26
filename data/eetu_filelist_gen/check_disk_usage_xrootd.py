#!/usr/bin/python3

import os
import subprocess
import argparse
from collections import defaultdict
import json

def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to directory. If starts with root:, will assume <xrootd redirector>:<path to directory>. If path contains ~, will expand to /store/user/<username>")
    parser.add_argument("-S", "--site", type=str, default=os.environ.get("XROOTD_STORAGE_SITE", ""), help="xrootd redirector to the storage site. Try from this order: 1) given argument path if path starts with root:, 2) given argument site, and 3) environment variable XROOTD_STORAGE_SITE")
    parser.add_argument("-d", "--max-depth", type=int, default=0, help="maximum level of directories to recurse")
    parser.add_argument("-s", "--sort", action="store_true", help="sort directories by size")

    args = parser.parse_args()
    
    # if path starts with root:, obtain redirector
    if args.path.startswith("root:"):
        site, path = args.path[len("root:"):].split(":")
        args.site = "root:" + site
        args.path = path

    path = args.path.strip("/") # remove leading and trailing slashes
    args.path = "/" + path
     
    # expand ~
    if "~" in args.path:
        args.path = args.path.replace("~", os.path.join("store/user", os.getlogin()))

    if len(args.site) == 0:
        raise ValueError("No redirector is provided.")
    
    # query size from storage site
    command = f"xrdfs {args.site} ls -l -R {args.path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # loop through the results and fill the size of leaf directories (directories with depth = max_depth)
    directories_to_report = [args.path]
    depth_directories_dict = defaultdict(list)
    depth_directories_dict[0].append(args.path)
    directory_size_dict = defaultdict(int)
    for line in result.stdout.splitlines():
        tokens = line.split() # permission date time size path
        depth = tokens[-1].count("/", len(args.path))
        if tokens[0].startswith("d"): # directory
            if depth <= args.max_depth:
                directories_to_report.append(tokens[-1])
                depth_directories_dict[depth].append(tokens[-1])
        else: # file
            directory_depth = depth - 1 if depth <= args.max_depth else args.max_depth
            for directory in depth_directories_dict[directory_depth]:
                if tokens[-1].startswith(directory + "/"):
                  #  print(directory)
                    directory_size_dict[directory] += int(tokens[3])

    # aggregate sizes for lower depth directories
    for depth in sorted(depth_directories_dict.keys())[::-1][1:]:
        for directory in depth_directories_dict[depth]:
            for subdirectory in depth_directories_dict[depth + 1]:
                if subdirectory.startswith(directory):
                    directory_size_dict[directory] += directory_size_dict[subdirectory]

    # print the results
    if args.sort:
        for directory, size in sorted(map(lambda x: (x, directory_size_dict[x]), directories_to_report), key=lambda x: x[1]):
            print(f"{sizeof_fmt(size):<10} {directory}")
    else:
        for directory in directories_to_report[::-1]:
            print(f"{sizeof_fmt(directory_size_dict[directory]):<10} {directory}")
            