#!/usr/local/bin/python

import dynclipy
task = dynclipy.main()
# task = dynclipy.main(
#   ["--dataset", "/code/example.h5", "--output", "/mnt/output"],
#   "/code/definition.yml"
# )

import PySCUBA
import json
import sys
import numpy as np
import os
import pandas as pd

import time
checkpoints = {}

#   ____________________________________________________________________________
#   Load data                                                               ####

expression = task["expression"]
p = task["params"]

if "timecourse_discrete" in task["priors"]:
  timecourse_discrete = task["priors"]["timecourse_discrete"]

# resave expression because SCUBA requires this (🙄)
expression.T.to_csv("/txpression.tsv", sep = "\t")

checkpoints["method_afterpreproc"] = time.time()

#   ____________________________________________________________________________
#   Infer trajectory                                                        ####
pseudotime_mode = timecourse_discrete is None
cell_IDs, data, markers, cell_stages, data_tag, output_directory = PySCUBA.Preprocessing.RNASeq_preprocess(
  "/expression.tsv",
  pseudotime_mode = pseudotime_mod,
  log_mode = False,
  N_dim = p["N_dim"],
  low_gene_threshold = p["low_gene_threshold"],
  low_gene_fraction_max = p["low_gene_fraction_max"]
)

if timecourse_discrete is not None:
  cell_stages = timecourse_discrete

centroid_coordinates, cluster_indices, parent_clusters = PySCUBA.initialize_tree(
  data,
  cell_stages,
  rigorous_gap_stats = p["rigorous_gap_stats"],
  min_split = p["min_split"],
  min_percentage_split = p["min_percentage_split"])

centroid_coordinates, cluster_indices, parent_clusters, new_tree = PySCUBA.refine_tree(
  data,
  centroid_coordinates,
  cluster_indices,
  parent_clusters,
  cell_stages,
  output_directory="/")

checkpoints["method_aftermethod"] = time.time()

#   ____________________________________________________________________________
#   Process & save output                                                   ####
#
 rouping = pd.DataFrame({
  "cell_id": expression.index,
  "group_id": cluster_indices.astype(str)
})

# milestone_network

tree_pd = pd.DataFrame(new_tree[1:,:], columns = new_tree[0,:])milestone_network = pd.DataFrame({
  "from": tree_pd["Parent cluster"].astype(np.double).astype(np.int).astype(str),
  "to": tree_pd["Cluster ID"].astype(np.double).astype(np.int).astype(str),
  "length": 1.0,
  "directed": True
})

# save
dataset = dynclipy.wrap_data(cell_ids = expression.index)
dataset.add_cluster_graph(
  grouping = grouping,
  milestone_network = milestone_network
)
dataset.add_timings(timings = checkpoints)
dataset.write_output(task["output"])
