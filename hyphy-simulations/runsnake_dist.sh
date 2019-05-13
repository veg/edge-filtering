for i in {1..12}
do
  bpsh 8 /home/sweaver/programming/hivtrace/edge/bin/python3.6 /home/sweaver/programming/hivtrace/edge/bin/snakemake -s SnakefileDistribution --config chain_size=8 seed=r$i -j 500 &
done

for i in {21..40}
do
  bpsh 6 /home/sweaver/programming/hivtrace/edge/bin/python3.6 /home/sweaver/programming/hivtrace/edge/bin/snakemake -s SnakefileDistribution --config chain_size=8 seed=r$i -j 500 &
done

for i in {41..100}
do
  bpsh 7 /home/sweaver/programming/hivtrace/edge/bin/python3.6 /home/sweaver/programming/hivtrace/edge/bin/snakemake -s SnakefileDistribution --config chain_size=8 seed=r$i -j 500 &
done
