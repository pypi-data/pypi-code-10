#!/usr/bin/env python

from pyplink import PyPlink

gen = PyPlink("t/test")
print(gen._geno_values)
snp, genotypes = gen.next()
print(genotypes.dtype)
