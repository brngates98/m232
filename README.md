# m232
Motronic 2.3.2 tuning suite

## Decompiled Firmware

The ECU firmware binary files have been decompiled to 8051 assembly language. See the `decompiled/` directory for:
- Assembly source files (.asm) for all firmware variants
- Detailed documentation about the processor architecture and decompilation process

To regenerate the decompiled files, run:
```bash
python3 decompile.py
```

## XDF Processing Tools

Tools for working with TunerPro XDF definitions to analyze and document the firmware:

- **annotate_asm.py** - Add XDF parameter labels to assembly files
- **extract_xdf_data.py** - Extract tuning tables/constants to CSV/text
- **parse_xdf.py** - Parse and display XDF file contents
- **process_xdf.py** - Master script for all XDF operations

See [XDF_TOOLS.md](XDF_TOOLS.md) for complete documentation and examples.

**Quick examples:**
```bash
# Annotate assembly with tuning parameter names
python3 annotate_asm.py TunerPro/m232.xdf decompiled/stock_AANABY_27c512.asm

# Extract all tuning tables to CSV files
python3 extract_xdf_data.py TunerPro/m232.xdf ECU/stock_AANABY_27c512.bin xdf_extracted/
```

## Repository Structure

- `ECU/` - Binary firmware files (stock and big turbo variants)
- `decompiled/` - Decompiled 8051 assembly code
- `TunerPro/` - TunerPro XDF definition file and logging config
- `src/` - Source code for checksum plugins and IDA databases
- `WinLog/` - WinLog related files
- `Factory data/` - Factory calibration data
