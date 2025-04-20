# Android Pattern Lock Decoder
![ChatGPT Image Apr 20, 2025, 09_49_32 PM](https://github.com/user-attachments/assets/971a124c-cc25-41ec-ad99-81ce617a86a9)

## Overview
Android's pattern lock allows users to unlock their devices by connecting at least four points on a 3x3 grid. Each point can only be used once, with a maximum of nine points. Internally, Android stores this pattern as a byte sequence, mapping each point to an index (0 to 8), where:
- `0` represents the top-left point.
- `8` represents the bottom-right point.

Unlike a standard PIN lock, which can use any digit from 0 to 9, the pattern lock is limited to these nine distinct points. Additionally, some sequences are restricted (e.g., directly connecting point `1` to `9` without touching `5`). This reduces the total number of possible pattern combinations compared to a traditional numeric PIN.

### Pattern Hash Storage
Android stores the **SHA-1 hash** of the pattern in one of the following locations:
```
/data/system/gesture.key
/data/system/users/<user-id>/gesture.key (for multi-user devices)
```
This hash is stored **without a salt**, meaning that the same pattern always results in the same SHA-1 hash. As a result, precomputed hash tables can be used to quickly retrieve patterns, making them vulnerable to dictionary attacks.

Since the `gesture.key` file is owned by the system user with default permissions set to `0600`, retrieving it from a non-rooted device is generally not possible.

---
## Usage
To use the **Android Pattern Lock Decoder**, run the following command:
```bash
python3 androunlock.py -g <gesture.key> -d <dictionary file>
```
This script attempts to recover the pattern lock by comparing the stored SHA-1 hash against a dictionary of precomputed hashes.

### Command-Line Options:
```
-h, --help            Show this help message and exit
-g, --gesture         Path to the gesture.key file on your system
-d, --dictionary      Path to the dictionary file containing SHA-1 hashes
```

---
## Example Usage
### 1. Extracting `gesture.key`
First, copy the `gesture.key` file from an Android device:
```bash
adb pull /data/system/gesture.key .
```
Since the file is protected, this step requires root access.

### 2. Viewing the `gesture.key` File
To inspect the contents of the `gesture.key` file, use the `od` tool or a hex editor (e.g., `xxd`, `ghex`, or `HxD`):
```bash
$ od -t x1 res/gesture.key 
0000000   21  69  de  4f  e6  5b  c2  46  78  0d  72  6a  e1  c2  5c  5b
0000020   fc  51  5a  5d
0000024
```

### 3. Decoding the Pattern
Use the **androunlock.py** script with a hash table to retrieve the pattern:
```bash
$ python3 androunlock.py -g res/gesture.key -d res/androidpatternsha1.txt
[+] Pattern retrieved from gesture.key file is: 3214789
```
This means the user’s unlock pattern is **3 → 2 → 1 → 4 → 7 → 8 → 9**.

---
## Notes
- The script requires a dictionary file containing precomputed SHA-1 hashes of all possible patterns.
- The **gesture.key** file must be obtained from the device (which usually requires root access).
- This method works because Android does not use a salt when hashing pattern locks.
