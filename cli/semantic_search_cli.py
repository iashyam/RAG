#!/usr/bin/env python3

import argparse
from lib.semantic_search import SemanticSearch
from lib.semantic_search import embed, verify_embeddings, embed_query_text, search
from handlers import chunk_handler, semantic_chunk_handler

def verify_model():
    search = SemanticSearch()
    print(f"Model Loaded {search.model}")
    print(f"Max sequence length: {search.model.max_seq_length}")

def main():
    parser = argparse.ArgumentParser(description="semantic search cli")
    subparsers = parser.add_subparsers(dest="command", help="available commands")

    varify_parser = subparsers.add_parser("verify", help="verify model")
    embedquery_parser = subparsers.add_parser("embedquery", help="embed query")
    embedquery_parser.add_argument("query", type=str, help="query to embed")
    varify_embeddings = subparsers.add_parser("verify_embeddings", help="verify embeddings")

    chunk_parser = subparsers.add_parser("chunk", help="chunk text")
    chunk_parser.add_argument("text", type=str, help="text to chunk")
    chunk_parser.add_argument("--chunk-size", type=int, default=200, help="chunk size")
    chunk_parser.add_argument("--overlap", type=int, default=0, help="overlap")

    semantic_chunk_parser = subparsers.add_parser("semantic_chunk", help="semantic_chunk text")
    semantic_chunk_parser.add_argument("text", type=str, help="text to semantic_chunk")
    semantic_chunk_parser.add_argument("--max-chunk-size", type=int, default=4, help="max size")
    semantic_chunk_parser.add_argument("--overlap", type=int, default=0, help="overlap")


    search_parser = subparsers.add_parser("search", help="search")
    search_parser.add_argument("query", type=str, help="query to search")
    search_parser.add_argument("--limit", type=int, default=5, help="limit")

    embed_parser = subparsers.add_parser("embed_text", help="embed text")
    embed_parser.add_argument("text", type=str, help="text to embed")

    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "verify_embeddings":
            verify_embeddings()
        case "embed_text":
            embed(args.text)
        case "embedquery":
            embed_query_text(args.query)
        case "search":
            search(args.query, args.limit)
        case "chunk":
            chunk_handler(args.text, args.chunk_size, args.overlap)
        case "semantic_chunk":
            semantic_chunk_handler(args.text, args.max_chunk_size, args.overlap)
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()