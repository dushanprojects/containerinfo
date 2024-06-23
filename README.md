# Project Overview
Repository for Query Container Resource Information. The code resides within the api directory.


## Building and Scaning Docker Image:
A separate GitHub Actions workflow is responsible for building, pushing, and scanning the Docker image. This image is publicly available on Docker Hub at dushansri/containerinfo:latest.

## Installing the containerinfo Helm Chart
Follow these steps to manually install the containerinfo Helm chart:

#### 1. Validate Templates with Debugging
Validate the templates and output them for debugging purposes. This helps ensure everything is set up correctly before actual installation.
```
helm template test helm/containerinfo --debug
```

#### 2. Install the Chart 
Install the Helm chart with a specific release name and namespace
```
kubectl create ns my-home-assignment
helm install containerinfo helm/containerinfo -n my-home-assignment
```

#### 3. Upgrade the Chart
Once the changes were made to your helmchart, you can update the existing release.
```
helm upgrade containerinfo helm/containerinfo -n my-home-assignment
```