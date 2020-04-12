# SinuosiTime: evaluating the spatio-temporal evolution of the sinuosity of channels undergoing base-level fall cut by groundwater-fed springs using high-resolution satellite imagery
*Presentation of a method for creating time series of channel sinuosity evolution from satellite imagery, along with a brief description and interpretation of results from the Ghor Al-Haditha study site, eastern Dead Sea shore, Jordan.*


**Robert A. Watson**\
Department of Earth Sciences, University College Dublin, Ireland\
*robert.watson@ucd.ie*

**Date published**: 5th April 2020

## Summary

This is a method I developed during my masters for calculating the sinuosity (ratio of channel centre-line length to valley length) of stream channels using satellite images from different timestamps. The method involves manually digitising the channel centreline 'thread' as a line shapefile for each timestamp in a GIS software package, and then calculating the sinuosity for each timestamp with a new Python library '*sinuutils*' written for the task. A moving window of fixed length is applied to interrogate each sinuosity timestamp spatially, with the channel profile resampled at 1 m intervals to normalise for length. Results obtained for the Dead Sea eastern shore site of Ghor Al-Haditha in Jordan are presented. At this site, channels cut by groundwater springs have developed new meanders, modified existing meanders and incised vertically since the year 2000, their evolution apparently triggered by the decline in Dead Sea level (the regional hydrological base-level), which has fallen almost 40 m since the 1960s, and the synchronous retreat of the lake shoreline.  


## Necessary data and software

To digitise channel centrelines and meander belt axes, you will need access to a time series of satellite imagery of appropriate resolution and software which supports digitisation of features as polyline shapefiles. This could be done using, for example, Google Earth or QGIS (using the the Google Earth Engine plugin for accessing Google's database of satellite imagery). My sample data is given within the folder *'sinuosity_shapefiles'*.

To perform the data processing and necessary analysis, I have used an interactive Python notebook environment (Jupyter within Anaconda). The dependent Python libraries for running the scripts are: math, matplotlib, numpy, pandas, pyshp, and string. Full dependencies are given in the environment file *'environment.yml'*. To install a given Python package, run the following command:

*pip install <package_name>* 

or, if working in a conda environment

*conda install <package_name>*

## Running the code

The sample workbook is published in the folder '*python*', and is named *'sinuosity_analysis_workbench.ipynb'*. A markdown file of this code is also published with the same name. All of the functions which underlie the analytical steps have been incorperated into a new python library, *'sinuutils'*, and comprise the python script *'sinuutils.py'*.

## Sample application to real-world geomorphology

An example of how I used this method to analyse stream channel geomorphology through time during my masters' thesis is given in the file *'method_results_presentation.md'*. I present the application of the method to one channel in the study area, which is located at the Dead Sea and has a [very rapidly evolving geomorphology](https://www.solid-earth.net/10/1451/2019/se-10-1451-2019.html).

## Improvements and future work

The method outlined here has several issues that need fixing (this will be done in due course). I've [raised issues](https://github.com/wobrotson/SinuosiTime/issues) where I think improvements can be made to the code. If you notice anything that you think should be improved, related to either the code itself or my geomorphological assumptions and interpretations, please let me know by raising an issue yourself!

I have a few ideas for future directions for the project, such as integrating the tool with other Python codes written to analyse stream channels. Some possible software packages that could be integrated include:

- [curvaturepy](https://github.com/zsylvester/curvaturepy) for analysing migration of meanders over time and the time series of meander curvature;
- [DeepRiver](https://github.com/isikdogan/deepriver), for automation of channel centreline extraction;
- [ChanGeom](https://github.com/BodoBookhagen/ChanGeom) for estimating and modelling channel planform topography in the case that high-resolution topographic models are not available. 

If you would like to collaborate on these then I would love to hear from you!

Ultimately, I hope to be able to turn the method into a plugin for QGIS, so that it can be used directly within one software package. This may take some time...
