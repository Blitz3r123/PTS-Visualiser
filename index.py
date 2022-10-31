"""
? How to use:
? Run `python index.py [test_set_path]`.
"""
from pprint import pprint
from rich.console import Console
console = Console()

import pandas as pd

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

# ? Validate if all files contain only numerics.
for dir in sub_dirs:
    files = os.listdir( os.path.join(camp_path, dir) )
    files = [x for x in files if '.csv' in x]
    for file in files:
        df = pd.read_csv( os.path.join(camp_path, dir, file) )
        for col in df.columns:
            has_non_numeric = not pd.to_numeric(df[col], errors='coerce').notnull().all()
            if has_non_numeric:
                file_path = os.path.join(camp_path, dir, file)
                console.print("Non-numeric value found in [bold blue]" + file_path + " [/bold blue]for the  column: [bold blue]" + col + "[/bold blue]", style="bold red")
                df = df[pd.to_numeric(df[col], errors='coerce').notnull()]
                df.to_csv(file_path, header=df.columns, index=False, mode="w")

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