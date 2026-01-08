#!/usr/bin/env python3

import argparse
from handlers import*

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    
    idf_parser = subparsers.add_parser("idf", help="get idf")
    idf_parser = subparsers.add_parser("varify", help="Verify model")
    idf_parser.add_argument("term", type=str, help="idf query")

    bm25idf_parser = subparsers.add_parser("bm25idf", help="get BM 25 IDF")
    bm25idf_parser.add_argument("term", type=str, help="idf query")

    build_parser = subparsers.add_parser("build", help="Loads And Saves Movies into Index")

    tf_parser = subparsers.add_parser("tf", help="Takes a doc_id and term and outputs terms frequency.")
    tf_parser.add_argument("doc_id", type=int, help="document id")
    tf_parser.add_argument("term", type=str, help="term")

    bm25_tf_parser = subparsers.add_parser("bm25tf", help="Get BM25 TF score for a given document ID and term")
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument("k1", type=float, nargs='?', default=BM25_K1, help="Tunable BM25 K1 parameter")
    bm25_tf_parser.add_argument("b", type=float, nargs='?', default=BM25_B, help="Tunable BM25 b parameter")

    tf_idf_parser = subparsers.add_parser("tfidf", help="Takes a doc_id and term and outputs tf_idf score.")
    tf_idf_parser.add_argument("doc_id", type=int, help="document id")
    tf_idf_parser.add_argument("term", type=str, help="term")

    bm25search_parser = subparsers.add_parser("bm25search", help="Search movies using full BM25 scoring")
    bm25search_parser.add_argument("query", type=str, help="Search query")
    bm25search_parser.add_argument("--limit", type=int, default=5, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            search_hanlder(args.query)
        case "build":
            build_handler()
        case "tf":
            tf_handler(args.doc_id, args.term)
        case "bm25tf":
            bm25tf_handler(args.doc_id, args.term, args.k1, args.b)
        case "idf":
            idf_handler(args.term)
        case "bm25idf":
            bm25idf_handler(args.term)
        case "tfidf":
            tf_idf_handler(args.doc_id, args.term)
        case "bm25search":
            bm25_handler(args.query, args.limit)
        case "varify":
            varify_model()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
