#LSDServer SQLAlchemy Backend

## Introduction
This document describes how the SQLAlchemy backend works behind the scenes to store.

## Strategy
For _smallish_ tables, the built-in ORM capabilities of SQLAlchemy are used.

This gives the advantage of rapid, easy development for these areas of the system.

The exception to this rule are the observations and observation_flags tables which are created using raw SQL.  This allows lots of data to be entered and used without having to worry about table joins for the vast majority of database lookups.

## Entity Relationship Diagram
```
platform ---< sensor ---< parameter >--- user_phenomena
                             .
                             .
                             .
                             o_N ---< o_f_N


                             user_flag



```
* Observation `o_N` table doesn't have any referential integrity linking it to the parameter
* New observation `o_N` and observation flags `o_f_N` tables are created for each row in `parameter`
* user_phenomena allows for user-defined phenomena to be created
* user_flag allows user-defined flags to be created

## Example tables
Its best to have a look at a few examples so that we can see how data would be stored in the real world.

Imagine you had built a couple of DIY weather stations and them at a couple of sites.  Each weather station has an identical sensor and measures temperature and humidity.


(PK) = Primary Key
(AI) = Auto increment
### platform

| id (PK) | name | description | info | position | mobile |
| ------- | ---- | ----------- | ---- | -------- | ------ |
| coogee | coogee weather station | homemade weather station | http://... | POINT(151.25525 -33.91837) | false |
| canberra | canberra weather station | homemade weather station | http://... | POINT(149.12868 -35.28200) | false |

* info field contains link to web page (see API)
* name and description are optional and can be used to embed small notes
* position column uses spatial datatype _point_

### sensor

| manufacturer (PK) | model (PK) | serial number (PK) | platform_id (PK) | description | info |
| ----------------- | ---------- | ------------------ | ---------------- | ----------- | ---- |
| TI | HDC1000 | 13252030.f | coogee | TI temp & humidity | http://www.ti.com/lit/gpn/hdc1000 |
| TI | HDC1000 | 13262024.f|  canberra | TI temp & humidity | http://www.ti.com/lit/gpn/hdc1000 |

* info field contains link to website or a hosted local file (/data...), typically this will be a datasheet for sensors

### parameter

| platform_id (PK) | sensor_manufacturer (PK) | sensor_model (PK) | serial_number (PK) | phenomena (PK) | observation_table (AI) |
|----------------- | ------------------------ | ----------------- | ------------------ | -------------- | ---------------------- |
| coogee | TI | HDC1000 | 13252030.f |  http://lsdserver.com/phenomena/temperature | 1 |
| coogee | TI | HDC1000 | 13252030.f | http://lsdserver.com/phenomena/humidity | 2 |
| canberra | TI | HDC1000 | 13262024.f|  http://lsdserver.com/phenomena/temperature | 3 |
| canberra | TI | HDC1000 | 13262024.f| http://lsdserver.com/phenomena/humidity | 4 |

* The full table name for observations is obtained by prepending "o_" to the observation_table field

###  Observation tables
Observation tables are created automatically by LSDServer as and when new parameters are registered.

Although in theory a single table could be used for observations, in practice this would lead to a _skinny, long, thin_ table with lots of joins needed to isolate data.  In practice, this gives poor database performance for general requests.

Such a table could be created through a view if required.

#### o_1
Observations table

| timestamp (PK) | value |
| -------------- | ----- |
| 1434268755 | 112.8 |
| 1434268755 | 23.1 |
| 1434268755 | 24.1 |

* timestamps are stored in database natural format and are entered in zone UTC
* the column type of the `value` is determined at table creation time by inspecting the value of the parameter's `phenomena` column

#### o_f_1
Observation flags table.  This table links quality control flags back to specific observation records.  They can be inserted automatically by the system or manually by the the user making a REST request

| timestamp (PK) | flag (PK) |
| -------------- | --------- |
| 1434268755 | http://lsdserver.com/flags/implausable |

### user_phenomena

| term (PK) | data_type | min_valid | max_valid | uom | description |
| --------- | --------- | --------- | --------- | --- | ----------- |
| http://vocab.nerc.ac.uk/collection/P02/current/ALKY/ | double | pH | 6.0d | 9.0d | Alkalinity, acidity and pH of the water column |

* Example of how a custom phenomena would be stored
* pH scale ranges from 0-14 but seawater typically [ranges from 7.5 to 8.4](https://en.wikipedia.org/wiki/Seawater)
* Measurements outside this range can be automatically flagged as being in error (_TODO_)
* The phenomena needs to be registered with LSD Server before it is usable so that the data type can be set correctly in the observations table

### user_flag

| term (PK) | info |
|---------- | ---- |
| http://vocab.nerc.ac.uk/collection/B06/current/xCsrformTimesValid/ | null |
| mark | data marked for removal |

* Example of how a custom user flag would be stored
* No special handling is required for flags, they're simply associated with an observation record and data consumers can then use them as they please
* info column can contain a link or a short plain text message
