class SampleData:

    """URI to use for /info redirection"""
    sample_uri = "http://www.lsdserver.com"

    sample_info = """
Sample Info
------------
This is some sample info, it will be created as a file and read back
    """

    """
    Platform
    """
    sample_platform_id = "myplatform_id"
    sample_platform = {
        "platform_id": sample_platform_id,
        "name": "platform_name",
        "description": "platform_description",
        "info": "http://link_for_more_info",
        "location": "POINT(0,0)"
    }

    """
    Sensor
    """
    sample_sensor_manufacturer = "sensor_manufacturer"
    sample_sensor_model = "sensor_model"
    sample_sensor_serial_number = "sensor_serial_number"
    sample_sensor = {
        "platform_id": sample_platform_id,
        "manufacturer": sample_sensor_manufacturer,
        "model": sample_sensor_model,
        "serial_number": sample_sensor_serial_number,
        "description": "sensor_description",
        "info": "http://..."
    }

    """
    Phenomena
    """
    sample_phenomena_term = "http://www.lsdserver.com/sample_term"
    sample_phenomena = {
        "term": sample_phenomena_term,
        "data_type": "phenomena_data_type",
        "min_valid": 0,
        "max_valid": 0,
        "uom": "phenomena_uom",
        "description": "phenomena_description"
    }

    """
    Parameter
    """
    sample_parameter = {
        "platform_id": sample_platform_id,
        "manufacturer": sample_sensor_manufacturer,
        "model": sample_sensor_model,
        "serial_number": sample_sensor_serial_number,
        "phenomena": sample_phenomena_term
    }

    """
    Observation
    """
    sample_observation = {
        "timestamp": 1434890106,
        "value": 10.0
    }
    sample_observation_with_flag = {
        "timestamp": 1434890106,
        "value": 10.0,
        "flag": [
            "http://...",
            "http://..."
        ]
    }