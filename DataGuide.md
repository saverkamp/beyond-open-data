# Data Packaging Guide

In our daily lives, we are awash in data, visualizations and analysis. Libraries, too, recognize the potential power in expressing our collections and their content as data, and we've made some strides in putting this data online to be downloaded, manipulated, recombined, and analyzed. 

*But who is actually using and making sense of it?* 

If we are to encourage a data revolution in libraries, we will need to make our data more accessible and malleable to more people, civilians and librarians alike, in formats that work with common tools and that make it easy for anyone to learn about the potentials and limitation in our data and collections.

This open document aims to serve as a guide for the work, the people, and the infrastructure that should be taken into consideration when releasing sets of data. 

## About Data Packaging

Data packages are containers for describing and sharing datasets. A data package typically includes a file of metadata listing and describing the features of a dataset, such as creation information, size, format, field definitions, any relevant contextual files, such as data creation scripts or textual documentation, and the data files themselves.   

Why data packages?
* Data is forever: Datasets outlive their original purpose. Limitations of data may be obvious within their original context, such as a library catalog, but may not be evident once data is divorced from the application it was created for.
* Data cannot stand alone: Information about the context and provenance of the data--how and why it was created, what real-world objects and concepts it represents, the constraints on values--is necessary to helping consumers interpret it responsibly.
* Structuring metadata about datasets in a standard, machine-readable way encourages the promotion, shareability, and reuse of data.

## Concerns

These are many issues to consider and mitigate when creating your data packages. They are sorted into categories according to the type of interested party.

The types are:
* Data Creators: stewards of collections
* Data Consumers: people interested in using the data
* Educators: people teaching information science or digital humanities and their students
* The Public: people interested in the work being done by the creators and consumers

### Data Creators

Many people within an institution come together as "data creators": curators, metadata librarians, subject specialists, archivists, et al. In large institutions, it will likely require many people to work together to produce data for a collection. In smaller institutions, it may be only a few or as little as one primary entity.

Here are some concerns from this perspective:
* Information about the completeness and provenance of the collections represented in the data is not clearly communicated.
* Data quality may not always reach desired standards (especially when gathered through crowdsourcing or accumulated over a long time).
* It’s hard to find time or resources to document all of the nuances that consumers might need to know.
* It’s hard to find time or resources to shape data into a format that many people can use (ex. CSV).

### Data Consumers

Data consumers are everyone interested in using, reviewing, gathering, manipulating, and building on top of your data. This may include researchers, subject specialists, hobbyists, people interested in digital humanities, et cetera.

Here are some concerns from this perspective:
* Technical learning curve (lack of knowledge broadly or specific to format; e.g. some people know how to write SQL queries but don't know how to use Docker)
* Technical issues (broken endpoints)
* Not being able to apply same logic to other datasets
* Lack of data dictionary
* Not knowing history of data (How did it get here?)
* Not knowing context for data (What can be found in this collection?)
* Not knowing what data is missing (What is not in this collection, and why?)
* Don't know where to find the data that is meaningful to their work

### Educators

Educators must be able to deliver meaningful high-level concepts and technical skills to students with variable degrees of expertise and domain knowledge. They need data packages that are easy to use and build off of.

Here are some concerns from this perspective:
* Difficult to teach with this dataset
* Not enough information to give appropriate context or support
* Unable to understand what is missing
* Lack of documentation

### The Public

The general public may not be interested in using the data, but they are interested in seeing the results. Without the work from the other interested parties, the public does not have anything to view except the raw data.

So the public has one major concern, and that is:
* **Why should we care?**

## Guidelines

Or, "What you need to do for your data to live forever."

Here are some guidelines for what to consider and how to consider it, broken into the following categories: Consistency, Context, Licensing, Planning, Portability, Publicity, Redundancy, Reproducibility, and Simplicity.

### Consistency

This isn't a guide that presents a single solution to use across all library/archives/museum institutions or even with all datasets within an institution. But there are plans to release datasets within an institution that are similar, or within a consortium of institutions, consider the benefits of using a shared data model and mapping everything to that same planned set of fields in the same format.  

[Frictionless Data](https://frictionlessdata.io/) is an initiative and set of specifications and standards maintained by [Open Knowledge International](https://okfn.org/) in support of machine-actionable, interoperable, self-describing data packages. This is not the only data package specification out there, but Frictionless Data currently has a growing community creating and improving tools for the easy creation and broader use of data packages. 

### Context

#### Description

Describe the collection of data overall. What kind of information can be found here? How and why was it created? 

**Example** 


#### Context

Define the provenance of this collection of data. Where did it come from? When and how was it processed? What was its original format? Why has it been collected? What collections or concepts does it represent? What snapshot in time does the data capture? 

**Example** 

#### Data dictionary

A data dictionary is a mapping of each field you are presenting in your data and some additional information about it to support its usage and lower the barrier to data-wrangling efforts.  

The data dictionary may answer the following questions: What fields are used for each piece of data? What does each field do? What is the data type (number, string, date) of each field? Was the presence of this field, when cataloging, required or optional? What is the allowable range of values for this field? Are controlled vocabularies used? How are null or missing values represented? You may also want to include any caveats about the values, potential errors in data collection or why the data may not conform to the dictionary. How would you clarify any of [these issues](https://github.com/quartz/bad-data-guide) with your data?

**Example** 

| Field | Description | Value | Required? |
| ----- | ----------- | ----- | --------- |
| ID | The unique identifier for the item. | number | required |
| Title | Primary title of the item. | string | required |
| Description | Description of the item. | string | optional |

### Licensing 

Licensing can be a significant barrier to data usage. A license should be chosen carefully and in association with your institution's legal department, when applicable. 

* Choose an open license
* State the chosen license clearly and prominently
* Explain the liberations/limitations of the chosen license, and what restrictions may apply
* Let users know where they can find more information about this license
* Explain that the license applies to the data, and not the content that the data represents (an open license on the metadata is not the same as the content itself being open, out of copyright, or able to be used freely)
* Explain why this license was chosen

**Examples** 

[RightsStatements.org](http://RightsStatements.org) is an initiative by DPLA and Europeana that seeks to simplify and clarify rights statements for use in cultural heritage institutions.  

[Open Data Commons](https://opendatacommons.org/), an Open Knowledge International initiative offers three open data licenses and instructions on use.  

The [Creative Commons Zero license](https://wiki.creativecommons.org/wiki/CC0_use_for_data) is also frequently used for explicitly dedicating datasets to the public domain. 

### Planning

Plan your data packaging strategy at the beginning of a project, if possible. Don't wait until the last minute to think about how to distribute your data. Bring collection curators and metadata specialists into technology projects early, and bring them in often. This includes projects in which releasing data publicly is not the exclusive goal of the project, but data is generated as a result. Web applications should always have a way to get data out of them, because they may not always be sustained. Planning for data extraction is an important portion of planning for the sunsetting of a project.

### Portability

Can your data be easily moved and manipulated? The answers to this section are contingent on the size of your dataset. Can it be easily manipulated if presented as a spreadsheet, or is the data too large for someone to open using a CSV-reading application? Even if the data is too big for Excel, consider how easily the data could be manipulated using scripts even if stored as a CSV.
For data that is very large and unwieldy, consider containerizing the entire package using a containerization system like Docker or Vagrant.

### Publicity

*If a tree falls in the forest but no one is around to hear it, does it make a sound?*  

If you release your data but don't tell anyone about it… no one will be able to use or benefit from it! Plan a public outreach strategy around your dataset and coordinate with your public relations department, when possible. At the very least, add clear definitions and links to your data packages available on your institution's website.

### Redundancy 

*LOCKSS: Lots of copies keeps stuff safe.*   

Are we treating the data of our collections with the same respect as the collections themselves? Where are you storing your data *and* where *else* are you storing your data? Data packages also need to be stored securely in multiple locations.

The Internet Archive is a good place to store data packages in addition to trusting your institution to care for the material long-term. It can handle the uploading of large files and is easily accessible by the general public.

### Reproducibility  

Make sure your data doesn't just run on your machine perfectly, but that the results are consistent regardless of the user and operating system they are using to access your data packages.

### Simplicity

Choose a low-barrier data format that works with open and easy-to-use tools. Like portability, this will depend on the type and size of data you are releasing, which will shape your larger data packaging goals.  

Strongly consider publishing a version of your data in CSV, so it can be used by more people. CSV is human-readable on its own, but can also be viewed and manipulated using many existing tools, like Google Sheets and [OpenRefine](http://openrefine.org/). Large or complex data sets can be distributed via multiple CSV files containing the flattened data. Get creative with distribution and it will increase interest in accessing your collections. 

## Examples

[ Examples go here ]  

## Additional Resources

### People

[Collections as Data](https://collectionsasdata.github.io/)

### Systems

[CKAN](https://github.com/ckan/ckan): An open-source DMS (data management system) for powering data hubs and data portals.

### Tools

[Datasette](https://github.com/simonw/datasette): An instant JSON API for SQLite databases.  
[Frictionless Data](https://frictionlessdata.io/specs/): a containerization format for any kind of data based on existing practices for publishing open-source software.  
[mira](https://github.com/davbre/mira): A simple HTTP API for CSV files.  
[sheetsee.js](https://github.com/jlord/sheetsee.js): A client-side library for connecting Google Spreadsheets to a website and visualizing the information with tables and charts.  

## Credits

[Shawn Averkamp](https://github.com/saverkamp/)  
[Ashley Blewer](https://github.com/ablwr/)  
[Matt Miller](https://github.com/thisismattmiller/)  
