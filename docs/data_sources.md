# Data sources

The artifact ships **locked, derived source data** (`source_data/`, md5-pinned) so the headline figures
reproduce offline in quick mode. Full recomputation uses **public** datasets, fetched on demand — **none are vendored
or relicensed** here. Each retains its own license/terms.

| Domain | Public dataset | Access | Used for |
|--------|----------------|--------|----------|
| Microbiome | microbiomeHD (CRC case/control studies) | public download | Type A / C / E (leave-study-out) |
| Crop genomics | CIMMYT wheat (BGLR example data) | public (BGLR / CIMMYT) | Type A / E (leave-cluster-out) |
| Crop genomics | rice genotype/phenotype panel | public | Type E LOD (right-censored), Type A |
| Protein | ProteinGym substitution benchmarks | public | referenced baselines (not recomputed in quick mode) |
| Drug | TDC (Therapeutics Data Commons) scaffold splits | public via PyTDC | null-validity boundary case only |

## Downloader
`scripts/download_public_data.py` fetches raw inputs to a local cache and **verifies md5** before use. It does not
commit or redistribute any dataset. Restricted/DUA-gated datasets (e.g. some DREAM challenges) are **not** included;
where a gated set was unavailable we substituted a public one and say so in the manuscript.

## What is and isn't in the repo
- **In repo:** derived, md5-locked CSVs (numbers behind figures) + rendered figures. These are our outputs, Apache-2.0.
- **Not in repo:** raw third-party datasets, any restricted data, any credentials.
