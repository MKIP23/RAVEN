from m5.objects import *
from m5.util import *
from gem5.components.boards.riscv_board import RiscvBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource, DiskImageResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
import argparse
import shutil
import m5

# --------------------------
# Command-line arguments
# --------------------------
parser = argparse.ArgumentParser()

parser.add_argument(
    "--image",
    type=str,
    required=True,
    help="Input the full path to the built spec-2017 disk-image.",
)
parser.add_argument("--checkpoint", type=str,
                   help="Path to checkpoint directory for restoration")

args = parser.parse_args()

# --------------------------
# ISA check
# --------------------------
requires(isa_required=ISA.RISCV)

# --------------------------
# System setup
# --------------------------
cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
    l1d_size="32KiB", l1i_size="32KiB", l2_size="512KiB"
)
memory = SingleChannelDDR3_1600()
processor = SimpleProcessor(
    cpu_type=CPUTypes.O3, isa=ISA.RISCV, num_cores=1
)
board = RiscvBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
board.set_kernel_disk_workload(
    kernel=obtain_resource("riscv-bootloader-vmlinux-5.10"),
    disk_image=DiskImageResource(local_path=args.image),
)
# --------------------------
# Simulation: restore or run
# --------------------------
if args.checkpoint:
    print(f"🔁 Restoring from {args.checkpoint}")
    simulator = Simulator(board=board, 
                          checkpoint_path=args.checkpoint)
else:
    simulator = Simulator(board=board)   
# --------------------------
# Custom Time Profiled stats
# --------------------------
# m5.stats.addStatVisitor("text://stats_mk.txt")
# m5.stats.addStatVisitor('h5://stats_mk.h5?formulas=True')
# m5.stats.dump()
# # Schedule stats dump every 0.1 simsecond
# m5.stats.periodicStatDump(10**11)
# # Now run the simulation
# print("Beginning simulation!")
simulator.run(2*10**12)
#simulator.run()
#/sbin/m5 checkpoint

# # Clear existing visitors (e.g., default stats.txt)
# m5.stats.stat_visitors = []
#print("Dumping!")