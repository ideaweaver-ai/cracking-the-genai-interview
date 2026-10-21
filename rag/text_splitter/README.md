# Text Splitters

Simple LangChain examples that split text into chunks.

## Setup

```bash
pip install -r requirements.txt
```

`semantic_splitter.py` also needs `OPENAI_API_KEY` in a `.env` file.

## Examples

| Script | Splitter | How it splits |
| --- | --- | --- |
| `fixed_length_splitter.py` | `CharacterTextSplitter` | Fixed character length (`separator=""`) |
| `recursive_character_splitter.py` | `RecursiveCharacterTextSplitter` | Paragraphs, then lines, then words |
| `semantic_splitter.py` | `SemanticChunker` | Where sentence meaning changes |

The first two use `sample.txt` with `chunk_size=80` and `chunk_overlap=20`. The semantic example uses `sample_semantic.txt` (two topics) and embeddings.

```bash
python3 fixed_length_splitter.py
python3 recursive_character_splitter.py
python3 semantic_splitter.py
```
