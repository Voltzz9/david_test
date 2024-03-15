# test_scheduler.py

import difflib
import logging
import os
import subprocess
import sys
import argparse

def read_log_file(filename):
    """
    Reads the contents of a log file and returns them as a list of lines.
    """
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def make() -> bool:
        """
        Makes the test.

        Returns:
            bool: True if compilation was successful, False otherwise
        """
        # get current working dir
        wd_dir = os.getcwd()
        # go back up out of davidtest dir
        wd_dir = os.path.dirname(wd_dir)

        clean_proc = subprocess.Popen(
            ['make', 'clean'],
            cwd=wd_dir,
            stdout=subprocess.DEVNULL
        )
        clean_proc.wait()

        comp_proc = subprocess.Popen(
            ['make'],
            cwd=wd_dir,
            stdout=subprocess.DEVNULL
        )
        comp_proc.wait()

        if comp_proc.returncode == 0:
            print('Compiled successfully!')
            return True

        print('Failed to compile with error code {comp_proc.returncode}')
        return False

def compare_logs(actual_log, expected_log, test_num):
    """
    Compares the actual log with the expected log and highlights differences.
    """
    d = difflib.Differ()
    diff = list(d.compare(actual_log, expected_log))
    diff_str = ''
    line_num = 1
    for line in diff:
        if line.startswith('- ') or line.startswith('+ '):
            diff_str += f'{line_num}: {line}\n'
        line_num += 1


    if not any(line.startswith('- ') or line.startswith('+ ') for line in diff):
        # Files are the same
        print("\033[92mTest ",test_num,"passed!\033[0m")
    else:
        # Files differ
        print("\033[91mTest ",test_num,"failed! See differences:\033[0m")
        print(diff_str)

# list of commands to run
COMMANDS_DEADLOCK = [
    'data/process1.list data/process2.list 0 2',
    'data/david1.list data/david2.list 0 2',
    'data/david3.list data/david4.list 0 2',
    'data/david5.list data/david6.list 0 2',
    'data/process1.list data/process2.list 2 2',
    'data/david1.list data/david2.list 2 2',
    'data/david3.list data/david4.list 2 2',
    'data/david5.list data/david6.list 2 2'
]
COMMANDS_NORMAL = [
    'data/test1.list data/test2.list 0 2',
    'data/test3.list data/test4.list 0 2',
    'data/test5.list data/test6.list 0 2',
    'data/test7.list data/test8.list 0 2'
]

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Test script for scheduler')

    # Add the command line argument
    parser.add_argument('mode', choices=['deadlock', 'deadlock_resolution', 'normal'], help='Specify the mode: "deadlock", "deadlock_resolution" or "normal"')

    # Parse the command line arguments
    args = parser.parse_args()

    # Specify the filenames for the actual and expected log files
    actual_log_filename = 'scheduler.log'

    if (not make()):
        print("Error: Compilation failed.")
        sys.exit(1)

    # Run the test
    # the name of the exec command is ./schedule_processes data/david1.list data/david2.list 0 2
    # Deadlock
    if args.mode == 'deadlock_resolution':
        for i in range(len(COMMANDS_DEADLOCK)):
            # empty the log file
            open(actual_log_filename, 'w').close()
            
            expected_log_filename = 'davidlogs/deadlock_resolution' + str(i+1) + '.log'
            
            # get current working dir
            wd_dir = os.getcwd()
            # go back up out of davidtest dir
            wd_dir = os.path.dirname(wd_dir)

            exec_command = [wd_dir+'/schedule_processes'] + list(COMMANDS_DEADLOCK)[i].split(' ')
            #print run command
            print("Running command: ", exec_command)
            exec_proc = subprocess.Popen(exec_command, stdout=subprocess.PIPE)
            try:
                exec_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("\033Your program timed out after 5 seconds! Exitting.\033[0m")
                sys.exit(1)


            # Read the log files
            actual_log = read_log_file(actual_log_filename)
            expected_log = read_log_file(expected_log_filename)

            # Compare the logs and highlight differences
            compare_logs(actual_log, expected_log, i+1)
    # Normal
    elif args.mode == 'deadlock':
        for i in range(len(COMMANDS_DEADLOCK)):
            # empty the log file
            open(actual_log_filename, 'w').close()
            
            expected_log_filename = 'davidlogs/deadlock' + str(i+1) + '.log'
            
            # get current working dir
            wd_dir = os.getcwd()
            # go back up out of davidtest dir
            wd_dir = os.path.dirname(wd_dir)

            exec_command = [wd_dir+'/schedule_processes'] + list(COMMANDS_DEADLOCK)[i].split(' ')
            #print run command
            print("Running command: ", exec_command)
            exec_proc = subprocess.Popen(exec_command, stdout=subprocess.PIPE)
            try:
                exec_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("\033Your program timed out after 5 seconds! Exitting.\033[0m")
                sys.exit(1)

            # Read the log files
            actual_log = read_log_file(actual_log_filename)
            expected_log = read_log_file(expected_log_filename)

            # Compare the logs and highlight differences
            compare_logs(actual_log, expected_log, i+1)
    else:
        for i in range(len(COMMANDS_NORMAL)):
            # empty the log file
            open(actual_log_filename, 'w').close()
            
            expected_log_filename = 'davidlogs/normal' + str(i+1) + '.log'
            
            # get current working dir
            wd_dir = os.getcwd()
            # go back up out of davidtest dir
            wd_dir = os.path.dirname(wd_dir)

            exec_command = [wd_dir+'/schedule_processes'] + list(COMMANDS_NORMAL)[i].split(' ')
            #print run command
            print("Running command: ", exec_command)
            exec_proc = subprocess.Popen(exec_command, stdout=subprocess.PIPE)
            try:
                exec_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("\033Your program timed out after 5 seconds! Exitting.\033[0m")
                sys.exit(1)

            # Read the log files
            actual_log = read_log_file(actual_log_filename)
            expected_log = read_log_file(expected_log_filename)

            # Compare the logs and highlight differences
            compare_logs(actual_log, expected_log, i+1)

if __name__ == "__main__":
    main()
