from math import pi


class WindTurbine:
    def __init__(self, model_name, height, swept_area):
        self.MODEL_NAME = model_name
        self.HEIGHT = height
        self.SWEPT_AREA = swept_area

    def calc_coefficient_performance(self, wind_speed):
        """
        :param wind_speed: metre/second
        :return: co-efficient of performance based on power curve of a different model of wind turbine

        Source: https://en.wind-turbine-models.com/turbines/1116-aerodyn-scd-8.0-168
        """
        COEFFICIENT_OF_PERFORMANCE = [0.0, 0.0, 0.0, 0.0, 0.1156, 0.2961, 0.3427, 0.4316, 0.4337, 0.4061, 0.3701,
                                      0.3337, 0.3212, 0.2695, 0.2158, 0.1754, 0.1446, 0.1205, 0.1015, 0.0863, 0.074,
                                      0.0639, 0.0556, 0.0487, 0.0428, 0.0379]

        # If the wind speed is less that cut-in speed (3m/s) or higher than cut-off speed (25m/s)
        # no the coefficient of power is 0.
        if wind_speed < 3 or wind_speed > 25:
            return 0.0
        else:
            return COEFFICIENT_OF_PERFORMANCE[wind_speed]

    def calc_air_density(self, air_pressure, air_temperature, relative_humidity):
        """
        Calculates the air density given the values for air pressure, air temperature and relative humidity.
        :param air_pressure:        unit: pascal
        :param air_temperature:     unit: Kelvin
        :param relative_humidity:   unit: N/A (ratio)
        :return: air_density calculated to 3 digits of precision.
        """
        DRY_AIR_SPECIFIC_GAS_CONSTANT = 287.058
        WATER_SPECIFIC_GAS_CONSTANT = 461.495

        saturation_vapor_pressure = 6.1078 * \
            10 ** (7.5 * air_temperature / (air_temperature + 237.3))
        water_vapor_pressure = saturation_vapor_pressure * relative_humidity
        dry_air_pressure = air_pressure - water_vapor_pressure
        air_density = (dry_air_pressure / (DRY_AIR_SPECIFIC_GAS_CONSTANT * air_temperature)) + \
                      (water_vapor_pressure /
                       (WATER_SPECIFIC_GAS_CONSTANT * air_temperature))
        air_density = round(air_density, 3)
        return air_density

    def calc_wind_turbine_power(self, air_pressure, air_temperature, relative_humidity, wind_speed):
        """
            :param air_pressure:        unit: pascal
            :param air_temperature:     unit: Kelvin
            :param relative_humidity:   unit: N/A (ratio)
            :param wind_speed:          unit: metre/second
            :return: wind_turbine_power calculated to 3 digits of precision.
        """
        COEFFICIENT_OF_PERFORMANCE = self.calc_coefficient_performance(
            wind_speed)
        air_density = self.calc_air_density(
            air_pressure, air_temperature, relative_humidity)
        available_wind_power = 0.5 * air_density * \
            (wind_speed ** 3) * self.SWEPT_AREA
        # Some of the available power is lost due to inefficiences of the wind turbine.
        # This is compensated by the coefficient of performance (< 1).
        wind_turbine_power = round(
            COEFFICIENT_OF_PERFORMANCE * available_wind_power, 3)
        return wind_turbine_power
