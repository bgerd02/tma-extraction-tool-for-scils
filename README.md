This repository contains code for a basic pixel extraction tool for MSI data stored in .slx files.

The executables stored in dist are software packages that provides a user interface to extract pixel-level intensities from MSI data. It utilizes the Bruker SCiLS Lab API and is thus only able to interact with .slx file types. The user is able to specify the extraction normalization (ex. Total Ion Count), the feature list to extract from, the region(s) to extract, and the format of the output (.txt or .csv). 
