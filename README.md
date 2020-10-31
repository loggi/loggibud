VRPLoggi Benchmark
==================

A dataset and benchmark for last-mile urban logistics.

# Overview

This repository contains the dataset and benchmark scripts for the VRPLoggi benchark. 
The data is from public sources that are highly correlated with actual deliveries
performed by Loggi on our last-mile step.


# Motivation

### Why a new dataset

There are several famous datasets for the Vehicle Routing Problem (VRP). Some examples
are:


However, we found some gaps between these datasets and what can be really applied on
real-world last-mile problems. 

* Small instances
* Ignore streets, use only euclidian distances
* 

### Why a new benchmark

Mainteined by a company.
Favours solutions that contain code.


# Challanges

## Capacitated Vehicle Routing Problem


K-Means + VRP


## Capacitated Vehicle Routing Problem with Stochastic Customers

K-Means clustering
Sweep


## Location-Allocation problems

OR-Tools (p-HUB + VRP)


# Installing and Running

## Download public data

If you are running a UNIX-based system and have have `wget` and `unzip`, you can do:

```bash
./download.sh
```

If you don't, you can manually download the data through the following links:

* 

# Citing this work

If you use this data in academic work, please cite our paper.


```
tex
```


# Disclaimer

This is not an official Loggi product. Use it at your own risk.