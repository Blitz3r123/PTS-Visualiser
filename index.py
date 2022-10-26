"""
? How to use:
? Run `python index.py [test_set_path]`.
"""
from rich.console import Console
console = Console()

import sys
import os
args = sys.argv[1:]

# Check that only one argument has been passed.
if len(args) > 1:
    console.print("You have more than 1 command line argument.", style="bold red")
    sys.exit()
else:
    camp_path = args[0]

# Check path is legit and is a folder
if not (os.path.exists(camp_path)):
    console.print("The path does not exist: \n\t" + camp_path, style="bold red")
if not (os.path.isdir(camp_path)):
    console.print("The path is not a directory: \n\t" + camp_path, style="bold red")
    
# Get all folders inside
sub_dirs = [x for x in os.listdir(camp_path) if os.path.isdir( os.path.join(camp_path, x) )]

# Check if the clean files already exist
required_files = [
    "latencies.csv",
    "throughputs.csv",
    "total_samples.csv",
    "sample_rates.csv",
    "lost_samples.csv"
]
for dir in sub_dirs:
    files = os.listdir( os.path.join(camp_path, dir) )
    missing_files = list(set(required_files) - set(files))
    
    if len(missing_files) > 0:
        console.print("Some clean files are missing from " + dir, style="bold red")
        os.system("python clean_test.py " + os.path.join(camp_path, dir) + " 1 1")

# ? Files should have been summarised at this point.

# Check if visualisations already exist
required_files = [
    "latencies_cdf.png",
    "latencies_line_graph.png",
    "lost_samples_cdf.png",
    "lost_samples_line_graph.png",
    "sample_rates_cdf.png",
    "sample_rates_line_graph.png",
    "throughputs_cdf.png",
    "throughputs_line_graph.png",
    "total_samples_cdf.png",
    "total_samples_line_graph.png"
]
for dir in sub_dirs:
    files = [x for x in os.listdir( os.path.join(camp_path, dir) ) if ".png" in x]
    missing_files = list(set(required_files) - set(files))
    
    if len(missing_files) > 0:
        console.print("Some graphs are missing from " + dir, style="bold red")
        os.system("python visualise_test.py " + os.path.join(camp_path, dir) + " 1 1")