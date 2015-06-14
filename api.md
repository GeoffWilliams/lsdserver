# LSDServer API

# entry point
[/]()

# Version
[/version]()

Software and API version

### Allowed HTTP verbs
* GET

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
```
{
  "name": "platform_name",
  "description": "platform_description",
  "info": "http://link_for_more_info",
  "position": "POINT(0,0)"
}
```

## Listing known platforms
[/platform/]()

List all known platforms

### Allowed HTTP verbs
* GET (read only listing)

## Creating, Reading, Updating and Deleting specific platforms
[/platform/\<platform_id\>/]()

Once you have a specific platform_id, your able to lookup its information, update the record or delete a platform *and any associated data*.

### Allowed HTTP verbs
* GET
* PUT
* DELETE

## Platform metadata (info)
[/platform/\<platform_id\>/info]()

You can obtain the metadata for a platform (if available) via this URL.  LSD Server will send a 302 redirect request to the user's browser with the real location of the info resource.

If a PUT request is made to this URL containing an uploaded file, LSD Server will make the file available as a static resource and will update the platform's info field to reference it.  If a string starting "http" is PUT, then this will be stored and clients accessing in the future via GET will be redirected to the referenced site

### Allowed HTTP verbs
* GET
* PUT
* DELETE

## Platform location
[/platform/\<platform_id\>/location/]()

Get WKT _point_ for the platform's location.  We don't handle moving platforms yet.  In the future this could endpoint could return a linestring or a polygon.

### Allowed HTTP verbs
* GET

## Filtering the platform list

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
* GET

# Sensors
A sensor is a device which is associated with a platform and records one or more parameters.

## Fields
* manufacturer (string, mandatory)
* model (string, mandatory)
* serial number (string, mandatory)
* description (string)
* info (string, a relative or absolute URL)

## JSON transport format
```
{
  "manufacturer": "sensor_manufacturer",
  "model": "sensor_model",
  "serial_number": "sensor_serial_number",
  "description": "sensor_description",
  "info": "http://..."
}
```
## Listing sensors associated with a platform
[/sensor/\<platform_id\>]()

### Allowed HTTP verbs
* GET

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
[/sensor/\<platform_id\>/?sensor_model=tm302]()

### Allowed HTTP verbs
* GET

## Creating, reading, updating or deleting a sensor
Sensors are identified by the natural key of:
* manufacturer
* model
* serial number
and MUST be associated with a platform

[/sensor/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>]()

### Allowed HTTP verbs
* GET
* PUT
* DELETE

## Sensor metadata (info)
[/sensor/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>/info]()

You can obtain the metadata for a sensor (if available) via this URL.  LSD Server will send a 302 redirect request to the user's browser with the real location of the info resource.

If a PUT request is made to this URL containing an uploaded file, LSD Server will make the file available as a static resource and will update the sensor's info field to reference it.  If a string starting "http" is PUT, then this will be stored and clients accessing in the future via GET will be redirected to the referenced site

### Allowed HTTP verbs
* GET
* PUT
* DELETE

# Parameters
Parameters are phenomena measured by sensors which are attached to platforms.  Many sensors measure more then one parameter which is why this mechanism is needed.

## Fields
* phenomena (string, URI referencing the phenomena this parameter measures *or* an integer referencing a definition hosted in this server)

## JSON transport format
```
{
  "phenomena": "http://..."
}
```

## Listing parameters associated with a sensor
[/parameter/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>]()

### Allowed HTTP verbs
* GET

## Creating, reading, updating or deleting a parameter
Parameters are identified by the natural key of:
* manufacturer
* model
* serial number
* phenomena
and MUST be associated with a platform AND a sensor

[/parameter/\<platform_id\>/\<manufacturer\>/\<model\>/\<serial number\>/\<phenomena\>]()

### Allowed HTTP verbs
* GET
* PUT
* DELETE

# Phenomena
Phenomena describe the physical conditions being measured by a parameter.  There are several built-in phenomena which are described on-line at http://lsdserver.com/phenomena

Users are able to reference the phenomena by supplying a phenomena URI for the phenomena field when registering a parameter with LSD Server.

Alternatively, users may define their own phenomena and reference them by URI when registering parameters.

TODO built in support for stuff like images, videos, mp3 etc

## List all phenomena
[/phenomena]()

## Fields
* term (string, mandatory)
* data_type (string, mandatory, identifies the data type, eg  double)
* min_valid (double, minimum valid value for this phenomena)
* max_valid (double, maximum valid value for this phenomena)
* uom (string, freetext identifying unit of measure)
* description (string, freetext for notes)

# JSON transport format
```
{
  "data_type": "phenomena_data_type",
  "min_valid": 0,
  "max_valid": 0,
  "uom": "phenomena_uom",
  "description": "phenomena_description"
}
```

### Allowed HTTP verbs
* GET

## Creating, reading, updating or deleting a phenomena
Phenomena are identified by their `term` which should be a URI pointing outside of the LSD Server system.

[/phenomena/\<term\>]()

### Allowed HTTP verbs
* GET
* PUT
* DELETE


# Flags
Flags are marks applied to individual observations.  Built-in flags are described at http://lsdserver.com/flags.  Users may also define and reference their own flags.

## Fields
* term (string, mandatory, ideally a URI)
* description (string, freetext for notes)

## list all flags
[/flag]()

## Creating, reading, updating or deleting a flag
Flags are identified by their `term` which should be a URI pointing outside of the LSD Server system.

[/flag/\<term\>]()

### Allowed HTTP verbs
* GET
* PUT
* DELETE


# Observations
Observations are individual measurements stored for each parameter on each sensor on each platform.

An observation typically comprises:
* timestamp (UTC)
* value
* flags

# JSON transport format
```
{
  "timestamp": 0,
  "value": 0.0d,
  "flag": [
    "http://...",
    "http://..."
  ]
}
```

## Creating, reading, updating or deleting an observation
Observations are uniquely identified by the combination of:
* platform_id
* sensor_manufacturer
* sensor_model
* sensor_serial_number
* phenomena
LSD Server uses this combination of facts to identify the correct place to store observations for a given parameter.

When creating observations, the timestamp may be omitted and LSD Server will use the current system time.  This is to support systems which do not have an RTC.

[/observation/\<platform_id\>/\<sensor_manufacturer\>/\<sensor_model\>/\<sensor_serial_number\>/\<phenomena\>]()

### Allowed HTTP verbs
* GET
* PUT
* DELETE

## latest observations from platform
[/observation/\<platform_id\>]()

### Allowed HTTP verbs
* GET

## latest observations from sensor
[/observation/\<platform_id\>\<sensor_manufacturer\>/\<sensor_model\>/\<sensor_serial_number\>]()

### Allowed HTTP verbs
* GET


# Notes
* Complex metadata should be stored outside of LSD Server, there are specialist systems available to do this such as [GeoNetwork](http://geonetwork-opensource.org/) or you could just reference a  static web page
