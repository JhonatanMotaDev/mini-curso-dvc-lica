# Mini curso DVC - LICA
Material do minicurso de 11/12/2026, preparado para o primeiro ensaio de 30/11/2026.

## Repositório e responsáveis

- **Repositório:** `JhonatanMotaDev/mini-curso-dvc-lica`
- **URL:** <https://github.com/JhonatanMotaDev/mini-curso-dvc-lica>
- **Branch principal:** `main`

## Objetivos e escopo do minicurso

Para alunos de graduação que participam de projetos do LICA. Os requisitos são: conhecimento básico de Python e uso de ferramentas CLI. Não é necessário conhecimento prévio de DVC ou outras ferramentas de versionamento de datasets.

Ao final da prática, a dupla deve conseguir versionar o dataset, voltar a uma versão anterior e recuperar o mesmo dado em um clone com cache DVC independente.

- **Git:** versiona código e pequenos metadados; arquivos binários grandes que mudam com frequência não são recomendados para armazenamento no GitHub.
- **DVC:** mantém no Git um ponteiro `.dvc` com o checksum que identifica cada versão do arquivo e armazena o conteúdo no cache e no remote configurado para a dupla.

## O dataset e versões registradas

O exemplo usa o dataset [Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption), da UCI. O arquivo original chama-se `household_power_consumption.txt` e contém dados tabulares separados por ponto e vírgula. Baixe e extraia o arquivo da página oficial para `data/source/household_power_consumption.txt`; essa fonte não é versionada pelo Git.

O script `scripts/create_snapshot.py` gera o arquivo de saída em `data/snapshots/household_power_consumption.txt`:

| Versão | Período incluído | Commit que registra os metadados | MD5 esperado | Tamanho |
| --- | --- | --- | --- | --- |
| V1 | 2006-12-16 a 2007-12-15 | `963a1b37a6b8597b41b9c69099588ccdd412c564` | `5e507ee676ed05e635b24d2949213d2e` | 33.706.918 bytes |
| V2 | 2006-12-16 a 2010-11-26 | `f7ba4965547f0d087e464319794adcf8d9ed33c7` | `e05286cd4a257d80c3f0407b350df7dd` | 132.960.755 bytes |

Os hashes na coluna "Commit" são do ambiente de referência; a dupla vai gerar commits próprios na seção 2 e deve anotar seus hashes. O Git guarda os arquivos `.dvc` com os metadados e checksums. Os conteúdos ficam no cache DVC e são enviados ao remote; o arquivo gerado não é adicionado ao Git.

## Pré-requisitos testados

| Ferramenta | Versão | Observação |
| --- | --- | --- |
| Python | 3.11 + |
| Git | 2.55.0 | qualquer versão recente |
| DVC | 3.67.1 | fixado no tutorial |

## 1. Instalação e remote local

O remote é uma pasta comum fora do repositório que simula o armazenamento compartilhado da dupla. Por ser local, não exige credenciais nem acesso a infraestrutura do LICA. A configuração fica em `.dvc/config.local`, que o Git ignora por padrão — ou seja, cada clone precisa configurar o próprio caminho.

**Windows (PowerShell)**

```powershell
git clone https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git
cd mini-curso-dvc-lica
git switch main

py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "dvc==3.67.1"

git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

$dvc        = '.\.venv\Scripts\dvc.exe'
$remotePath = Join-Path $HOME 'dvc-remote-dupla01'   # troque o número da dupla
New-Item -ItemType Directory -Force -Path $remotePath | Out-Null
& $dvc remote add --local --default --force lab $remotePath
& $dvc remote list --local
```

**Linux / macOS (bash/zsh)**

```bash
git clone https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git
cd mini-curso-dvc-lica
git switch main

python3 -m venv .venv
.venv/bin/pip install "dvc==3.67.1"

git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

dvc=".venv/bin/dvc"
remotePath="$HOME/dvc-remote-dupla01"   # troque o número da dupla
mkdir -p "$remotePath"
"$dvc" remote add --local --default --force lab "$remotePath"
"$dvc" remote list --local
```

## 2. Criar e enviar as versões V1 e V2 do dataset

**Windows (PowerShell)**

```powershell
$python     = '.\.venv\Scripts\python.exe'
$dvc        = '.\.venv\Scripts\dvc.exe'
$remotePath = Join-Path $HOME 'dvc-remote-dupla01'
git switch -c pratica-git-dvc

& $python .\scripts\create_snapshot.py v1
& $dvc add .\data\snapshots\household_power_consumption.txt
git add .\data\snapshots\.gitignore .\data\snapshots\household_power_consumption.txt.dvc
git commit -m "data: track household power consumption V1"
$commitV1 = (git rev-parse HEAD).Trim()
Write-Host "Anote o hash da V1: $commitV1"

& $python .\scripts\create_snapshot.py v2
& $dvc add .\data\snapshots\household_power_consumption.txt
git add .\data\snapshots\.gitignore .\data\snapshots\household_power_consumption.txt.dvc
git commit -m "data: update household power consumption to V2"

Get-Content .\data\snapshots\household_power_consumption.txt.dvc
git status --short --ignored

& $dvc push --all-commits
& $dvc status --cloud
Get-ChildItem $remotePath -Recurse -File | Measure-Object | Select-Object Count

git push -u origin pratica-git-dvc
```

**Linux / macOS (bash/zsh)**

```bash
python=".venv/bin/python"
dvc=".venv/bin/dvc"
remotePath="$HOME/dvc-remote-dupla01"
git switch -c pratica-git-dvc

"$python" scripts/create_snapshot.py v1
"$dvc" add data/snapshots/household_power_consumption.txt
git add data/snapshots/.gitignore data/snapshots/household_power_consumption.txt.dvc
git commit -m "data: track household power consumption V1"
commitV1=$(git rev-parse HEAD)
echo "Anote o hash da V1: $commitV1"

"$python" scripts/create_snapshot.py v2
"$dvc" add data/snapshots/household_power_consumption.txt
git add data/snapshots/.gitignore data/snapshots/household_power_consumption.txt.dvc
git commit -m "data: update household power consumption to V2"

cat data/snapshots/household_power_consumption.txt.dvc
git status --short --ignored

"$dvc" push --all-commits
"$dvc" status --cloud
find "$remotePath" -type f | wc -l

git push -u origin pratica-git-dvc
```

## 3. Alternar entre a V1 e V2 do dataset

**Windows (PowerShell)**

```powershell
$dvc = '.\.venv\Scripts\dvc.exe'
# $commitV1 foi definido na seção 2; se abriu terminal novo, cole o hash anotado:
# $commitV1 = 'cole-aqui-o-hash-da-v1'

# V1 -> 5e507ee676ed05e635b24d2949213d2e
git switch --detach $commitV1
& $dvc checkout
(Get-FileHash .\data\snapshots\household_power_consumption.txt -Algorithm MD5).Hash.ToLower()

# V2 -> e05286cd4a257d80c3f0407b350df7dd
git switch pratica-git-dvc
& $dvc checkout
(Get-FileHash .\data\snapshots\household_power_consumption.txt -Algorithm MD5).Hash.ToLower()
```

**Linux / macOS (bash/zsh)**

```bash
dvc=".venv/bin/dvc"
# commitV1 foi definido na seção 2; se abriu terminal novo, cole o hash anotado:
# commitV1='cole-aqui-o-hash-da-v1'

# V1 -> 5e507ee676ed05e635b24d2949213d2e
git switch --detach "$commitV1"
"$dvc" checkout
md5sum data/snapshots/household_power_consumption.txt   # Linux
# md5 data/snapshots/household_power_consumption.txt   # macOS

# V2 -> e05286cd4a257d80c3f0407b350df7dd
git switch pratica-git-dvc
"$dvc" checkout
md5sum data/snapshots/household_power_consumption.txt   # Linux
# md5 data/snapshots/household_power_consumption.txt   # macOS
```

## 4. Recuperar a V1 em outro clone

**Windows (PowerShell)**

```powershell
# Cole o hash anotado na seção 2 e o caminho do remote configurado na seção 1
$commitV1         = 'cole-aqui-o-hash-da-v1'
$sourceRemotePath = Join-Path $HOME 'dvc-remote-dupla01'
$clonePath        = Join-Path $HOME 'mini-curso-dvc-v1-clone'

git clone https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git $clonePath
Push-Location $clonePath

py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "dvc==3.67.1"

$dvc = '.\.venv\Scripts\dvc.exe'
& $dvc remote add --local --default --force lab $sourceRemotePath
git switch --detach $commitV1
& $dvc pull

$ok = (Get-FileHash .\data\snapshots\household_power_consumption.txt -Algorithm MD5).Hash.ToLower() -eq '5e507ee676ed05e635b24d2949213d2e'
Write-Host "Hash confere: $ok"   # deve imprimir True

Pop-Location
```

**Linux / macOS (bash/zsh)**

```bash
# Cole o hash anotado na seção 2 e o caminho do remote configurado na seção 1
commitV1='cole-aqui-o-hash-da-v1'
sourceRemotePath="$HOME/dvc-remote-dupla01"
clonePath="$HOME/mini-curso-dvc-v1-clone"

git clone https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git "$clonePath"
cd "$clonePath"

python3 -m venv .venv
.venv/bin/pip install "dvc==3.67.1"

dvc=".venv/bin/dvc"
"$dvc" remote add --local --default --force lab "$sourceRemotePath"
git switch --detach "$commitV1"
"$dvc" pull

hash=$(md5sum data/snapshots/household_power_consumption.txt | awk '{print $1}')   # Linux
# hash=$(md5 -q data/snapshots/household_power_consumption.txt)                   # macOS
[ "$hash" = "5e507ee676ed05e635b24d2949213d2e" ] && echo "Hash confere: True" || echo "Hash confere: False"
```
