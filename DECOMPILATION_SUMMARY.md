# Decompilation Summary

## Task Completed

All Motronic 2.3.2 ECU firmware binary files have been successfully decompiled to 8051 assembly language.

## What Was Done

### 1. Processor Identification
- Identified the ECU processor as **Siemens SAB80C515** (Intel 8051 family)
- Researched and documented processor specifications and SFR addresses

### 2. Decompilation Tooling
- Integrated **disasm51** - a professional Python-based 8051/8052 disassembler
- Created `sab80c515.mcu` - MCU definition file with all SFR mappings for the processor
- Developed `decompile.py` - automated decompilation script

### 3. Firmware Decompilation
Successfully decompiled all 4 firmware variants:
- `stock_AANABY_27c512.bin` → `stock_AANABY_27c512.asm` (64KB, 55,906 lines)
- `stock_AANABY_87c257.bin` → `stock_AANABY_87c257.asm` (32KB, 30,848 lines)
- `bigturbo_WMI_27c512.bin` → `bigturbo_WMI_27c512.asm` (64KB, 55,909 lines)
- `bigturbo_WMI_87c257.bin` → `bigturbo_WMI_87c257.asm` (32KB, 30,848 lines)

### 4. Documentation
- Created comprehensive README in `decompiled/` directory
- Updated main README with decompilation information
- Added inline comments and labels in assembly output
- Documented processor architecture and SFR definitions

### 5. Quality Assurance
- Verified assembly syntax correctness
- Confirmed proper interrupt vector labels (RESET, EXTI0, TIMER0, etc.)
- Validated jump targets and code flow
- Tested reproducibility of decompilation process
- Added `.gitignore` to exclude log files

## Output Files

### Decompiled Assembly Files
Located in `decompiled/` directory:
- 4 `.asm` files containing complete disassembled 8051 assembly code
- Human-readable with symbolic register names and interrupt vectors
- Can be reassembled with asem-51 or similar 8051 assemblers

### Supporting Files
- `disasm51.py` - Main disassembler script
- `addresses.py` - Address and label management
- `codeanalyzer.py` - Code flow analysis
- `instructions.py` - 8051 instruction definitions
- `utils.py` - Utility functions
- `sab80c515.mcu` - Processor definition file
- `decompile.py` - Automated batch decompilation script

## Key Features

### Proper Labels and Symbols
- Standard interrupt vectors (RESET, EXTI0, TIMER0, TIMER1, TIMER2, SINT)
- Jump targets labeled as `jump_XXXX`
- Data pointer references as `dptr_XXXX`
- SFR names (P0, P1, ACC, PSW, IE, IP, etc.)

### Assembly Quality
- Valid 8051 assembly syntax
- Includes MCU definition file
- Proper segment declarations (cseg)
- Address comments for data bytes
- Organization directives for proper memory layout

### Comparison Capability
- Enables direct comparison between stock and modified tunes
- Diff analysis shows specific data table and code changes
- Helps identify tuning modifications (fuel, ignition, boost control)

## Usage

### Regenerate Decompiled Files
```bash
python3 decompile.py
```

### View Assembly Code
```bash
# View any decompiled file
less decompiled/stock_AANABY_87c257.asm

# Compare stock vs. big turbo
diff -u decompiled/stock_AANABY_87c257.asm decompiled/bigturbo_WMI_87c257.asm
```

### Reassembly (Optional)
To reassemble back to binary:
```bash
# Using asem-51 (if installed)
asem stock_AANABY_87c257.asm
```

## Technical Notes

### Warnings
The log files contain warnings about some SFR addresses. These are benign:
- Disasm51 couldn't find symbolic names for all SFRs
- Hex addresses (e.g., `0E0h`) are used instead
- The disassembly is still correct and complete

### Architecture Details
- **CPU**: 8-bit CMOS microcontroller
- **Instruction Set**: Intel MCS-51
- **ROM Size**: 32KB (87c257) or 64KB (27c512)
- **Special Features**: Enhanced timers, ADC, DAC, extra I/O ports

## Benefits

1. **Human Readable**: Code can be analyzed and understood
2. **Modifiable**: Assembly can be edited for custom tuning
3. **Comparable**: Easy to compare different firmware versions
4. **Reproducible**: Script allows regeneration at any time
5. **Educational**: Learn ECU programming and tuning strategies

## Credits

- **disasm51** by Aleksander Mazur (Apache 2.0 License)
- **Processor Research**: Based on Siemens/Infineon SAB80C515 datasheets
- **ECU Platform**: Bosch Motronic 2.3.2

---
Generated: 2025-12-29
Status: ✅ Complete
