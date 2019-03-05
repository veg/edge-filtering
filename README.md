# edge-filtering
Edge Filtering with HIV-TRACE

# Possible metrics to use to describe effectiveness 
- Global Clustering Coefficient - measures the total number of closed triangles in a network

# Running on a cluster
`snakemake --cluster "qsub -l nodes=1:ppn=4 -l walltime=5:00:00 -q datamonkey" -j 100`
