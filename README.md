Loggi BUD - Benchmark for Urban Deliveries
==================

# Overview

The Loggi Benchmark for Urban Deliveries contains datasets and benchmark scripts for large-scale problems in some of Brazil's largest cities. The data is from public sources that have a high correlation with actual last-mile deliveries performed by Loggi. Similar to several benchmarks, we publish a leaderboard of best-known solutions.


# Tasks

### Task 1.1 Capacitated Vehicle Routing Problem

| Submission | Date       | Submitted by             | Solution                            | Distance (km)       |
| ---------- | -----------| ------------------------ | ----------------------------------- | ------------------- |
| ortools1   | 2020/10/31 | Loggi - Network design   | OR-tools VRP \[[code](.)\]          | 10000.000           |
| kmortools1 | 2020/10/31 | Loggi - Network design   | KMeans + OR-tools VRP \[[code](.)\] | 10000.000           |


### Task 1.2 Capacitated Vehicle Routing Problem with Stochastic Customers


### Task 1.3 End-to-end last-mile problem 


# Motivation

This benchmark is an effort to make new operations research solutions closer to real-world applications. We believe this work can help both practitioners and academics to reduce the gap between state-of-the-art and practice.

We identify that several promising solutions in academic literature have evaluation or reproducibility issues. Several papers only include experiments for toy problems that do not resemble real applications. Another issue is that some authors do not publish any code related to the publications, which makes their work very hard to reproduce.


### Why a new dataset

There are several famous datasets for the Vehicle Routing Problem (VRP). However, there are limitations to these instances that make them hard to apply to real-world last-mile problems. Some of them include:

* Small instances
* Ignore streets, use only euclidean distances
* No discussion on aggregation levels


### Why a GitHub benchmark

We want to make publishing results as easy as opening a pull-request. We also want to provide you with code to evaluate your solution and make sure it's ready for publication. If you're not familiar with making open-source contributions, don't worry. Open an issue, and we'll be happy to guide you with your submission.


# How to submit

To include your method to the benchmark leaderboards, you must submit the solution data into a pull request. Please check our submission guidelines for more information.

While submitting the code is not required, we strongly suggest making your research code available to make reproducing the results more accessible. You can publish the code on your repository and include a link on your submission. We also have some baselines on this repository. If you want to include your code as a baseline, we'll be happy to revise it.

Don't forget to acknowledge the literature and code you have used on your solution. Use the acknowledgments section for that.

# Instance generation pipeline

If you want more details on how we generate our instances and how they relate to actual deliveries, please check our [generation pipeline documentation](./generation.md). It also includes the steps for reproducing the provided instances.


# Citing this work

If you use this data in academic work, please cite our paper.

```
Coming soon.
```

# Acknowledgments

[]

# Disclaimer

This repository is not an official Loggi product. Use it at your own risk under the terms of the MIT license.
