VRPLoggi Benchmark
==================

A dataset and benchmark for last-mile urban logistics.

# Overview

The VRPLoggi benchark contains a dataset and benchmark scripts for urban logistics
problems. The data is from public sources that are highly correlated with actual deliveries
performed by Loggi on our last-mile step.

# Leaderboards

## Capacitated Vehicle Routing Problem

| Publication date | Team name                | Solution name                | Total distance (km) |
| ---------------- | ------------------------ | ---------------------------- | ------------------- |
| 2020/10/31       | Loggi - Network design   | OR-tools VRP                 | 10000.000           |
| 2020/10/31       | Loggi - Network design   | KMeans + OR-tools VRP        | 10000.000           |


## Capacitated Vehicle Routing Problem with Stochastic Customers 

| Publication date | Team name                | Solution name                | Test total distance (km) | Train total distance (km) |
| ---------------- | ------------------------ | ---------------------------- | ------------------------ | --------------------------|
| 2020/10/31       | Loggi - Network design   | OR-tools VRP                 | 10000.000                | 10000.000                 |
| 2020/10/31       | Loggi - Network design   | KMeans + OR-tools VRP        | 10000.000                | 10000.000                 | 

## Routing + Facility location

OR-Tools (p-HUB + VRP)


# Motivation

### Why a new dataset

There are several famous datasets for the Vehicle Routing Problem (VRP). However, we found some gaps between these datasets and what can be really applied on real-world last-mile problems. 


* Small instances
* Ignore streets, use only euclidian distances
* No discussion on aggregation levels


### Why also a benchmark

Mainteined by a company. Favours solutions that contain code.


# Installing and Running


## Download public data

First we need to download the raw data from IBGE (~350Mb - compressed). If you are 
running a UNIX-based system and have have `wget` and `unzip`, you can do 


```bash
./download.sh

```

If you don't, you can manually download the data through the following links:
* 

Make sure your final file structure looks like:
```
```

# Citing this work
If you use this data in academic work, please cite our paper.
```
tex
```

# Disclaimer

This is not an official Loggi product. Use it at your own risk.