import os
import glob
import config
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def make_group_plot(args):
  """Make a group plot from the similar results in the output/ directory."""
  directory = args.directory
  prefix = args.prefix
  buckets = args.buckets 

  # Collect all the results and create placeholder for results.
  all_files = glob.glob(directory + "/" + prefix + "*.csv")
  df = pd.concat((pd.read_csv(f) for f in all_files), axis=1)
  df.columns = all_files
  results_raw = df.as_matrix()
  num_bins = int(np.ceil(results_raw.shape[0]/buckets))
  results_binned = np.zeros((results_raw.shape[1], num_bins))

  # Bin the results.
  for run in range(results_raw.shape[1]):
      for bin_idx in range(num_bins):
          results_binned[run, bin_idx] = (np.mean(results_raw[
            int(bin_idx*buckets):int(bin_idx*buckets+buckets), run]))

  # Build the plot.
  fig, ax = plt.subplots(figsize=(args.figSizeX, args.figSizeY))
  sns.tsplot(data = results_binned, ax=ax, ci=[68, 95], color="m")

  # Save the plot.
  ax.set_title(prefix + ' -- Average Binned Return', fontsize=18)
  ax.set_xlabel('Bin', fontsize=18)
  ax.set_ylabel('Average Return', fontsize=18)
  plt.tick_params(axis='both', which='major', labelsize=18)
  ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
  plt.savefig(os.path.join(directory, prefix+'_groupfig.png'), 
    bbox_inches='tight')
  
  # Return binned results for group figure.
  return results_binned

def make_comparison_plot(args, res, keys, min_length):
  """Make a comparison plot to compare two groups."""
  directory = args.directory

  # Build the plot.
  fig, ax = plt.subplots(figsize=(args.figSizeX, args.figSizeY))

  # Stack the results groups, thus, each must be the same shape.
  sns.tsplot(data = np.stack(res, axis=2), condition=keys, ax=ax, ci=[68, 95])
  
  # Save the plot.
  ax.set_title('Average Return by Group, N=' + str(min_length), fontsize=18)
  ax.set_xlabel('Bin', fontsize=18)
  ax.set_ylabel('Average Return', fontsize=18)
  ax.legend(fontsize=18)
  plt.tick_params(axis='both', which='major', labelsize=18)
  ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
  plt.savefig(os.path.join(directory, 'group_comparison.png'), 
    bbox_inches='tight')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=('Plot group of'
                                                'experimental runs.'))
  parser.add_argument('-d', '--directory', default='output')
  parser.add_argument('-p', '--prefix', default='sarsa_nep_434')
  parser.add_argument('-x', '--figSizeX', default=12)
  parser.add_argument('-y', '--figSizeY', default=5)
  parser.add_argument('-b', '--buckets', default=config.REPORT_EVERY_N, 
      help="Average data into N buckets, use 0 for no averaging")
  args = parser.parse_args()
  mp(args)