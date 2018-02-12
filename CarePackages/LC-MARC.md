# LC/MARC Work by Matt Miller (transcribed by Ashley Blewer)

How do you release perhaps the most unfriendly data format for a general audience, MARC files? 

Using Library of Congress’s recently released data (just the Book data, not serials or music) we were thinking about how make it more accessible. We can convert them to CSV and JSON files but then you end up massive files that are hard to work with. There has been suggestions to use SQLite and tools like [Datasette](https://github.com/simonw/datasette) to make data easily browse-able. We wanted to see how well this would work.

## Converting to SQLite
We did not want to make a massively comprehensive mapping, as there are very few key fields that makes the data interesting to work with. If you did want to do that there are already extensive tools like Blacklight to build a index, basically building a catalog, which is not the goal.

But of course people underestimate the complexity of MARC records, repeated fields, very difficult not as easy as just saying "oh put it in a SQLite database."

So thought about a couple use cases: 
- I want to see how things or organized, using subject headings, find books based on subject headings.
- I want to make a mini-lccn lookup services for myself, give it an LCCN and it returns the ISBN or it returns the publisher, etc.

So we made two SQL databases, one that held subject heading information connected to titles and one focused more on technical metadata connected to titles, identifiers, dates, publishers, etc.

The mapping is available here: [https://github.com/thisismattmiller/lc-sqlite](https://github.com/thisismattmiller/lc-sqlite) 

There are scripts for each database. This is nice because you can simply add fields you are interested in or put indexes on various fields.

The resulting files are SQLite DBs that you can use. In this case, for each database, the subjects and titles were 5GB each. 

https://s3.amazonaws.com/lc-sqlite/lc_books_subjects.db.gz (1.2GB)  
https://s3.amazonaws.com/lc-sqlite/lc_books_titles.db.gz (2GB)  

The next step is to work with the data. You can interact with it right on your computer using the sqlite3 command line tool and run queries, or write simple Python scripts to work with it, or use a tool like [Datasette](https://github.com/simonw/datasette) to make a web interface and API endpoint.

Very easy to install: https://s3.amazonaws.com/lc-sqlite/datasette_intall.gif

![](assets/images/datasette_install.gif)

Examples:
Search for subject headings and then reduce it to a title search  
![](/assets/images/e1.jpg)  
[Download video of example](https://s3.amazonaws.com/lc-sqlite/subjects_search_example_star_trek.mp4)  

Search for a known subject heading:  
![](/assets/images/e2.jpg)  
[Download video of example](https://s3.amazonaws.com/lc-sqlite/subjects_search_example_foucault.mp4) 
 
Make your own LCCN API service for local work:  
![](/assets/images/e3.jpg)  
[Download video of example](https://s3.amazonaws.com/lc-sqlite/titles_lccn_api_example.mp4)  

The URL for this would then be something like: http://127.0.0.1:8001/lc_books_titles-b5b0894/titles.jsono?lccn__exact=73005618
And that could be used to do these types of look-ups.

## Problems

- The size of the LC MARC files (around 10M records) is a little too large for this tool. 
- It is a nice way to play around with it though and explore the dataset if you have some familiarity with SQL syntax.

## Thoughts

MARC data is complicated, but if you think about building your own database for a specific use case and releasing that as a data package, it makes thing much more manageable.

This is a super cheap way of building an API. If you put indexes on everything you wanted and stay away from full text search you could totally setup some simple API endpoints for people to use.

