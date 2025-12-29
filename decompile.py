#!/usr/bin/env python3
"""
Decompile Motronic 2.3.2 ECU bin files to assembly
This script uses disasm51 to decompile 8051 firmware binaries
"""

import os
import sys
import subprocess
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ECU_DIR = SCRIPT_DIR / "ECU"
DECOMPILED_DIR = SCRIPT_DIR / "decompiled"
MCU_FILE = SCRIPT_DIR / "sab80c515.mcu"
DISASM_SCRIPT = SCRIPT_DIR / "disasm51.py"

# Bin files to decompile
BIN_FILES = [
    "stock_AANABY_27c512.bin",
    "stock_AANABY_87c257.bin",
    "bigturbo_WMI_27c512.bin",
    "bigturbo_WMI_87c257.bin",
]

def decompile_bin(bin_path, output_path, mcu_file):
    """Decompile a single bin file using disasm51"""
    print(f"Decompiling {bin_path.name}...")
    
    # Command to run disasm51
    cmd = [
        sys.executable,
        str(DISASM_SCRIPT),
        "--include", str(mcu_file),
        "--entry", "RESET",  # Start from reset vector
        str(bin_path)
    ]
    
    try:
        # Run disasm51 and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Write output to file
        with open(output_path, 'w') as f:
            f.write(result.stdout)
        
        # Also capture warnings/errors if any
        if result.stderr:
            warning_file = output_path.with_suffix('.log')
            with open(warning_file, 'w') as f:
                f.write(result.stderr)
            print(f"  Warnings written to {warning_file.name}")
        
        print(f"  Successfully decompiled to {output_path.name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  Error decompiling {bin_path.name}: {e}")
        print(f"  stderr: {e.stderr}")
        return False

def main():
    """Main function to decompile all bin files"""
    print("=" * 60)
    print("Motronic 2.3.2 ECU Firmware Decompiler")
    print("Target Processor: Siemens SAB80C515 (8051 family)")
    print("=" * 60)
    print()
    
    # Ensure directories exist
    if not ECU_DIR.exists():
        print(f"Error: ECU directory not found: {ECU_DIR}")
        return 1
    
    DECOMPILED_DIR.mkdir(exist_ok=True)
    
    # Check if MCU file exists
    if not MCU_FILE.exists():
        print(f"Error: MCU definition file not found: {MCU_FILE}")
        return 1
    
    # Check if disasm script exists
    if not DISASM_SCRIPT.exists():
        print(f"Error: disasm51.py not found: {DISASM_SCRIPT}")
        return 1
    
    # Decompile each bin file
    success_count = 0
    for bin_file in BIN_FILES:
        bin_path = ECU_DIR / bin_file
        
        if not bin_path.exists():
            print(f"Warning: {bin_file} not found, skipping...")
            continue
        
        # Create output filename
        output_name = bin_file.replace('.bin', '.asm')
        output_path = DECOMPILED_DIR / output_name
        
        if decompile_bin(bin_path, output_path, MCU_FILE):
            success_count += 1
        print()
    
    # Summary
    print("=" * 60)
    print(f"Decompilation complete: {success_count}/{len(BIN_FILES)} files processed")
    print(f"Output directory: {DECOMPILED_DIR}")
    print("=" * 60)
    
    return 0 if success_count > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
