# LSDServer API

## entry point
[/]()


##platforms

[/platform/]()
List all platforms

[/platform/\<platform_id\>/]()
CRUD platform (container)

[/platform/\<platform_id\>/info]()
[/platform/\<platform_id\>/info/\<redirection_uri\>]()
CRUD Platform metadata resource URL OR post HTML/XML *FILE*

[/platform/\<platform_id\>/location/]()

[/platform/\<platform_id\>/location/\<lon,lat,epsg,timestamp\>]()
CRUD platform location info

[/platform/?filter=sensor_id,tm3002]()
find what platform sensor tm3002 is attached to
[/platform/?filter=location]()

_platforms within platforms -- possible but not supported yet_

## phenomena
[/phenomena]()
List all phenomena

[/phenomena/\<term,type,uom,definition\>]()
CRUD term to definition (URI or plaintext).  Once a phenomena is defined it
    can be assigned to a sensor
        term - eg temperature
        type - eg float
        uom - eg celcius
        definition - eg URI with more info

    TODO built in support for stuff like images, videos, mp3 etc

## Quality
[/quality]()
list all quality flags

[/quality/\<value, defintion\>]()
CRUD a quality marker


## sensors
[/sensor/\<platform_id\>/\<sensor_id\>]()
CRUD sensor container

[/sensor/\<platform_id\>/\<sensor_id\>/info]()
CRUD sensor metadata URI OR post HTML/XML *FILE*

[/sensor/\<platform_id\>/\<sensor_id\>/\<phenomena_id\>]()
CRUD sensor measured phenomena

[/sensor/?phenomena=temperature]()
query list of sensors that measure temperature

## observations
[/observation/\<platform_id\>]()
latest observations from platform

[/observation/\<platform_id\>/\<sensor_id\>]()
latest observations from sensor

[/observation/?phenomena=temperature]()
latest observations of temperature

[/observation/\<platform_id\>/\<sensor_id\>/\<ts,value,quality\>]()
CRUD an observation value
