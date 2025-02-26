#### Legal Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

## NOAA IR JSON API

The following Python scripts allow you to interact with the NOAA IR JSON API.

### API Query script

Use `api_query.py` to query NOAA IR records, downloading a single collection or entire IR collection as a whole. Additionally, in doing so, you utilize `fields.toml` file to filter for specific IR API fields. A date range filter method is also available for limiting your search of records **from** a formated YYYY-DD-MM date **until** formatted YYYY-DD-MM date.

If you wish to download a single IR collection or entire IR collection as a whole with all IR fields, please refer to the NOAA Repository IR API repo. 

##### `fields.toml`

Use `fields.toml` field to pass in specific fields you wish to parse as well as optional date parameters. `fields.toml` is first passed in a command line argument, then passed in an parameter to the `RepositoryQuery` class during instantiation. 


### IR fields

The API fields in records are composed of four main categories, each usually begin with the following prefix, the exception being PID: 

- PID
- mods
- dc
- fgs
- DS
 
#### PID

**PID** is an IR record's unique identifier, and prepend it with the following string - ***https://repository.library.noaa.gov/view/noaa/*** you have a IR document URL (i.e. https://repository.library.noaa.gov/view/noaa/5695).

#### mods and dc

**mods** fields contains an IR record's descriptive metadata (e.g. 'mods.title', 'mods.abstract')

**mods** and **dc** and both contain descriptive metadata; however, they both contain the same information, but **mods** contains additional fields not found in **dc** fields, so it is recommended to pull from **mods** fields.

#### fgs

**fgs** fields contain an IR record's adminstrative metadata ('fgs.createdDate', 'fgs.lastModifiedDate')

#### DS

**DS** fields contain an IR record's source field information. This field will always follow a specific pattern for an record: 

 - Begin with DS1, which stands for the record's main document
 - Each 'DS' instance will increment by +1 as long as there are supporting files for the record (i.e. If there are two supporting files for an record, there will be DS2, DS3). 
 - For each DS instance, there are four fields:
    - mimetype_txt_en: mime type
    - label_txt_en: filename 
    - filesize_tl: in bytes
    - checksum_txt_en: sha256
    - sourceurl: if available