"""将原始数据合并成R1和R2两个文件"""



rule merge_raw_fastq:
    output:
        R1 = "Results/{sample}/MergeFastq/{sample}_R1.fastq.gz",
        R2 = "Results/{sample}/MergeFastq/{sample}_R2.fastq.gz",
    params:
        rulename = "merge_raw_fastq",
    threads: 1
    conda: "../envs/rna-seq-star-deseq2.yaml"
    shell:
        f"{{s_run_shell}} -j {{params.rulename}} -n {{wildcards.sample}} -c '"
        f"{scripts['merge_fq']} -r RawFastq -s {{wildcards.sample}} -o Results/{{wildcards.sample}}/MergeFastq"
        f"'"
