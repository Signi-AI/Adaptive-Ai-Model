# Offline Content Ingestion Validation

This folder validates the offline educational content ingestion pipeline for W2-MT-01.

## Purpose

The ingestion layer prepares educational documents for the later local RAG retrieval system.

The pipeline:

Raw Documents
↓
Document Loader
↓
Text Extraction
↓
Text Chunking
↓
Metadata Extraction
↓
Processed Content

## Components

### `document_loader.py`

Loads local `.txt` educational documents.

Responsibilities:

- Load individual documents
- Load multiple documents from a directory
- Validate file paths
- Validate supported file types

### `chunker.py`

Splits extracted document text into smaller overlapping chunks.

Default configuration:

- Chunk size: 500 characters
- Overlap: 50 characters

### `metadata_extractor.py`

Creates metadata for each processed chunk.

Metadata includes:

- `chunk_id`
- `source`
- `topic`

### `ingest_content.py`

Connects all ingestion components into one pipeline.

It:

1. Loads raw documents.
2. Extracts text.
3. Splits text into chunks.
4. Creates metadata.
5. Saves processed content as JSON.

### `test_ingestion.py`

Validates the ingestion pipeline against the W2-MT-01 acceptance criteria.

## Directory Structure

```text
offline-content-ingestion/
├── raw/
│   └── sample_machine_learning.txt
├── processed/
│   └── processed_content.json
├── document_loader.py
├── chunker.py
├── metadata_extractor.py
├── ingest_content.py
├── test_ingestion.py
├── README.md
└── requirements.txt