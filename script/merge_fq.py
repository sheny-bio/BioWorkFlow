#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : shenny
# @Time     : 2022/11/14 16:37
# @File     : merge_fq.py
# @Project  : BioWorkFlow


"""合并同一个样本的所有fq文件"""

from multiprocessing import Pool
import logging
from glob import glob
import os
import subprocess

import click
import coloredlogs


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


class MergeFq(object):
    """ 合并同一样本的多个下机数据
    """

    def __init__(self, d_fq_list: list, sample_id, output="", suffix_r1="1*.fastq.gz", suffix_r2="2*.fastq.gz"):

        self.d_fq_list = d_fq_list
        self.sample_id = sample_id
        self.output = self._outdir(output)
        self.suffix_r1 = suffix_r1
        self.suffix_r2 = suffix_r2

        self.final_r1 = f"{self.output}/{self.sample_id}_R1.fastq.gz"
        self.final_r2 = f"{self.output}/{self.sample_id}_R2.fastq.gz"

    def merge(self):
        """合并R1 R2 fastq文件"""

        r1_list = sorted([f for d in self.d_fq_list for f in glob(f"{d}/{self.sample_id}*{self.suffix_r1}")])
        r2_list = sorted([f for d in self.d_fq_list for f in glob(f"{d}/{self.sample_id}*{self.suffix_r2}")])

        if len(r1_list) != len(r2_list) or r1_list == 0 or r2_list == 0:
            logger.info(f"Don't have multiple fastq files")
            subprocess.check_output(f"cp {r1_list[0]} {self.final_r1}", shell=True)
            subprocess.check_output(f"cp {r2_list[0]} {self.final_r2}", shell=True)
        else:
            cmd = f"cat {' '.join(r1_list)} > {self.final_r1}"
            logger.info(f"merge r1 fq. {cmd}")
            subprocess.check_output(cmd, shell=True)

            cmd = f"cat {' '.join(r2_list)} > {self.final_r2}"
            logger.info(f"merge r2 fq. {cmd}")
            subprocess.check_output(cmd, shell=True)

        logger.info(f"done!")

    @staticmethod
    def _outdir(p):
        if not os.path.exists(p):
            try:
                os.makedirs(p)
            except:
                pass
        return p


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option("-r", "--d_fq_list", "d_fq_list",
              multiple=True, required=True,
              help="原始下机目录"
              )
@click.option("-s", "--sample_id", "sample_id",
              required=True,
              help="样本ID"
              )
@click.option("-o", "--output",
              required=True,
              help="结果目录"
              )
@click.option("--x1", "--suffix_r1", "suffix_r1",
              default="1*.fastq.gz", help="R1文件的后缀(包含R1往后的字符串格式，支持正则匹配)"
              )
@click.option("--x2", "--suffix_r2", "suffix_r2",
              default="2*.fastq.gz", help="R2文件的后缀(包含R1往后的字符串格式，支持正则匹配)"
              )
def cli(**kwargs):
    MergeFq(**kwargs).merge()


if __name__ == '__main__':
    cli()
