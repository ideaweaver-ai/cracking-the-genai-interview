# Text Splitters

Simple LangChain examples that split `sample.txt` into chunks.

## Setup

```bash
pip install -r requirements.txt
```

## Examples

| Script | Splitter | How it splits |
| --- | --- | --- |
| `fixed_length_splitter.py` | `CharacterTextSplitter` | Fixed character length (`separator=""`) |
| `recursive_character_splitter.py` | `RecursiveCharacterTextSplitter` | Paragraphs, then lines, then words |

Both use `chunk_size=80` and `chunk_overlap=20`.

```bash
python3 fixed_length_splitter.py
python3 recursive_character_splitter.py
```
