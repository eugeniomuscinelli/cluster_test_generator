# Generating a Stimuli Header for PULP Program Execution on ESP
This document outlines the **sub-process** required to generate a C header file containing the binary and instruction data of a PULP program, tailored to be executed by the **PULP cluster within the ESP platform**. This process modifies parts of the `pulp_cluster` repository to match ESP's memory map and creates the appropriate stimuli header file for loading the program onto the cluster.

---

## 1. Clone the PULP Cluster Repository

First, clone the official [`pulp_cluster`](https://github.com/pulp-platform/pulp_cluster) repository:

```bash
git clone https://github.com/pulp-platform/pulp_cluster.git
cd pulp_cluster
```

Follow the repository's README **up to this step (included)**, including:

```bash
make regression-tests
make pulp-runtime
```


---

## 2. Modify the Memory Map and Linker Script for ESP

ESP maps the cluster L2 memory into a specific address range. To ensure compatibility, modify both the memory map and linker script.

### Modify `memory_map.h`

File location:  
`pulp_cluster/pulp-runtime/include/archi/chips/astral-cluster/memory_map.h`

Update these lines:

```c
#define ARCHI_L2_PRIV0_ADDR  0x78000000
#define ARCHI_L2_PRIV1_ADDR  0x78008000
#define ARCHI_L2_SHARED_ADDR 0x78000000
```

Accordingly to the base address reserved to the cluster into the ESP memory tile (usually `0xA0103680`).


### Modify `link.ld`

File location:  
`pulp_cluster/pulp-runtime/kernel/chips/astral-cluster/link.ld`

Change:

```ld
MEMORY
{
  L2           : ORIGIN = 0x78000000, LENGTH = 0x00020000
  L1           : ORIGIN = 0x50000000, LENGTH = 0x0003FFFC
}
```
Since the L2 is mapped into the ESP memory tile, the origin of it must be once again changed accordingly.

## 3. Build the Target Test Binary

Now that memory map and linker script have been changed, source the appopriate envorinment (astral in this case):

```bash
source env/astral-env.sh
```

Navigate to the appropriate test folder, depending on the test case:

```bash
cd pulp_cluster/regression-tests/<your_test_folder>
```

Then build:

```bash
make clean all
```

This produces the test binary (`.bin` file) needed for stimuli generation.

---

## 4. Generate JTAG Stimuli File

Use the `stim_utils.py` script to convert the binary into a `.txt` vector file:

```bash
<path_to_pulp_cluster>/pulp_cluster/pulp-runtime/bin/stim_utils.py \
  --binary=<path_to_executable> \
  --vectors=<output_folder>/<stimuli_file_name>.txt
```

Replace:
- `<path_to_executable>` with the path to the generated `.bin` file.
- `<stimuli_file_name>` with your desired name for the output file.

---

## 5. Generate the Final C Header File

To convert the `.txt` file into a header file suitable for ESP integration:

```bash
python <path_to_generate_stimuli_script>/generate_padded_stimuli.py <stimuli_file_name>.txt
```

This produces a `.h` file formatted for memory-mapped loading on the PULP cluster via ESP.

