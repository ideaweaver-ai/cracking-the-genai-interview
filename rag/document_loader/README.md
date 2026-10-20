# Document Loaders

Simple LangChain examples that load files into `Document` objects (`page_content` + `metadata`).

## Setup

```bash
pip install -r requirements.txt
```

## Examples

| Script | Loader | Sample data |
| --- | --- | --- |
| `text_loader.py` | `TextLoader` | `sample.txt` |
| `pdf_loader.py` | `PyPDFLoader` | `sample.pdf` |
| `csv_loader.py` | `CSVLoader` | `sample.csv` |
| `directory_loader.py` | `DirectoryLoader` | `docs/*.txt` |

```bash
python3 text_loader.py
python3 pdf_loader.py
python3 csv_loader.py
python3 directory_loader.py
```

`DirectoryLoader` uses `TextLoader` for each matching file. `CSVLoader` creates one document per row.
