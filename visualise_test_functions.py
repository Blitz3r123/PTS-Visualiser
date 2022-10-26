import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from rich.console import Console
console = Console()

import os

def validate_test_cleaning(test_path):
    required_files = [
        "latencies.csv",
        "throughputs.csv",
        "total_samples.csv",
        "sample_rates.csv",
        "lost_samples.csv"
    ]
    current_files = os.listdir(test_path)
    
    missing_files = (set(required_files) - set(current_files))
    
    if len(missing_files) > 0:
        console.print("The following files are missing from " + os.path.basename(test_path) + ":", style="bold red")
        for file in missing_files:
            console.print("\t- " + file, style="bold red")
            
    return list(set(required_files) - set(missing_files))

def visualise_file(file):
    metric_name = get_metric_name(file)
    metric_units = get_metric_units(metric_name)
    df = pd.read_csv(file)
    col_count = len(df.columns)

    plot_line_graph(file, metric_name, metric_units, df, col_count)
    plot_cdf(file, metric_name, df) 
    
def plot_cdf(file, metric_name, df):
    stats_df = df \
        .groupby(list(df)[0]) \
        [list(df)[0]] \
        .agg('count') \
        .pipe(pd.DataFrame) \
        .rename(columns = {list(df)[0]: 'frequency'})
    
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
    
    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.suptitle = metric_name + " " + os.path.dirname(file)
    ax.set_title(metric_name + " " + os.path.dirname(file).replace("\\", " "), fontweight="bold", fontsize=12)
    
        
    stats_df.plot(x = list(df)[0], y = ['pdf', 'cdf'], grid=True, ax=ax)
    
    ax.set_ylabel("F(x)")
    ax.set_xlabel(metric_name)
    
    plt.grid()
    
    filename = os.path.join(os.path.dirname(file), metric_name.replace(" ", "_") + "_cdf.png")
    filename.replace(" ", "_")
    
    fig.savefig(filename)
    
def plot_line_graph(file, metric_name, metric_units, df, col_count):    
    line_graph, ax = plt.subplots(figsize=(10, 10))
    line_graph.suptitle = metric_name + " " + os.path.dirname(file)
    
    ax.set_title(metric_name + " " + os.path.dirname(file).replace("\\", " "), fontweight="bold", fontsize=12)
    
    ax.set_ylabel(metric_name.title() + " (" + metric_units + ")")
    ax.set_xlabel(get_x_label(metric_name, "line_graph"))
    
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    
    for col in range(col_count):
        run_data = df.iloc[:, col]
        ax.plot(run_data)
        
    plt.grid()
    
    filename = os.path.join(os.path.dirname(file), metric_name.replace(" ", "_") + "_line_graph.png")
    filename.replace(" ", "_")
    
    line_graph.savefig(filename)
    
def get_x_label(name, graph_type):
    if "line_graph" in graph_type:
        if "latencies" not in name:
            return "Time (s)"
        else:
            return "Samples Over Increasing Time"
    
def get_metric_name(file):
    return os.path.basename(file).split(".")[0].replace("_", " ")

def get_metric_units(metric_name):
    if "latencies" in metric_name:
        return "us"
    elif "throughputs" in metric_name:
        return "mbps"
    elif "total samples" in metric_name:
        return "samples"
    elif "sample rates" in metric_name:
        return "samples/s"
    elif "lost samples" in metric_name:
        return "samples"
    else: 
        return None
