from rich.console import Console

from visualise_test_functions import *

import os
import sys

console = Console()

args = sys.argv[1:]
# Check that only one argument has been passed.
if len(args) > 3:
    console.print("You have more than 3 command line argument.", style="bold red")
    sys.exit
else:
    test_path = args[0]
    curr_test = args[1]
    total_test_count = args[2]
    
# Check path exists
if not os.path.exists(test_path):
    console.print("Path doesn't exist: \n\t" + test_path, style="bold red")
    sys.exit()
    
console.print("[" +str(curr_test)+ "/" +str(total_test_count)+ "] Visualising " + os.path.basename(test_path), style="bold blue")

valid_csv_files = validate_test_cleaning(test_path)
valid_csv_files = [os.path.join(test_path, file) for file in valid_csv_files]

for file in valid_csv_files:
    visualise_file(file)