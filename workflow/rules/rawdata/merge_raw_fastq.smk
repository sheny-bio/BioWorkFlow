"""将原始数据合并成R1和R2两个文件"""


rule merge_raw_fastq:
    input:
        R = lambda wildcards: FQ[wildcards.sample]
    output:
        R1 = "Results/{sample}/TEMP/RNARawFastq/{sample}.rna_R1.fastq.gz",
        R2 = "Results/{sample}/TEMP/RNARawFastq/{sample}.rna_R2.fastq.gz",
    params:
        rulename = "rna_fastq_merge",
    threads: 2
