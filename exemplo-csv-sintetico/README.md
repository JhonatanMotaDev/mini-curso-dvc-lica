# Exemplo mínimo: CSV sintético com Git + DVC

Versão reduzida da prática do minicurso. Em vez do dataset da UCI, usa um CSV sintético de 100 linhas, gerado de forma determinística (semente fixa) e sem download.

- **Repositório:** <https://github.com/JhonatanMotaDev/mini-curso-dvc-lica> (o `origin` configurado)
- **Branch:** `feat/csv-sintetico`
- **DVC:** 3.67.1 · **Python:** 3.11+

## Estrutura

```
exemplo-csv-sintetico/
├── scripts/generate_csv.py      # gerador (v1 | v2)
├── data/medicoes.csv            # gerado; ignorado pelo Git, rastreado pelo DVC
├── data/medicoes.csv.dvc        # ponteiro versionado no Git
├── remote-storage/              # remote local (ignorado pelo Git)
└── .dvc/                        # projeto DVC (init --subdir)
```

## Versões

| Versão | Descrição | Commit | MD5 esperado | Tamanho |
| --- | --- | --- | --- | --- |
| V1 | 100 linhas (`id,sensor,valor`) | `1a466ce27eed2e3f9167b0213c657b40408557d2` | `8259fcc178597cbd7c152ad2b75eb0db` | 1.796 bytes |
| V2 | V1 com 5 linhas alteradas | `fcf48bef65d2e660ab080025525f31eb36e3ca60` | `f1c46fa2bb6637081a7561b2c270c95f` | 1.801 bytes |

### Alteração V1 → V2

Nas linhas de dados `id` = 10, 20, 30, 40 e 50 (linhas 11, 21, 31, 41 e 51 do arquivo), a coluna `valor` passa a ser `999.99`:

| id | V1 | V2 |
| --- | --- | --- |
| 10 | 12.68 | 999.99 |
| 20 | 10.58 | 999.99 |
| 30 | 64.34 | 999.99 |
| 40 | 61.96 | 999.99 |
| 50 | 42.83 | 999.99 |

Como a semente é fixa, quem rodar o gerador obtém os mesmos checksums da tabela.

## Remote (um único esquema: `config.local`)

O remote é uma pasta dentro deste diretório, configurada **apenas** em `.dvc/config.local` (ignorado pelo Git). O `.dvc/config` versionado não contém remote, então cada clone configura o seu.

```bash
cd exemplo-csv-sintetico
dvc remote add --local --default lab remote-storage
cat .dvc/config.local
```

## Prática

```bash
cd exemplo-csv-sintetico
git switch -c minha-pratica

python3 scripts/generate_csv.py v1
dvc add data/medicoes.csv
git add . && git commit -m "data: track synthetic CSV V1"

python3 scripts/generate_csv.py v2
dvc add data/medicoes.csv
git add . && git commit -m "data: update synthetic CSV to V2"

dvc push --all-commits
dvc status --cloud
find remote-storage -type f | wc -l     # esperado: 2
```

### Alternar entre versões

```bash
git switch --detach 1a466ce && dvc checkout && md5sum data/medicoes.csv   # 8259fcc1...
git switch feat/csv-sintetico && dvc checkout && md5sum data/medicoes.csv   # f1c46fa2...
```

## Evidências

Saídas reais, executadas em 2026-11-25 após os dois commits.

`dvc push --all-commits`:

```text
2 files pushed
```

`dvc status --cloud`:

```text
Cache and remote 'lab' are in sync.
```

Contagem de objetos no remote (`find remote-storage -type f`):

```text
remote-storage/files/md5/82/59fcc178597cbd7c152ad2b75eb0db   # V1 (8259fcc1...)
remote-storage/files/md5/f1/c46fa2bb6637081a7561b2c270c95f   # V2 (f1c46fa2...)
```

**Total: 2 objetos**, um por versão, com os checksums idênticos aos dos arquivos `.dvc` de cada commit.
