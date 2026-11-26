# Exemplo mínimo: CSV sintético com Git + DVC

Versão reduzida da prática do minicurso. Em vez do dataset da UCI, utiliza um CSV sintético com 100 registros, gerado deterministicamente (semente fixa), sem necessidade de download.

- **Repositório:** [mini-curso-dvc-lica](https://github.com/JhonatanMotaDev/mini-curso-dvc-lica)
- **Branch:** `feat/csv-sintetico`
- **DVC:** 3.67.1
- **Python:** 3.11+

## Estrutura

O exemplo fica dentro do repositório principal, com o DVC inicializado na subpasta usando `dvc init --subdir`.

```text
mini-curso-dvc-lica/
└── exemplo-csv-sintetico/
    ├── scripts/
    │   └── generate_csv.py       # gerador (v1 | v2)
    ├── data/
    │   ├── medicoes.csv          # gerado; ignorado pelo Git
    │   └── medicoes.csv.dvc      # ponteiro versionado pelo Git
    ├── remote-storage/           # remote local; ignorado pelo Git
    ├── .dvc/
    │   ├── config               # configuração versionada
    │   └── config.local         # configuração local do remote
    ├── .dvcignore
    ├── .gitignore
    └── README.md
```

O Git controla o histórico do projeto e dos arquivos `.dvc`. O DVC controla o armazenamento e a recuperação do conteúdo do CSV.

## Versões

| Versão | Descrição | Commit | MD5 | Tamanho |
| --- | --- | --- | --- | --- |
| V1 | 100 registros (`id,sensor,valor`) | `1a466ce27eed2e3f9167b0213c657b40408557d2` | `8259fcc178597cbd7c152ad2b75eb0db` | 1.796 bytes |
| V2 | V1 com 5 registros alterados | `fcf48bef65d2e660ab080025525f31eb36e3ca60` | `f1c46fa2bb6637081a7561b2c270c95f` | 1.801 bytes |

Os commits acima pertencem ao histórico publicado na branch `feat/csv-sintetico`. Em uma nova reprodução, os hashes dos commits serão diferentes, pois dependem dos metadados e do histórico Git.

### Alteração V1 → V2

Nas linhas de dados com `id` igual a 10, 20, 30, 40 e 50, a coluna `valor` passa a ser `999.99`.

| id | V1 | V2 |
| --- | --- | --- |
| 10 | 12.68 | 999.99 |
| 20 | 10.58 | 999.99 |
| 30 | 64.34 | 999.99 |
| 40 | 61.96 | 999.99 |
| 50 | 42.83 | 999.99 |

O gerador utiliza `random.Random(42)`, garantindo a geração dos mesmos valores para uma mesma versão. A V2 é construída a partir dos mesmos dados-base da V1, modificando somente os cinco registros indicados.

## Configuração do ambiente

Clone o repositório e entre na pasta do exemplo:

```bash
git clone -b feat/csv-sintetico \
  https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git

cd mini-curso-dvc-lica/exemplo-csv-sintetico
```

Confira as ferramentas:

```bash
git --version
python3 --version
dvc --version
```

O exemplo foi desenvolvido com DVC 3.67.1 e Python 3.11 ou superior.

## Remote local

O armazenamento remoto utiliza uma pasta local chamada `remote-storage/`.

A configuração é feita exclusivamente em `.dvc/config.local`, que não é versionado pelo Git. Assim, cada clone pode configurar seu próprio armazenamento sem modificar a configuração compartilhada do projeto.

Dentro da pasta `exemplo-csv-sintetico`, execute:

```bash
dvc remote add --local --default lab remote-storage
```

Confira a configuração:

```bash
cat .dvc/config.local
```

A configuração deve conter o remote `lab` como padrão, apontando para a pasta `remote-storage`.

**Importante:** o remote local não é compartilhado automaticamente entre clones ou computadores. Para recuperar os dados em outro ambiente, é necessário configurar o remote para apontar para o armazenamento que contém os objetos enviados.

## Prática

A prática utiliza o histórico já versionado na branch `feat/csv-sintetico`.

### 1. Conferir as versões

```bash
git log --oneline
```

Identifique os commits correspondentes à V1 e à V2.

### 2. Recuperar a V1

Selecione o commit da primeira versão:

```bash
git switch --detach 1a466ce27eed2e3f9167b0213c657b40408557d2
```

Recupere o conteúdo correspondente ao ponteiro DVC:

```bash
dvc checkout
```

Confira o checksum:

```bash
md5sum data/medicoes.csv
```

Resultado esperado:

```text
8259fcc178597cbd7c152ad2b75eb0db  data/medicoes.csv
```

### 3. Recuperar a V2

Retorne à branch do exemplo:

```bash
git switch feat/csv-sintetico
```

Recupere os dados correspondentes à versão atual:

```bash
dvc checkout
```

Confira:

```bash
md5sum data/medicoes.csv
```

Resultado esperado:

```text
f1c46fa2bb6637081a7561b2c270c95f  data/medicoes.csv
```

## Envio das versões ao remote

Para armazenar os objetos necessários à recuperação das versões históricas, execute:

```bash
dvc push --all-commits
```

O parâmetro `--all-commits` permite enviar os dados referenciados pelos commits disponíveis no histórico Git, e não apenas aqueles associados ao estado atual da workspace.

Resultado esperado:

```text
2 files pushed
```

Verifique a sincronização:

```bash
dvc status --cloud
```

Resultado esperado:

```text
Cache and remote 'lab' are in sync.
```

Confira os objetos armazenados:

```bash
find remote-storage -type f
```

Conte os objetos:

```bash
find remote-storage -type f | wc -l
```

Resultado esperado:

```text
2
```

## Evidências

Saídas reais obtidas durante a execução da prática em 25/11/2026.

**Envio dos dados:**

```text
2 files pushed
```

**Estado do remote:**

```text
Cache and remote 'lab' are in sync.
```

**Objetos armazenados:**

```text
remote-storage/files/md5/82/59fcc178597cbd7c152ad2b75eb0db
remote-storage/files/md5/f1/c46fa2bb6637081a7561b2c270c95f
```

**Total: 2 objetos**, correspondentes às duas versões do CSV.

Os checksums dos objetos correspondem aos valores registrados nos respectivos arquivos `.dvc`.

## Resultado esperado

Ao concluir a prática, é possível demonstrar:

1. **Geração determinística:** criação de um dataset sintético reproduzível, sem download externo.
2. **Versionamento de código e metadados:** histórico Git com ponteiros DVC distintos para cada versão.
3. **Versionamento de dados:** armazenamento de conteúdos identificados por checksum.
4. **Armazenamento remoto:** envio dos objetos correspondentes às versões históricas.
5. **Recuperação histórica:** restauração dos arquivos correspondentes a diferentes commits usando Git e DVC.

O exemplo demonstra como Git e DVC trabalham em conjunto: o Git registra a evolução dos metadados e o DVC armazena e recupera os dados associados a cada versão.

**Limitação do experimento:** a recuperação histórica foi demonstrada no ambiente de execução original. A recuperação em um segundo clone ou computador exige uma etapa adicional de configuração e validação do armazenamento remoto.
