# Before and After Comparison

## What Changed

The LOAD axis tables now display actual manifold pressure in kPa instead of raw LOAD values.

## Visual Comparison

### Table: 0x8D21 - 4x1 - Load

**BEFORE (Raw LOAD values):**
```
Index  |  Value
-------|-------
  0    |   17
  1    |   26
  2    |   34
  3    |  162
```

**AFTER (kPa values with Type 4 sensor):**
```
Index  |  Value
-------|--------
  0    |  34.5 kPa
  1    |  49.1 kPa
  2    |  62.0 kPa
  3    | 269.4 kPa
```

---

### Table: 0x8D44 - 4x1 - Load

**BEFORE (Raw LOAD values):**
```
Index  |  Value
-------|-------
  0    |   15
  1    |   20
  2    |   70
  3    |  126
```

**AFTER (kPa values with Type 4 sensor):**
```
Index  |  Value
-------|--------
  0    |  31.3 kPa
  1    |  39.4 kPa
  2    | 120.3 kPa
  3    | 211.1 kPa
```

---

### Table: 0xA188 - 6x1 - Load

**BEFORE (Raw LOAD values):**
```
Index  |  Value
-------|-------
  0    |   10
  1    |   25
  2    |   40
  3    |   40
  4    |   50
  5    |   76
```

**AFTER (kPa values with Type 4 sensor):**
```
Index  |  Value
-------|--------
  0    |  23.2 kPa
  1    |  47.5 kPa
  2    |  71.7 kPa
  3    |  71.7 kPa
  4    |  87.9 kPa
  5    | 130.1 kPa
```

---

## Cross-Sensor Comparison

### Same LOAD value (162) with different MAP sensors:

| Sensor Type | Model | LOAD | kPa |
|------------|-------|------|-----|
| Type 1 | Bosch 250kPa | 162 | 168.8 kPa |
| Type 2 | Bosch 300kPa | 162 | 202.6 kPa |
| Type 3 | Motorola 300kPa | 162 | 200.0 kPa |
| Type 4 | Motorola 400kPa | 162 | **269.4 kPa** |

**Note**: The stock tune (stock_AANABY_27c512.bin) uses Type 4 sensor.

---

## Benefits

✅ **Immediate Understanding**: See actual manifold pressure values  
✅ **No Manual Conversion**: Values update automatically  
✅ **Sensor Type Aware**: Changes when you change sensor type  
✅ **Tuning Friendly**: Easier to correlate with boost gauge readings

---

## Technical Note

The raw LOAD values (0-255) in the bin file remain unchanged. Only the display values change in TunerPro when you open the XDF file. This ensures:

- ✓ Backward compatibility with existing tunes
- ✓ No data corruption risk
- ✓ Easy to revert if needed
- ✓ Works with any MAP sensor type

