import matplotlib.pyplot as plt
import sys
import numpy as np
import re


def extract_metrics_single_model(filename, iternum):
    train_set_error = []
    test_set_error  = []
    # print(filename)
    with open(filename, "r") as f:
        for line in f:
            info = line.rstrip()
            # print(info)
            metrics = re.findall(r"[-+]?\d*\.\d+|\d+", info)
            if len(metrics) < 6:
                continue
            metrics = [float(x) for x in metrics]
            if metrics[0] != iternum:
                continue
            train_set_error.append(metrics[3])
            test_set_error.append(metrics[2])

    # print(train_set_error)
    # print(test_set_error)
    return train_set_error, test_set_error


def plot_error_multi_model(metrics, metric_name, savefile):
    fig, ax = plt.subplots()
    learning_size   = [0.2, 0.4, 0.6, 0.8, 1.0]
    index   = np.arange(5)
    width   = 0.1
    # print(metrics)
    d_p = ax.bar(index, metrics[0], width)
    s_p = ax.bar(index + width, metrics[1], width)
    r_p = ax.bar(index + 2 * width, metrics[2], width)

    ax.set_title('{} with different training set size'.format(metric_name))
    ax.set_xticks(index + width / 2)
    ax.set_xticklabels(learning_size)

    ax.legend((d_p[0], s_p[0], r_p[0]), ('deterministic', 'simple', 'robust'))
    ax.yaxis.set_units("error rate")
    ax.autoscale_view()

    plt.savefig(savefile)

def extract_metrics_multi_model(dfile, sfile, rfile, datatype, iternum, savefolder):
    d_metrics = extract_metrics_single_model(dfile, iternum)
    s_metrics = extract_metrics_single_model(sfile, iternum)
    r_metrics = extract_metrics_single_model(rfile, iternum)

    train_metrics = [d_metrics[0], s_metrics[0], r_metrics[0]]
    test_metrics  = [d_metrics[1], s_metrics[1], r_metrics[1]]
    # print(train_metrics)
    # print(test_metrics)

    train_savefile = savefolder + "train_{}.png".format(datatype)
    plot_error_multi_model(train_metrics, "train error", train_savefile)

    test_savefile =  savefolder + "test_{}.png".format(datatype)
    plot_error_multi_model(test_metrics, "test error", test_savefile)


if __name__ == "__main__":
    args = sys.argv[1:]
    dfile = args[0]
    sfile = args[1]
    rfile = args[2]
    datatype = args[3]
    iternum  = int(args[4]) # Iteration number to record
    savefolder = args[5]

    # extract_metrics_single_model(rfile, 4000)
    extract_metrics_multi_model(dfile, sfile, rfile, datatype, iternum, savefolder)
