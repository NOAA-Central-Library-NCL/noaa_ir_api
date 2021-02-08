#### Legal Disclaimer

*This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.*

## NOAA IR JSON API


The following Python scripts allow you to interact with the NOAA IR JSON API, either
directly or indirectly.

### CLI Menu

This tool provides a menu to view individual collections as well as download all items from IR. All libraries used within the files are built-ins, with the exception of requests.

#### Usage

Download ```api_query.py``` and ```menu.py``` and place in the same directory. Run python ```menu.py``` in the shell or terminal. Doing so start the following menu:

```
Query NOAA Repository JSON REST API

1. Get CSV of collection
2. Get CSV of all items
3. Quit
```

You can also use ```api_query.py``` which menu.py uses as to retrieve data from the JSON API.

### Stats

Use ```stats.py``` to call to NOAA IR's JSON API using the requests library and transform collections into pandas DataFrames enabling quick analysis.

Methods have been written to enable facet analysis, which can be tricky as the NOAA IR JSON API packs multiple values into a single field.

### CDC Article Monthly Update Stats

Use ```article_monthly_update.py``` stats to generate additional usage stats for
NOAA IR items. Combine this output with ```api_query.py``` or ```stats.py``` to
generate custom reports for stakeholders.
