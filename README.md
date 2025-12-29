# m232
Motronic 2.3.2 tuning suite

## Features

### LOAD to kPa Conversion
The XDF file now automatically converts LOAD axis values (0-255) to kPa (kilopascals) based on the configured MAP sensor type. This makes it easy to understand actual manifold pressure values when tuning.

**Example**: LOAD value 162 displays as 269.4 kPa with a 400kPa MAP sensor.

See [LOAD_to_kPa_Conversion.md](LOAD_to_kPa_Conversion.md) for complete documentation.
