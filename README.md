This repository contains code for a basic pixel extraction tool for MSI data stored in .slx files.

The executables stored in dist are software packages that provides a user interface to extract pixel-level intensities from MSI data. It utilizes the Bruker SCiLS Lab API and is thus only able to interact with .slx file types. The user is able to specify the extraction normalization (ex. Total Ion Count), the feature list to extract from, the region(s) to extract, and the format of the output (.txt or .csv). Note: I am having some trouble uploading v1.2.0, but am working on fixing that. 

Notes for usage
* You cannot run PET on a .slx file that is actively open. 
* Exporting to .txt is generally much faster than exporting to .csv
* Given the SCiLS API methods, the m/z values/features will be listed as two values separated by an underscore. You can match this up with the m/zs in your feature list manually after the file is generated.
* Regions are identified by their attributes. When you enter a word, it will identify any region with that listed as an attribute. I find using the attribute editor to classify different regions to be the easiest way to do this.
