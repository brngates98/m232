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

## Repository Structure

- `ECU/` - Binary firmware files (stock and big turbo variants)
- `decompiled/` - Decompiled 8051 assembly code
- `src/` - Source code for checksum plugins and IDA databases
- `TunerPro/` - TunerPro definition files
- `WinLog/` - WinLog related files
- `Factory data/` - Factory calibration data
