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

Os commits acima pertencem ao histórico publicado na branch `feat/csv-sintetico`. Em uma nova reprodução feita do zero, os hashes dos commits serão diferentes, pois dependem dos metadados e do histórico Git. Os MD5 dos dados, por outro lado, são sempre os mesmos.

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

Crie uma pasta vazia, clone o repositório nela e entre na pasta do exemplo:

```bash
mkdir validacao && cd validacao

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

> **Não execute `git init` nem `dvc init` no clone.** O clone já é um repositório Git e o DVC já está inicializado nesta subpasta. Um `git init` dentro de `exemplo-csv-sintetico` cria um repositório vazio aninhado, que esconde o histórico e faz `git switch` para a V1 falhar com `fatal: unable to read tree`. Se isso acontecer, apague a pasta `.git` criada dentro de `exemplo-csv-sintetico` (somente ela).

Logo após o clone, `data/` contém apenas o ponteiro `medicoes.csv.dvc`. O CSV não vem pelo Git; ele é recuperado pelo DVC a partir do remote.

## Remote local

O armazenamento remoto utiliza uma pasta local chamada `remote-storage/`, que fica dentro de `exemplo-csv-sintetico/` e é ignorada pelo Git.

A configuração é feita exclusivamente em `.dvc/config.local`, que não é versionado. Assim, cada clone configura seu próprio armazenamento sem modificar a configuração compartilhada do projeto.

**Quem vai reproduzir o exercício** precisa receber a pasta `remote-storage/` da dupla que fez o `dvc push`, pois ela não vem no clone. Há duas formas:

1. Copiar a pasta da dupla para dentro de `exemplo-csv-sintetico/`:

   ```bash
   cp -r /caminho/da/dupla/exemplo-csv-sintetico/remote-storage ./remote-storage
   dvc remote add --local --default lab remote-storage
   ```

2. Apontar o remote diretamente para a pasta da dupla, sem copiar:

   ```bash
   dvc remote add --local --default lab /caminho/da/dupla/exemplo-csv-sintetico/remote-storage
   ```

**Quem está criando o exercício** do zero usa apenas `dvc remote add --local --default lab remote-storage`; a pasta é criada no primeiro `dvc push`.

Confira a configuração:

```bash
cat .dvc/config.local
```

A configuração deve conter o remote `lab` como padrão, apontando para a pasta `remote-storage`.

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

Busque no remote e restaure o conteúdo correspondente ao ponteiro DVC:

```bash
dvc pull
```

Confira o checksum e o conteúdo:

```bash
md5sum data/medicoes.csv
sed -n '11p' data/medicoes.csv
```

Resultado esperado:

```text
8259fcc178597cbd7c152ad2b75eb0db  data/medicoes.csv
10,sensor_1,12.68
```

> Use `dvc pull`, não apenas `dvc checkout`. O `checkout` só restaura versões que já estão no cache local; em um clone novo ele falha com `missing-files` ("Is your cache up to date?"). O `pull` busca o objeto no remote e faz o checkout em seguida.

### 3. Recuperar a V2

Retorne à branch do exemplo e recupere os dados:

```bash
git switch feat/csv-sintetico
dvc pull
```

Confira:

```bash
md5sum data/medicoes.csv
sed -n '11p' data/medicoes.csv
```

Resultado esperado:

```text
f1c46fa2bb6637081a7561b2c270c95f  data/medicoes.csv
10,sensor_1,999.99
```

### 4. Verificar a sincronização

```bash
dvc status
dvc status --cloud
```

Resultado esperado:

```text
Data and pipelines are up to date.
Cache and remote 'lab' are in sync.
```

## Envio das versões ao remote

Esta etapa é feita por quem criou as versões. Para armazenar os objetos necessários à recuperação das versões históricas, execute:

```bash
dvc push --all-commits
```

O parâmetro `--all-commits` envia os dados referenciados por todos os commits do histórico Git, e não apenas os associados ao estado atual da workspace.

Resultado esperado:

```text
2 files pushed
```

Verifique a sincronização e conte os objetos:

```bash
dvc status --cloud
find remote-storage -type f
find remote-storage -type f | wc -l
```

Resultado esperado: `Cache and remote 'lab' are in sync.` e **2** objetos.

## Evidências

### Envio ao remote (25/11/2026, ambiente original)

```text
$ dvc push --all-commits
2 files pushed

$ dvc status --cloud
Cache and remote 'lab' are in sync.

$ find remote-storage -type f
remote-storage/files/md5/82/59fcc178597cbd7c152ad2b75eb0db
remote-storage/files/md5/f1/c46fa2bb6637081a7561b2c270c95f
```

**Total: 2 objetos**, correspondentes às duas versões do CSV. Os checksums dos objetos correspondem aos valores registrados nos respectivos arquivos `.dvc`.

### Recuperação em clone independente (27/11/2026)

**Ambiente:** Linux 7.0.0-43-generic, Git 2.53.0, Python 3.14.4, DVC 3.67.1.
**Clone:** branch `feat/csv-sintetico` em pasta vazia, commit `e6c686a`, cache DVC próprio e vazio (`exemplo-csv-sintetico/.dvc/cache`).
**Remote:** cópia da pasta `remote-storage/` da dupla, configurada com `dvc remote add --local --default lab remote-storage`.

```text
$ ls -A data/
.gitignore  medicoes.csv.dvc

$ git switch --detach 1a466ce27eed2e3f9167b0213c657b40408557d2
HEAD is now at 1a466ce data(exemplo-csv): Adiciona o V1 para rastreio

$ dvc checkout
Is your cache up to date?
<https://error.dvc.org/missing-files>

$ dvc pull
A       data/medicoes.csv
1 file fetched and 1 file added

$ md5sum data/medicoes.csv
8259fcc178597cbd7c152ad2b75eb0db  data/medicoes.csv

$ wc -lc data/medicoes.csv
 101 1796 data/medicoes.csv

$ sed -n '11p;21p;31p;41p;51p' data/medicoes.csv
10,sensor_1,12.68
20,sensor_1,10.58
30,sensor_1,64.34
40,sensor_1,61.96
50,sensor_1,42.83

$ dvc status --cloud
Cache and remote 'lab' are in sync.

$ git switch feat/csv-sintetico && dvc checkout
$ md5sum data/medicoes.csv
f1c46fa2bb6637081a7561b2c270c95f  data/medicoes.csv
```

A V1 foi reproduzida com conteúdo e checksum idênticos aos registrados, e a V2 foi restaurada em seguida. As falhas encontradas durante a validação (`dvc checkout` com cache vazio e `git init` aninhado) motivaram os avisos incluídos nas seções *Configuração do ambiente*, *Remote local* e *Prática*.

## Resultado esperado

Ao concluir a prática, é possível demonstrar:

1. **Geração determinística:** criação de um dataset sintético reproduzível, sem download externo.
2. **Versionamento de código e metadados:** histórico Git com ponteiros DVC distintos para cada versão.
3. **Versionamento de dados:** armazenamento de conteúdos identificados por checksum.
4. **Armazenamento remoto:** envio dos objetos correspondentes às versões históricas.
5. **Recuperação histórica:** restauração dos arquivos correspondentes a diferentes commits usando Git e DVC, inclusive em um segundo clone com cache independente.

O exemplo demonstra como Git e DVC trabalham em conjunto: o Git registra a evolução dos metadados e o DVC armazena e recupera os dados associados a cada versão.

## Limitações conhecidas

1. **Remote local, não compartilhado.** A pasta `remote-storage/` existe apenas na máquina de quem fez o `dvc push`; para reproduzir em outro ambiente, ela precisa ser copiada ou acessível por caminho. Para uso real em equipe, o ideal é um remote compartilhado (S3, SSH, Google Drive etc.).
2. **Dataset pequeno.** O CSV de 100 registros valida o fluxo Git + DVC, mas não o desempenho com arquivos grandes.
3. **Repositório fora do padrão LICA.** O repositório está no GitHub pessoal, não no GitLab do LICA, e os commits não trazem o ID da task do ClickUp.

## Aceite

| Item | Onde |
| --- | --- |
| Repositório / branch | <https://github.com/JhonatanMotaDev/mini-curso-dvc-lica/tree/feat/csv-sintetico> |
| README | `exemplo-csv-sintetico/README.md` |
| Commit V1 | `1a466ce` |
| Commit V2 | `fcf48be` |
| Sincronização | *Evidências → Envio ao remote* |
| Recuperação | *Evidências → Recuperação em clone independente* |
| Limitações | *Limitações conhecidas* |
| Revisão | Angelina Meiras Ottoni — registra aceite ou ajustes solicitados |
