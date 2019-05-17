for i in {200..220}
do
  bpsh 8 snakemake --quiet --config chain_size=8 seed=p$i -j 500 &
done

for i in {221..240}
do
  bpsh 6 snakemake --quiet --config chain_size=8 seed=p$i -j 500 &
done

for i in {241..250}
do
  bpsh 7 snakemake --quiet --config chain_size=8 seed=p$i -j 500 &
done
