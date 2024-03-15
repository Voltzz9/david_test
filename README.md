# david_test
### Current Version:  v2.2
simple lightweight testing script for cs314 proj1
![david test](https://github.com/Voltzz9/david_test/assets/91885586/2e8fe12e-da8e-43aa-9c74-ab15f626440a)


## Important:
- Current functionality: Tests the output log file of your scheduler against my implementation.
- it is **your responsibility** to ensure your `.gitignore` file accounts for my test cases
- There are **no guarantees that my test cases are correct**
- Currently runs **FCFS and Priority Scheduling only**

## Setup
1. Clone this repo into your **proj1** directory
2. Execute tests without deadlocks with `python3 david_test.py {mode}` where mode is `normal`, `deadlock_resolution`, or `deadlock`

#### Example
in the `proj1/david_test` dir
```sh
$ python3 david_test.py normal
```

## Mode Information
Option                 | Description
-----------------------| --------------------------------------------------------
_normal_               | Test cases with no deadlocks at all
_deadlock\_resolution_ | Test cases with a full deadlock resolution implemented
_deadlock_             | Test cases with **only** deadlock detection (no resolution) which quits when a deadlock is found

## Your implementation gives a different result?
If you have a solid argument for a different log file output feel free to open an issue on github. Make sure to include the differences and your argument as to why the output should be different.

## Changelog
### v2.2
- Fixed deadlock resolution test case bugs

### v2.1
- Added deadlock detection _without resolution_

### v2
- Added non-deadlock test cases