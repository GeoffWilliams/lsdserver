#!/bin/bash

SERVER=http://localhost:5000

PLATFORM='
{
  "platform_id": "platform_id",
  "name": "platform_name",
  "description": "platform_description",
  "info": "http://link_for_more_info",
  "location": "POINT(0,0)"
}'

SENSOR='{
  "platform_id": "platform_id",
  "manufacturer": "sensor_manufacturer",
  "model": "sensor_model",
  "serial_number": "sensor_serial_number",
  "description": "sensor_description",
  "info": "http://..."
}'

PARAMETER='{
  "platform_id": "platform_id",
  "manufacturer": "sensor_manufacturer",
  "model": "sensor_model",
  "serial_number": "sensor_serial_number",
  "phenomena": "phenomena"
}'

OBSERVATION='{
  "timestamp": 1437265024,
  "value": 11.1,
  "flag": [
    "http://...",
    "http://..."
  ]
}'
curl  -H 'Content-Type: application/json' -X PUT -d "$PLATFORM" "$SERVER/platform/platform_id"
curl  -H 'Content-Type: application/json' -X PUT -d "$SENSOR" "$SERVER/sensor/platform_id/sensor_manufacturer/sensor_model/sensor_serial_number"
curl  -H 'Content-Type: application/json' -X PUT -d "$PARAMETER" "$SERVER/parameter/platform_id/sensor_manufacturer/sensor_model/sensor_serial_number/phenomena"
curl  -H 'Content-Type: application/json' -X PUT -d "$OBSERVATION" "$SERVER/observation/platform_id/sensor_manufacturer/sensor_model/sensor_serial_number/phenomena"

