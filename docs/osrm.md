Computing Street distances
======

Some of our instances are provided with precomputed distance matrixes. However, for some problems providing these matrixes is unfeasible due to the quadratic cost of computing them. For these problems we recommend solvers to run their own street distance calculator. We recommend it to be consistent with our own evaluation pipeline.

Our pipeline for computing street distances is based on OpenStreetMaps and OSRM. Two amazing open source projects that make this work possible.

# Running a distance server 

The easiest way to use to reproduce the distances computed on the benchmark is thorough an OSRM server using docker. This can be done with the following steps:

1. Download and install docker according to your operational system.
2. Download our [precompiled distance files](https://loggibud.s3.amazonaws.com/osrm/osrm.zip) (5.3Gb compressed, 12.6Gb decompressed).
3. Extract the files into an `osrm` directory.
3. Run an OSRM backend container with the following command:

```
docker run --rm -t -id \
	--name osrm \
	-p 5000:5000 \
	-v "${PWD}/osrm:/data" \
	osrm/osrm-backend osrm-routed --algorithm ch /data/brazil-201110.osrm --max-table-size 10000
```

# I have no resources to run my own server

Don't worry, OSRM provides a test instance at `http://router.project-osrm.org`. It may not be 100% equal to our distances, but it should be broadly consistent. It is probably ok to evaluate your solution using OSRM public server and just obtain the final results with our version of the maps.

# Recompiling map files

We provide the precompiled files to ease development. We recommend using them for further devolopment.

This section describes how we compile the maps, in case you want to reproduce the provided files or generate them with the latest version of the maps. Our pipeline is based on Brazil OpenStreetMaps version 201110. You can download it [from Geofabrik](http://download.geofabrik.de/south-america/brazil-201110.osm.pbf) or through our [S3 mirror](https://loggibud.s3.amazonaws.com/osrm/brazil-201110.osm.pbf).

We use the basic configuration from OSRM using contraction hierarchies. This may take about 14Gb of RAM and 3h on an i7 CPU. Double chek your RAM and swap space before proceeding.

```
docker run --name osrm --rm -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/brazil-201110.osm.pbf
docker run --name osrm --rm -t -v "${PWD}:/data" osrm/osrm-backend osrm-contract /data/brazil-201110.osrm
```
