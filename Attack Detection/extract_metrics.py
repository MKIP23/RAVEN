import os
import re

# Root folders containing stats
input_dirs = [
    "attack_stats_dir",
    "attack_stats_dir_test",
    "benign_stats_dir",
    "benign_stats_dir_test"
]

# Destination folder
output_base = "grepped"


# target_lines = [
#     # r"board\.cache_hierarchy\.l1icaches\.tags\.occupancies::processor\.cores\.core\.inst",
#     r"board\.cache_hierarchy\.l1icaches\.tags\.tagsInUse",
#     r"board\.cache_hierarchy\.l1dcaches\.LoadLockedReq\.misses::total",
#     # r"board\.cache_hierarchy\.l1dcaches\.LoadLockedReq\.missRate::processor\.cores\.core\.data",
#     r"board\.cache_hierarchy\.l1dcaches\.tags\.tagsInUse",
#     # r"board\.cache_hierarchy\.l1dcaches\.SwapReq\.mshrHits::total",
#     r"board\.processor\.cores\.core\.branchPred\.targetWrong_0::CallIndirect",
#     # r"board\.processor\.cores\.core\.mmu\.dtb\.readMisses",
#     # r"board\.processor\.cores\.core\.fpInstQueueWrites",
#     # r"board\.processor\.cores\.core\.fpAluAccesses",
#     # r"board\.processor\.cores\.core\.fpInstQueueReads"
# ]

target_lines = [
    r"board\.cache_hierarchy\.l1dcaches\.overallMisses::total",
    r"board\.processor\.cores\.core\.commit\.branchMispredicts",
    r"board\.processor\.cores\.core\.rob\.writes",
    r"board\.cache_hierarchy\.l1icaches\.overallMisses::total",  # If intentionally duplicated
]


# Compile regex patterns that match both integer and float values
patterns = [re.compile(rf"^\s*{line}\s+(\d+|\d+\.\d+)") for line in target_lines]

for input_dir in input_dirs:
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_base, input_dir, relative_path)

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(input_path, "r") as infile, open(output_path, "w") as outfile:
                    for line in infile:
                        # Check if any pattern matches the line
                        if any(pattern.search(line) for pattern in patterns):
                            outfile.write(line)