# NYPL Digital Collections Collection Data Packager

by [Shawn Averkamp](https://github.com/saverkamp)  

This script takes a Digital Collections collection identifier (UUID) and uses the [Digital Collections API](http://api.repo.nypl.org/) to retrieve metadata some image details for all items in a collection and then convert from MODS XML to a flat CSV format. It also fetches the collection-level record to create a datapackage.json file describing the content and schema of the CSV file. (Code is still very much a work in progress, but instructions at the end of this page on running it.)  

We don't see a lot of use of the Digital Collections API, partly I think because the metadata schema is difficult to understand for the layperson and also because we don't have an easy call for what people are usually interested in--data and images from a specific collection. I wanted to try to simplify this process for users not intimately familiar with our API and also make the data simpler and flatter, so users of many skill levels can explore it with existing spreadsheet tools. In my own process, I wanted to get a better sense of what is lost when you map from a hierarchical XML schema to a flat table schema and to closely consider what loss is acceptable and what loss is potentially dangerous to user comprehension of these digital representations (which are already a generation removed from the originals).  
 

## Running the data packager

These scripts run on Python 2.7 and use the following third-party libraries:  
`lxml`  
`requests`  

This script requires a Digital Collections API key, which can be obtained at [http://api.repo.nypl.org/sign_up](http://api.repo.nypl.org/sign_up). Add this key to the `config.ini` file as the value of `token`.

To generate a CSV of items from an NYPL collection, run the `getNyplMods.py` script on the command line, including a collection uuid as a second argument (You can find the collection uuid at the bottom of the "About" tab of the left sidebar of any [Digital Collections collection page](https://digitalcollections.nypl.org/collections).):  

`>> python getNyplMods.py 5e789350-c5dc-012f-1163-58d385a7bc34`  

This should create a new directory that contains:
* a CSV file with a file name that reflects the collection name (ex. "robinson-locke-collection.csv")  
* a `datapackage.json` file that contains the metadata and data dictionary for your collection data

