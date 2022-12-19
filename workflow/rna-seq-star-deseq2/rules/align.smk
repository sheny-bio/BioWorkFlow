rule align:
    input:
        R1="Results/{sample}/MergeFastq/{sample}_R1.fastq.gz",
        R2="Results/{sample}/MergeFastq/{sample}_R2.fastq.gz",
    output:
        "Results/{sample}/Align/{sample}-{unit}/Aligned.sortedByCoord.out.bam",
        "Results/{sample}/Align/{sample}-{unit}/ReadsPerGene.out.tab",
    log:
        "logs/star/{sample}-{unit}.log",
    params:
        index=lambda wc, input: input.index,
        extra="--outSAMtype BAM SortedByCoordinate --quantMode GeneCounts --sjdbGTFfile {} {}".format(
            "resources/genome.gtf", config["params"]["star"]
        ),
    threads: 24
    wrapper:
        "0.77.0/bio/star/align"