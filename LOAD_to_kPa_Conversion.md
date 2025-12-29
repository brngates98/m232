# LOAD to kPa Conversion Guide

## Overview

The Motronic 2.3.2 ECU uses an internal "LOAD" value (0-255) to represent manifold absolute pressure (MAP). This guide explains how to convert between LOAD values and kPa (kilopascals).

## Conversion Formula

The conversion from LOAD to kPa depends on the MAP sensor type configured in the ECU:

```
kPa = (LOAD × factor) + offset
```

Where `factor` and `offset` are determined by the MAP sensor type.

## MAP Sensor Types

The MAP sensor type is stored at address **0x48** in the bin file:

| Type | Sensor Model | Max Pressure | Factor | Offset |
|------|-------------|--------------|--------|---------|
| 1 | Bosch 0 273 003 210 | 250 kPa | 0.9804 (50/51) | 10.0 |
| 2 | Bosch 0 273 003 211 | 300 kPa | 1.2918 (65.88235/51) | -6.35764 |
| 3 | Motorola MPXH6300A | 300 kPa | 1.2332 (62.89308/51) | 0.222013 |
| 4 | Motorola MPXH6400A | 400 kPa | 1.6198 (82.61049/51) | 6.9558 |

## Examples

### Example 1: Type 1 Sensor (250 kPa)
For MAP sensor type 1, with LOAD values from the stock tune at 0x8D23:

| LOAD | Calculation | kPa |
|------|------------|-----|
| 17 | (17 × 0.9804) + 10 | 26.7 |
| 26 | (26 × 0.9804) + 10 | 35.5 |
| 34 | (34 × 0.9804) + 10 | 43.3 |
| 162 | (162 × 0.9804) + 10 | 168.8 |

### Example 2: Type 4 Sensor (400 kPa)
For MAP sensor type 4, with the same LOAD values:

| LOAD | Calculation | kPa |
|------|------------|-----|
| 17 | (17 × 1.6198) + 6.9558 | 34.5 |
| 26 | (26 × 1.6198) + 6.9558 | 49.1 |
| 34 | (34 × 1.6198) + 6.9558 | 62.0 |
| 162 | (162 × 1.6198) + 6.9558 | 269.2 |

## LOAD Axis Locations

The following tables in the XDF contain LOAD axis data and have been updated to display kPa values:

| Table Name | Address | Elements | Description |
|------------|---------|----------|-------------|
| Fuel enrichment - P/T - LOAD (kPa) | 0x8E03 | 16 | LOAD axis for fuel enrichment partial throttle tables |
| Ignition - P/T - LOAD (kPa) | 0x924F | 16 | LOAD axis for ignition partial throttle tables |
| 0x8D21 - 4x1 - Load (kPa) | 0x8D23 | 4 | LOAD axis used in boost control |
| 0x8D44 - 4x1 - Load (kPa) | 0x8D46 | 4 | LOAD axis used in wall film enrichment |
| 0xA188 - 6x1 - Load (kPa) | 0xA18A | 6 | LOAD axis used in various tables |

## XDF Implementation

The XDF file has been updated with the following changes:

1. **Added units**: Each LOAD axis Z-axis now includes `<units>kPa</units>`
2. **Added conversion formula**: The MATH equation now references the MAP sensor type constants:
   ```xml
   <MATH equation="(X*THAT(8754;0;0;FALSE)) + THAT(18181;0;0;FALSE)">
   ```
   Where:
   - `THAT(8754;0;0;FALSE)` = MAP sensor factor constant (uniqueid 0x2232)
   - `THAT(18181;0;0;FALSE)` = MAP sensor offset constant (uniqueid 0x4705)

3. **Updated titles**: Table titles now include "(kPa)" to indicate the displayed units

## Reverse Conversion (kPa to LOAD)

To convert from kPa back to LOAD:

```
LOAD = (kPa - offset) / factor
```

## Notes

- The conversion is dynamic based on the MAP sensor type setting at address 0x48
- When you change the MAP sensor type in the bin file, all LOAD axis values will automatically display the correct kPa values
- The raw LOAD values (0-255) in the bin file remain unchanged; only the display values change
- These LOAD axes are used as reference axes in various tuning tables (fuel, ignition, boost control, etc.)
