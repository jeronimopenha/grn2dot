# grn2dot

A small conversor for gnr format to networkx graphs and dot language

## To install

pip install git+https://github.com/jeronimopenha/grn2dot.git

# Simple usage example

from grn2dot.grn2dot import Grn2dot

grn2dot = Grn2dot("./grn_benchmarks/Benchmark_70.txt")
print(grn2dot.get_dot_str())
