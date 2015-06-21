# LSDServer API -- Version WIP (technology preview)

# entry point
[/]()

## Allowed HTTP verbs
| Verb | Description | Status code |
| ---- | ----------- | ----------- |
| GET | System homepage | 200 OK |

***

# Version
[/version]()

Software and API version

## Allowed HTTP verbs
| Verb | Description | Status code |
| ---- | ----------- | ----------- |
| GET | version information | 200 OK |

***

# Platforms

A platform is a base to which a group of sensors are attached.  For example, a weather station, an autonomous vehicle or a satellite would all be considered as platforms.

## Fields
The following fields are available (identifier is encoded into the URL):
* name (string)
* description (string)
* info (string, a relative or absolute URL)
* position (fixed location _point_ for this platform, [WKT](https://en.wikipedia.org/wiki/Well-known_text) used as transport format)
* mobile (false - not *currently supported*)

## JSON transport format
```json
{
  "platform_id": "platform_id",
  "name": "platform_name",
  "description": "platform_description",
  "info": "http://link_for_more_info",
  "position": "POINT(0,0)"
}
```

## Platform Collection
[/platform/]()

## Platform Collection -- Filtering

### Location
[/platform/?location=POLYGON((138.515625+-27.839076094777802,154.3359375+-27.839076094777802,154.3359375+-40.044437584608566,138.515625+-40.044437584608566,138.515625+-27.839076094777802))]()
Filter by bounding polygon (the example above draws a box around Australia)

### Common properties
You can also filter based on matching any of the following properties:

_platform info_
* ID
* name
* description
* info

_sensor info_
* sensor_manufacturer
* sensor_model
* sensor_serial_number
* sensor_description
* sensor_info

_parameter info_
* parameter_phenomena

eg:
[/platform/?name=Canberra]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | List all known platforms (optionally, filter them)| 200 OK |
| POST | Create platform with system assigned ID | 201 CREATED |

## Platform Element
[/platform/\<platform_id\>/]()

Once you have a specific platform_id (or you've generated your own), your able to lookup its information, create a platform or delete a platform *and any associated data*.

Whole platform records cannot be updated.

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | Read a platform by ID | 200 OK |
| PUT  | Create a platform | 201 CREATED |
| DELETE | Delete a platform | 204 NO CONTENT |

## Platform element metadata (info)
[/platform/\<platform_id\>/info]()

You can obtain the metadata for a platform (if available) via this URL.  LSD Server will send a 302 redirect request to the user's browser with the real location of the info resource.

If a PUT request is made to this URL containing an uploaded file, LSD Server will make the file available as a static resource and will update the platform's info field to reference it.  If a string starting "http" is PUT, then this will be stored and clients accessing in the future via GET will be redirected to the referenced site

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | Redirect to platform info | 302 FOUND |
| PUT  | Replace info URI with uploaded file or URI | 201 CREATED |
| DELETE | Remove any uploaded file and remove link from metadata | 204 NO CONTENT |

## Platform element location
[/platform/\<platform_id\>/location/]()

Get WKT _point_ for the platform's location.  We don't handle moving platforms yet.  In the future this could endpoint could return a linestring or a polygon.

### Allowed HTTP verbs
| Verb | Description | Success Code |
| ---- | ----------- | ------------ |
| GET  | Get WKT of platform location | 200 OK |

***

# Sensors
A sensor is a device which is associated with a platform and records one or more parameters.

## Fields
* manufacturer (string, mandatory)
* model (string, mandatory)
* serial number (string, mandatory)
* description (string)
* info (string, a relative or absolute URL)

## JSON transport format
```json
{
  "platform_id": "platform_id",
  "manufacturer": "sensor_manufacturer",
  "model": "sensor_model",
  "serial_number": "sensor_serial_number",
  "description": "sensor_description",
  "info": "http://..."
}
```
## Sensor Collections
* [/sensor/]() All registered sensors
* [/sensor/\<platform_id\>]() All sensors associated with given platform

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | Get a list of sensors and optionally filter it | 200 OK |

## Filtering the sensor list

### Common properties
You can filter based on matching any of the following properties:

_sensor info_
* sensor_manufacturer
* sensor_model
* sensor_serial_number
* sensor_description
* sensor_info

_parameter info_
* parameter_phenomena

eg:
* [/sensor/?sensor_model=tm302]() _all registered tm302 sensors_
* [/sensor/\<platform_id\>/?sensor_model=tm302]() _all tm302 sensors attached to given platform_

## Sensor Element
Sensors are identified by the natural key of:
* manufacturer
* model
* serial number

and MUST be associated with a platform

[/sensor/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | Read a sensor record | 200 OK |
| PUT | Create a sensor record | 201 CREATED |
| DELETE | Delete a sensor record | 204 NO CONTENT |

## Sensor Element metadata (info)
[/sensor/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>/info]()

You can obtain the metadata for a sensor (if available) via this URL.  LSD Server will send a 302 redirect request to the user's browser with the real location of the info resource.

If a PUT request is made to this URL containing an uploaded file, LSD Server will make the file available as a static resource and will update the sensor's info field to reference it.  If a string starting "http" is PUT, then this will be stored and clients accessing in the future via GET will be redirected to the referenced site

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | Redirect to metadata URI | 302 FOUND |
| PUT | update metadata URI or upload file to serve | 201 CREATED |
| DELETE | Delete metadata URI and any associated hosted content | 204 NO CONTENT |

***

# Parameters
Parameters are phenomena measured by sensors which are attached to platforms.  Many sensors measure more then one parameter which is why this mechanism is needed.

Parameters are identified by the natural key of:
* manufacturer
* model
* serial number
* phenomena
and MUST be associated with a platform AND a sensor

## Fields
* platform_id _link to platform_
* manufacturer _link to sensor_
* model _link to sensor_
* serial_number _link_to_sensor_
* phenomena (string, URI referencing the phenomena this parameter measures *or* an integer referencing a definition hosted in this server)

## JSON transport format

```json
{
  "platform_id": "platform_id",
  "manufacturer": "sensor_manufacturer",
  "model": "sensor_model",
  "serial_number": "sensor_serial_number",
  "phenomena": "http://..."
}
```

## Parameter Collections
* [/parameter]() _all known parameters_
* [/parameter/\<platform_id\>]() _all parameters associated with given platform_id_
* [/parameter/\<platform_id\>/\<manufacturer\>]() _all parameters associated with given platform_id and manufacturer_
* [/parameter/\<platform_id\>/\<manufacturer\>/\<model\>]() _all parameters associated with given platform_id, manufacturer and model_
* [/parameter/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>]() _all parameters associated with given platform_id, manufacturer, model and serial_number_

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | Read parameter information, optionally search | 200 OK |

## Filtering the parameter list

### Common properties
You can filter based on matching any of the following properties:

_parameter info_
* parameter_phenomena

eg:
* [/parameter/?parameter_phenomena=http://...]() _all registered parameters with matching phenomena_
* [/sensor/\<platform_id\>/?parameter_phenomena=http://...]() _all registered parameters with matching phenomena attached to given platform_

## Parameter Element

[/parameter/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>/\<phenomena\>]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | Read parameter information, optionally search | 200 OK |
| PUT | Create a new parameter and associate it with a sensor, platform and phenomena | 201 CREATED |
| DELETE | Delete a parameter and associated data | 204 NO CONTENT |

***

# Phenomena
Phenomena describe the physical conditions being measured by a parameter.  There are several built-in phenomena which are described on-line at http://lsdserver.com/phenomena

Users are able to reference the phenomena by supplying a phenomena URI for the phenomena field when registering a parameter with LSD Server.

Alternatively, users may define their own phenomena and reference them by URI when registering parameters.

TODO built in support for stuff like images, videos, mp3 etc


## Fields
* term (string, mandatory)
* data_type (string, mandatory, identifies the data type, eg  double)
* min_valid (double, minimum valid value for this phenomena)
* max_valid (double, maximum valid value for this phenomena)
* uom (string, freetext identifying unit of measure)
* description (string, freetext for notes)

## JSON transport format
```json
{
  "term": "http://term...",
  "data_type": "phenomena_data_type",
  "min_valid": 0,
  "max_valid": 0,
  "uom": "phenomena_uom",
  "description": "phenomena_description"
}
```

## Phenomena Collection
[/phenomena]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | List phenomena | 200 OK |
| POST | Create phenomena with system generated identifier | 201 CREATED |

## Filtering the phenomena list

### Common properties
You can filter based on matching any of the following properties:

_phenomena info_
* term
* data_type
* uom
* description

eg:
* [/phenomena/?uom=degrees celcius]()

## Phenomena Element
Phenomena are identified by their `term` which should be a URI pointing outside of the LSD Server system, although one can be generated for you by POSTing to the collection URI if necessary.

[/phenomena/\<term\>]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | Read a phenomena | 200 OK |
| PUT | Register a phenomena | 201 CREATED |
| DELETE | Delete a phenomena and associated _local_ data | 204 NO CONTENT |

***

# Flags
Flags are marks applied to individual observations.  Built-in flags are described at http://lsdserver.com/flags.  Users may also define and reference their own flags.

## Fields
* term (string, mandatory, ideally a URI)
* description (string, freetext for notes)

## JSON transport format
```json
{
  "term": "http://...",
  "description": "flag description"
}
```

## Flag Collection
[/flag]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | List all known flags | 200 OK |
| POST | Create a flag with a system generated ID | 201 CREATED |

## Filtering the flag list

### Common properties
You can filter based on matching any of the following properties:

_phenomena info_
* term
* description

eg:
* [/flag/?description=the description]()

## Flag Element
Flags are identified by their `term` which should be a URI pointing outside of the LSD Server system.

[/flag/\<term\>]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET | Read a flag | 200 OK |
| PUT | Register a flag | 201 CREATED |
| DELETE | Delete a flag | 204 NO CONTENT |

***

# Observations
Observations are individual measurements stored for each parameter on each sensor on each platform.

An observation typically comprises:
* timestamp (UTC)
* value
* flags

# JSON transport format
```json
{
  "timestamp": 0,
  "value": 0.0,
  "flag": [
    "http://...",
    "http://..."
  ]
}
```

## Observation Collections
[/observation/\<platform_id\>/\<sensor_manufacturer\>/\<sensor_model\>/\<sensor_serial_number\>/\<phenomena\>]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | List known observations (limited) | 200 OK |
| POST | Create a new observation using the system time OR create batch of observations with supplied timestamps| 201 CREATED |

## Observation Element
Observations are uniquely identified by the combination of:
* platform_id
* sensor_manufacturer
* sensor_model
* sensor_serial_number
* phenomena
* timestamp _unix timestamp in UTC_
LSD Server uses this combination of data to identify the correct place to store observations for a given parameter.

When creating observations, the timestamp may be omitted and LSD Server will use the current system time.  This is to support systems which do not have an RTC.

[/observation/\<platform_id\>/\<sensor_manufacturer\>/\<sensor_model\>/\<sensor_serial_number\>/\<phenomena\>/<timestamp>]()

### Allowed HTTP verbs
| Verb | Description | Success code |
| ---- | ----------- | ------------ |
| GET  | List known observations (limited) | 200 OK |
| PUT | Create a new observation for this timestamp | 201 CREATED
| DELETE | Delete this observation | 204 NO CONTENT

***

# General Notes
* Complex metadata should be stored outside of LSD Server, there are specialist systems available to do this such as [GeoNetwork](http://geonetwork-opensource.org/) or you could just reference a  static web page
