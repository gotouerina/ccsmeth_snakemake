SampleIndex = {"golani"}
ref = "golani.chr.fa"
#kmc=/data/00/user/user214/miniconda3/envs/snakemake/bin/kmc
#genomewcope=/data/00/user/user214/miniconda3/envs/snakemake/bin/genomescope2
rule all:
    input:
        expand("{sample}.hifi.pbmm2.call_mods.modbam.freq", sample = SampleIndex)
rule callhifi:
    input:
        "{sample}.bam"
    output:
        "{sample}.hifi.bam"
    shell:
        """
        ccsmeth call_hifi --subreads {input}  --threads 10 --output {output}
        """
rule align:
    input:
        "{sample}.hifi.bam"
    output:
        "{sample}.hifi.pbmm2.bam"
    shell:
        "ccsmeth align_hifi --hifireads {input} --ref {ref} --output {output} --threads 10"
rule callmod:
    input:
        "{sample}.hifi.pbmm2.bam"
    output:
        "{sample}.hifi.pbmm2.call_mods.modbam.bam"
    params:
        "{sample}.hifi.pbmm2.call_mods"
    shell:
        """
        ccsmeth call_mods --input {input} --ref {ref} --model_file /home/106public/software/ccsmeth/models/model_ccsmeth_5mCpG_call_mods_attbigru2s_b21.v1.ckpt --output {params} --threads 10 --threads_call 2 --model_type attbigru2s rm _per_readsite --mode align

        """
rule callfrequency:
    input:
        "{sample}.hifi.pbmm2.call_mods.modbam.bam"
    output:
        "{sample}.hifi.pbmm2.call_mods.modbam.freq"
    shell:
        "ccsmeth call_freqb  --input_bam {input} --ref {ref} --output {output} --threads 10 --sort --bed --call_mod aggregate --aggre_model /home/106public/software/ccsmeth/models/model_ccsmeth_5mCpG_aggregate_attbigru_b11.v2.ckpt"

