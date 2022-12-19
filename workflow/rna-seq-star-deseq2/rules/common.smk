"""用于定义框架的全局变量"""

import glob
import os
import snakemake

import pandas as pd


def outdir(p):
    if not os.path.exists(p):
        os.makedirs(p)
    return p


# 全局路径路径
d_root = os.path.abspath("/dssg/home/sheny/MyProject/BioWorkFlow")  # 仓库路径
d_workdir = os.path.abspath("common/")  # 分析路径
d_log = outdir(f"{d_workdir}/Log")

# 样本信息
df_samples = pd.read_table("sample.tsv").set_index("SampleID", drop=False)

# 脚本路径
s_run_shell = f"python {d_root}/script/run_shell.py -d {d_log}"
scripts = {
    "merge_fq": f"python {d_root}/script/merge_fq.py",
}

# 相关函数
class Io:

    @staticmethod
    def merge_raw_fastq_output(wildcards):
        rslt = {
            "R1": f"Results/{wildcards.sample}/MergeFastq/{wildcards.sample}_R1.fastq.gz",
            "R2": f"Results/{wildcards.sample}/MergeFastq/{wildcards.sample}_R2.fastq.gz",
        }
        return rslt

