# XDF Processing Tools

This directory contains tools for working with TunerPro XDF (eXtensible Definition Format) files to analyze and document ECU firmware.

## Overview

The XDF file (`TunerPro/m232.xdf`) contains definitions for tuning parameters in the Motronic 2.3.2 firmware, including:
- **136 tables** - Multi-dimensional maps for fuel, ignition, boost, etc.
- **70 constants** - Single values like injector sizes, RPM limits, etc.
- **193 unique addresses** - Memory locations mapped to parameters

## Tools

### 1. parse_xdf.py
Parse and display XDF file contents.

```bash
python3 parse_xdf.py TunerPro/m232.xdf
```

**Output:**
- Summary of categories, tables, and constants
- All definitions sorted by memory address
- Parameter names, sizes, units, and equations

### 2. annotate_asm.py
Add XDF labels as comments to assembly files.

```bash
python3 annotate_asm.py TunerPro/m232.xdf decompiled/stock_AANABY_27c512.asm
```

**Creates:**
- Annotated assembly file with XDF parameter names at each address
- Comments showing table sizes, units, and equations
- Makes assembly code much easier to understand

**Example output:**
```asm
; === XDF: Address 0x8D09 ===
; Max calculated load [4x1]
	db 100  ; [8D09h]
	db 245  ; [8D0Ah]
	db 245  ; [8D0Bh]
	db 245  ; [8D0Ch]

; === XDF: Address 0x8377 ===
; Injector minimum pulsewidth (ms)
	db 5    ; [8377h]
```

### 3. extract_xdf_data.py
Extract tuning data from binary files to CSV/text format.

```bash
python3 extract_xdf_data.py TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin xdf_extracted/
```

**Creates:**
- CSV files for each table with raw data values
- Text files for each constant with calculated values
- Organized in output directory

**Example files:**
- `Max_calculated_load_0x8D09.csv` - Table data in CSV format
- `Injector_minimum_pulsewidth_0x8377.txt` - Constant with equation results

### 4. process_xdf.py
Master script combining all functionality.

```bash
# Annotate assembly only
python3 process_xdf.py --annotate TunerPro/m232.xdf decompiled/stock_AANABY_27c512.asm

# Extract data only
python3 process_xdf.py --extract TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin

# Do both
python3 process_xdf.py --all TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin decompiled/stock_AANABY_27c512.asm
```

## Quick Start

### Annotate All Assembly Files
```bash
for asm in decompiled/*.asm; do
    python3 annotate_asm.py TunerPro/m232.xdf "$asm" "decompiled/annotated_$(basename $asm)"
done
```

### Extract Data from All Binaries
```bash
for bin in ECU/*.bin; do
    name=$(basename "$bin" .bin)
    python3 extract_xdf_data.py TunerPro/m232.xdf "$bin" "xdf_extracted/$name"
done
```

### Compare Stock vs Big Turbo Tables
```bash
# Extract both
python3 extract_xdf_data.py TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin xdf_extracted/stock
python3 extract_xdf_data.py TunerPro/m232.xdf ECU/bigturbo_WMI_27c512.bin xdf_extracted/bigturbo

# Compare fuel table
diff xdf_extracted/stock/Fuel_enrichment_-_PT_0x8E00.csv \
     xdf_extracted/bigturbo/Fuel_enrichment_-_PT_0x8E00.csv
```

## XDF File Structure

### Tables (XDFTABLE)
Tables are multi-dimensional maps with:
- **Title**: Descriptive name (e.g., "Fuel enrichment - P/T")
- **Address**: Memory location (e.g., 0x8E00)
- **Size**: Dimensions (e.g., 16x16)
- **Units**: Measurement units (e.g., "ms", "deg", "rpm")
- **Categories**: Organization tags (Fueling, Ignition, Boost control, etc.)

### Constants (XDFCONSTANT)
Constants are single values with:
- **Title**: Descriptive name
- **Address**: Memory location
- **Units**: Measurement units
- **Equation**: Conversion formula (e.g., "X*40" for RPM)
- **Calculated Value**: Result of applying equation to raw value

### Categories
The XDF defines 20 categories:
- 27C512, 87C257 - ROM chip types
- MAF Linearization, Fueling, Ignition - Functional groups
- Boost control, Knock control, Lambda control - Control systems
- RPM limits, Load limits, Injectors - Configuration parameters
- Stock, Patches, Fast diag - Special features

## Tuning Parameters

### Key Tables
- **Fuel enrichment - P/T** (0x8E00): Main fuel map [16x16]
- **Ignition - P/T** (0x925F): Ignition timing map [16x16]
- **Target boost** (various): Boost pressure targets
- **Knock detection threshold** (0x2218+): Knock sensor sensitivity per cylinder

### Key Constants
- **Injector constant** (0x8399): Injector flow rate
- **Injector minimum pulsewidth** (0x8377): Dead time
- **RPM limits**: Rev limiter, NLS/launch control settings

## Technical Notes

### Binary File Compatibility
- **27c512 variants** (64KB): All XDF addresses work
- **87c257 variants** (32KB): Only addresses below 0x8000 work
- The XDF is primarily designed for 27c512 (64KB) firmware

### Address Format
- XDF uses hex format: `0x8D09`
- Assembly uses hex with 'h' suffix: `8D09h`
- Tools handle both formats automatically

### Equation Evaluation
For constants with equations, tools attempt to calculate real values:
- `X*40` where X=50 → 2000 RPM
- `X/10` where X=5 → 0.5 ms
- `360/(X/128)` - Injector flow calculation

## Integration with Decompilation

The XDF tools complement the assembly decompilation:

1. **Decompile firmware** → Get assembly code with all instructions
2. **Annotate with XDF** → Add parameter names to assembly
3. **Extract data tables** → Get tuning values in readable format
4. **Compare versions** → Diff to see tuning changes

This provides three views of the same firmware:
- **Binary**: Raw data (.bin files)
- **Assembly**: Instructions and code flow (.asm files)
- **Tables**: Tuning parameters (CSV/text files)

## References

- TunerPro RT: https://www.tunerpro.net/
- XDF Format: eXtensible Definition Format for ROM editing
- Motronic 2.3.2: Bosch ECU for Audi AAN/ABY 5-cylinder turbo engines

## Credits

- XDF file: prj (original author)
- XDF parsing tools: This repository
- TunerPro RT: Mark Mansur
