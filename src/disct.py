import json
import asyncio
import argparse
import sys
from typing import Any, Dict, Union, Optional, List
import discord
from sqlitedict import SqliteDict

# ---------- Serialization ----------

def serialize(obj: Any) -> Any:
    """
    Recursively convert discord.User/discord.Member objects into
    placeholder strings "user:ID". All other types are left unchanged.
    Handles dict, list, tuple, set, and basic types.
    """
    if isinstance(obj, (discord.User, discord.Member)):
        return f"user:{obj.id}"
    elif isinstance(obj, dict):
        return {serialize(k): serialize(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return type(obj)(serialize(item) for item in obj)
    else:
        return obj


# ---------- Deserialization ----------

async def deserialize(obj: Any, client: discord.Client) -> Any:
    """
    Recursively reconstruct the original structure by replacing
    "user:ID" strings with actual discord.User/discord.Member objects.
    Fetches missing users via client.fetch_user (async).
    """
    if isinstance(obj, str) and obj.startswith("user:"):
        user_id = int(obj[5:])
        return await fetch_user(client, user_id)
    elif isinstance(obj, dict):
        return {
            await deserialize(k, client): await deserialize(v, client)
            for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple, set)):
        return type(obj)([await deserialize(item, client) for item in obj])
    else:
        return obj


async def fetch_user(client: discord.Client, user_id: int) -> discord.User:
    """Helper to get a user by ID, fetching if not cached."""
    user = client.get_user(user_id)
    if user is None:
        user = await client.fetch_user(user_id)
    return user


# ---------- SQLiteDict Persistence ----------

def save_to_sqlitedict(db_path: str, key: str, data: Any) -> None:
    """
    Store a Python object under a given key in a SQLite dictionary.
    The data should be serializable (i.e., contain only basic types)
    or be properly serialized first using `serialize()`.
    """
    with SqliteDict(db_path) as db:
        db[key] = data
        db.commit()


def load_from_sqlitedict(db_path: str, key: str) -> Optional[Any]:
    """
    Retrieve the object stored under `key` from the SQLite dictionary.
    Returns None if the key does not exist.
    """
    with SqliteDict(db_path) as db:
        return db.get(key)


# ---------- JSON to SQLiteDict Transfer ----------

def convert_large_ints_to_users(data: Any, threshold: int = 10**15) -> Any:
    """
    Recursively traverse the data and replace any integer larger than
    `threshold` with a user placeholder string "user:<int>".
    This is a heuristic for Discord snowflake IDs.
    """
    if isinstance(data, int) and data > threshold:
        return f"user:{data}"
    elif isinstance(data, dict):
        return {k: convert_large_ints_to_users(v, threshold) for k, v in data.items()}
    elif isinstance(data, (list, tuple, set)):
        return type(data)(convert_large_ints_to_users(item, threshold) for item in data)
    else:
        return data


def transfer_json_to_sqlitedict(
    json_path: str,
    db_path: str,
    key: Optional[str] = None,
    use_serialized: bool = False,
    convert_large_ints: bool = False,
    large_int_threshold: int = 10**15
) -> None:
    """
    Read a JSON file and store its contents into a SQLite dictionary.

    - If `key` is provided, the whole JSON content is stored under that key.
    - If `key` is None, each top-level key of the JSON object is stored as a
      separate entry in the SQLite dict (the JSON must be a dict at top level).

    If `use_serialized` is True, the JSON is assumed to already contain
    serialized data (e.g., "user:123" placeholders). Otherwise, the data is
    passed through `serialize()` before storing.

    If `convert_large_ints` is True, any integer larger than `large_int_threshold`
    encountered during the process will be converted to a "user:ID" placeholder.
    This conversion happens *before* any serialization (if `use_serialized` is False)
    or as a separate pass (if `use_serialized` is True).
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Optionally convert large integers to user placeholders
    if convert_large_ints:
        data = convert_large_ints_to_users(data, large_int_threshold)

    # Optionally run through the serializer (if we want to ensure User objects are stored as strings)
    if not use_serialized:
        data = serialize(data)   # This will only affect actual discord.User objects, which are not present in raw JSON
        # If we converted large ints above, they are now "user:ID" strings, so serialize() leaves them unchanged.

    with SqliteDict(db_path) as db:
        if key is not None:
            db[key] = data
        else:
            if not isinstance(data, dict):
                raise ValueError(
                    "When key is None, the JSON must contain a top-level dictionary."
                )
            for k, v in data.items():
                db[k] = v
        db.commit()


# ---------- Command-Line Interface ----------

def main():
    parser = argparse.ArgumentParser(description="Transfer JSON data to SQLiteDict with optional Discord user serialization.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Subcommands')

    # transfer-json command
    transfer_parser = subparsers.add_parser('transfer-json', help='Transfer a JSON file to SQLiteDict')
    transfer_parser.add_argument('json_path', help='Path to input JSON file')
    transfer_parser.add_argument('db_path', help='Path to SQLiteDict database file')
    transfer_parser.add_argument('--key', help='Key under which to store the whole JSON object. If omitted, top-level keys become entries.')
    transfer_parser.add_argument('--serialized', action='store_true', help='Indicate that the JSON already contains serialized user placeholders ("user:ID").')
    transfer_parser.add_argument('--convert-large-ints', action='store_true', help='Convert integers larger than a threshold (snowflakes) to user placeholders.')
    transfer_parser.add_argument('--threshold', type=int, default=10**15, help='Threshold for large integer conversion (default: 10^15).')

    # get command (optional, to retrieve data)
    get_parser = subparsers.add_parser('get', help='Retrieve a value from SQLiteDict by key')
    get_parser.add_argument('db_path', help='Path to SQLiteDict database file')
    get_parser.add_argument('key', help='Key to retrieve')
    get_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # set command (optional, to store raw data)
    set_parser = subparsers.add_parser('set', help='Store a JSON value into SQLiteDict (raw, no conversion)')
    set_parser.add_argument('db_path', help='Path to SQLiteDict database file')
    set_parser.add_argument('key', help='Key to store under')
    set_parser.add_argument('json_data', help='JSON string to store')

    args = parser.parse_args()

    if args.command == 'transfer-json':
        transfer_json_to_sqlitedict(
            args.json_path,
            args.db_path,
            key=args.key,
            use_serialized=args.serialized,
            convert_large_ints=args.convert_large_ints,
            large_int_threshold=args.threshold
        )
        print(f"Data transferred to {args.db_path}")

    elif args.command == 'get':
        data = load_from_sqlitedict(args.db_path, args.key)
        if args.json:
            print(json.dumps(data, default=str, indent=2))
        else:
            print(data)

    elif args.command == 'set':
        try:
            data = json.loads(args.json_data)
        except json.JSONDecodeError:
            print("Error: Invalid JSON string", file=sys.stderr)
            sys.exit(1)
        save_to_sqlitedict(args.db_path, args.key, data)
        print(f"Data stored under key '{args.key}' in {args.db_path}")


if __name__ == "__main__":
    main()
