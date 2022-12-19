""" 数据质控，得到clean data
"""

rule preprocessing:
    """原始数据质控，得到HQ data"""

    input:
        R1 = merge_raw.fastq.output.R1,
        R2 = merge_raw.fastq.output.R2,
    output:
        R1 = "Results/{sample}/HQData/{sample}_R1.fastq.gz",
        R2 = "Results/{sample}/HQData/{sample}_R2.fastq.gz",
        unpaired_r1 = temp("Results/{sample}/TEMP/{sample}.rna_unpaired_R1.fastq.gz"),
        unpaired_r2 = temp("Results/{sample}/TEMP/{sample}.rna_unpaired_R2.fastq.gz"),
        failed= temp("Results/{sample}/TEMP/{sample}.rna_failed.fastq.gz"),
        json = "Results/{sample}/Qc/{sample}.rna.fastp.json",
        html = "Results/{sample}/Qc/{sample}.rna.fastp.html",
    params:
        rulename="preprocessing",
    threads: 10
    conda: "../envs/rna-seq-star-deseq2.yaml"
    shell:
        f"{{s_run_shell}} -j {{params.rulename}} -n {{wildcards.sample}} -c '"
        f"{scripts['merge_fq']} -r RawFastq -s {{wildcards.sample}} -o Results/{{wildcards.sample}}/MergeFastq"
        f"'"