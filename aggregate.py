import matplotlib.pyplot as plt
import sys
import numpy as np
import re

def get_metrics(fstream, num_models):
    metrics = []
    for _ in range(num_models):
        data = fstream.readline().strip().split(" ")
        data = [float(x) for x in data]
        metrics.append(data)
    return metrics

def plot_compare(filename, num_models):
    f = open(filename, "r")
    lines  = [line for line in f]

    header = lines[0].strip().split()
    true_model_metrics = [float(x) for x in header]
    
    #print(true_model_metrics)
    splits = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]

    i = 1    
    aggregate_metrics = []
    while i < len(lines):
        metrics_by_split = []
        #deter_metric_str = lines[i].strip().split()
        #print(deter_metric_str)
        #deter_metric = [float(x) for x in deter_metric_str]
        #metrics_by_split.append(deter_metric)
        for k in range(num_models):
            other_metric_str = lines[i+k].strip().split()
            other_metric = [float(x) for x in other_metric_str]
            metrics_by_split.append(other_metric)
            
        i += num_models
        aggregate_metrics.append(metrics_by_split)
    
    aggregate_metrics = np.array(aggregate_metrics)
    print(aggregate_metrics.shape)
    return aggregate_metrics, true_model_metrics


def show_model_comparisons(filename, num_models):
    our_models, true_models = plot_compare(filename, num_models)
    splits = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
    num_split = np.size(our_models, axis=0)
    found_splits = splits[: num_split]

    fig, ax = plt.subplots()



if __name__ == "__main__":
    args = sys.argv[1:]
    file_name = args[0] # aggregate filename
    num_models = int(args[1]) # Number of models to compare

    plot_compare(file_name, num_models)

