# Exemplo reprodutível de Git + DVC

Material do minicurso de 11/12/2026, preparado para o primeiro ensaio de 30/11/2026.

## Repositório e responsáveis

- **Repositório:** `JhonatanMotaDev/mini-curso-dvc-lica`
- **URL:** <https://github.com/JhonatanMotaDev/mini-curso-dvc-lica>
- **Branch principal:** `main`

## Objetivos e escopo do minicurso

Para alunos de graduação que participam de projetos do LICA. Os requisitos são: conhecimento básico de Python e uso de ferramentas CLI. Não é necessário conhecimento prévio de DVC ou outras ferramentas de versionamento de datasets.

Ao final da prática, a dupla deve conseguir versionar o dataset, voltar a uma versão anterior e recuperar o mesmo dado em um clone com cache DVC independente.

- **Git:** versiona código e pequenos metadados; arquivos binários grandes que mudam com frequência aumentam não são recomendados de serem armazenados no Github.
- **DVC:** mantém no Git um ponteiro `.dvc` com o checksum que identifica exatamente cada arquivo como é e armazena o conteúdo no cache e no remote configurado para a dupla.

## O dataset e versões registradas

O exemplo usa o dataset [Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption), da UCI. O arquivo original chama-se `household_power_consumption.txt` e contém dados tabulares separados por ponto e vírgula. Baixe e extraia o arquivo da página oficial para `data/source/household_power_consumption.txt`; essa fonte não é versionada pelo Git.

O script `scripts/create_snapshot.py` gera o CSV de saída em `data/snapshots/household_power_consumption.txt`:

| Versão | Período incluído | Commit que registra os metadados | MD5 esperado | Tamanho |
| --- | --- | --- | --- | --- |
| V1 | 2006-12-16 a 2007-12-15 | `963a1b37a6b8597b41b9c69099588ccdd412c564` | `5e507ee676ed05e635b24d2949213d2e` | 33.706.918 bytes |
| V2 | 2006-12-16 a 2010-11-26 | `f7ba4965547f0d087e464319794adcf8d9ed33c7` | `e05286cd4a257d80c3f0407b350df7dd` | 132.960.755 bytes |

O Git guarda os arquivos `.dvc` com os metadados e checksums. Os conteúdos ficam no cache DVC e são enviados ao remote; o CSV gerado não é adicionado ao Git.

## Pré-requisitos testados

Ambiente validado: Windows 11, PowerShell.

| Ferramenta | Versão |
| --- | --- |
| Python | 3.14.5 |
| Git | 2.55.0.windows.5 |
| DVC | 3.67.1 |

## 1. Instalação e remote local

```powershell
git clone [https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git](https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git)
cd mini-curso-dvc-lica
git switch main

py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "dvc==3.67.1"

git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

$dvc = '.\.venv\Scripts\dvc.exe'$remotePath = Join-Path (Get-Location).Path 'remote-storage'
New-Item -ItemType Directory -Force -Path $remotePath | Out-Null
& $dvc remote add --local --default --force lab$remotePath
& $dvc remote list
```

## 2. Criar e enviar as versões V1 e V2 do dataset

```powershell
$python = '.\.venv\Scripts\python.exe'
git switch -c pratica-git-dvc

& $python .\scripts\create_snapshot.py v1
& $dvc add .\data\snapshots\household_power_consumption.txt
git add .\data\snapshots\.gitignore .\data\snapshots\household_power_consumption.txt.dvc
git commit -m "data: track household power consumption V1"
$commitV1 = (git rev-parse HEAD).Trim()

& $python .\scripts\create_snapshot.py v2
& $dvc add .\data\snapshots\household_power_consumption.txt
git add .\data\snapshots\.gitignore .\data\snapshots\household_power_consumption.txt.dvc
git commit -m "data: update household power consumption to V2"

Get-Content .\data\snapshots\household_power_consumption.txt.dvc
git status --short --ignored

& $dvc push --all-commits
git push -u origin pratica-git-dvc
```

## 3. Alternar entre a V1 e V2 do dataset

```powershell
# V1 -> 5e507ee676ed05e635b24d2949213d2e
git switch --detach $commitV1
& $dvc checkout
(Get-FileHash .\data\snapshots\household_power_consumption.txt -Algorithm MD5).Hash.ToLower()

# V2 -> e05286cd4a257d80c3f0407b350df7dd
git switch pratica-git-dvc
& $dvc checkout
(Get-FileHash .\data\snapshots\household_power_consumption.txt -Algorithm MD5).Hash.ToLower()
```

## 4. Recuperar a V1 em outro clone

```powershell
$sourceRemotePath = Join-Path (Get-Location).Path 'remote-storage'$commitV1 = '963a1b37a6b8597b41b9c69099588ccdd412c564'
$clonePath = Join-Path$HOME 'mini-curso-dvc-v1-clone'

git clone [https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git](https://github.com/JhonatanMotaDev/mini-curso-dvc-lica.git) $clonePath
Set-Location $clonePath

py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "dvc==3.67.1"

$dvc = '.\.venv\Scripts\dvc.exe'
git switch --detach $commitV1
& $dvc remote modify --local lab url$sourceRemotePath
& $dvc pull

(Get-FileHash .\data\snapshots\household_power_consumption.txt -Algorithm MD5).Hash.ToLower() -eq '5e507ee676ed05e635b24d2949213d2e'
```