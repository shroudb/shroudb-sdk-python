# shroudb

Unified Python SDK for all ShrouDB engines. Provides namespaced, type-safe
access to every engine with built-in serialization, connection pooling, and
dual transport support (RESP3 for direct connections, HTTP for Moat gateway).

## Installation

```bash
pip install shroudb
```

## Quick Start

```python
import asyncio
from shroudb import ShrouDB

async def main():
    # Connect via Moat gateway (routes all engines through one endpoint)
    async with ShrouDB(
        moat="https://moat.example.com",
        token="my-token",
    ) as db:
        # Encrypt data
        result = await db.cipher.encrypt("my-keyring", "SGVsbG8=")
        print(result.ciphertext)

        # Create a user
        user = await db.sigil.user_create("myapp", "alice",
            password="s3cret", email="alice@example.com")


asyncio.run(main())
```

```python
# Or connect to individual engines directly
db = ShrouDB(
    shroudb="shroudb://token@localhost:6399",
    cipher="shroudb-cipher://token@localhost:6599",
    sigil="sigil://token@localhost:6499",
    veil="shroudb-veil://token@localhost:6799",
    sentry="shroudb-sentry://token@localhost:6799",
    forge="shroudb-forge://token@localhost:6699",
    keep="shroudb-keep://token@localhost:6899",
    courier="shroudb-courier://token@localhost:6999",
    chronicle="chronicle://token@localhost:7099",
    stash="shroudb-stash://token@localhost:6399",
)
```

## Connection Modes

### Moat Gateway (HTTP)

Routes all engine commands through a single Moat endpoint via HTTP POST.

```python
db = ShrouDB(moat="https://moat.example.com", token="my-token")
```

### Moat Gateway (RESP3)

Direct RESP3 connection to Moat with engine-prefixed commands.

```python
db = ShrouDB(moat="shroudb-moat://my-token@moat.example.com:8201")
```

### Direct Engine Connections

Connect to individual engines via RESP3. Only configure the engines you need.

```python
db = ShrouDB(
    cipher="shroudb-cipher://token@cipher-host:6599",
    sigil="shroudb-sigil://token@sigil-host:6499",
)
```

### Mixed Mode

Route most engines through Moat, but connect directly to specific engines.

```python
db = ShrouDB(
    moat="https://moat.example.com",
    cipher="shroudb-cipher://token@dedicated-cipher:6599",  # direct
    token="moat-token",
)
```

## Engines

### `db.shroudb`

Encrypted key-value database

| Method | Description |
|--------|-------------|
| `auth(token)` | Authenticate the connection with a token |
| `command_list()` | List all supported commands |
| `config_get(key)` | Read a runtime configuration value |
| `config_set(key, value)` | Set a runtime configuration value (admin only) |
| `delete(namespace, key)` | Delete a key by writing a tombstone |
| `get(namespace, key, meta, **kwargs)` | Retrieve the value at a key |
| `health()` | Check server health |
| `list(namespace, **kwargs)` | List active keys in a namespace |
| `namespace_alter(name, **kwargs)` | Update namespace configuration (enforce-on-write-only) |
| `namespace_create(name, **kwargs)` | Create a new namespace |
| `namespace_drop(name, force)` | Drop a namespace |
| `namespace_info(name)` | Get metadata about a namespace |
| `namespace_list(**kwargs)` | List namespaces (filtered by token grants) |
| `namespace_validate(name)` | Check existing entries against current MetaSchema |
| `ping()` | Test connectivity |
| `pipeline(count)` | Execute commands atomically (all succeed or all roll back) |
| `put(namespace, key, value, **kwargs)` | Store a value at the given key. Auto-increments version. |
| `subscribe(namespace, **kwargs)` | Subscribe to change events on a namespace |
| `unsubscribe()` | End the current subscription |
| `versions(namespace, key, **kwargs)` | Retrieve version history for a key (most recent first) |

### `db.cipher`

Encryption-as-a-service

| Method | Description |
|--------|-------------|
| `auth(token)` | Authenticate the connection |
| `command_list()` | List all supported commands |
| `decrypt(keyring, ciphertext, **kwargs)` | Decrypt ciphertext using the embedded key version |
| `encrypt(keyring, plaintext, **kwargs)` | Encrypt plaintext with the active key version |
| `generate_data_key(keyring, **kwargs)` | Generate a data encryption key (envelope encryption pattern) |
| `health()` | Check server health |
| `key_info(keyring)` | Get keyring metadata and key version information |
| `keyring_create(name, algorithm, **kwargs)` | Create a new keyring with its first active key |
| `keyring_list()` | List all keyring names |
| `ping()` | Simple connectivity check — returns PONG |
| `rewrap(keyring, ciphertext, **kwargs)` | Re-encrypt ciphertext with the current active key version |
| `rotate(keyring, **kwargs)` | Rotate the keyring to a new key version |
| `sign(keyring, data)` | Create a detached signature |
| `verify_signature(keyring, data, signature)` | Verify a detached signature |

### `db.sigil`

Schema-driven credential envelope engine

| Method | Description |
|--------|-------------|
| `credential_change(schema, id, field, old, new)` | Change a credential field (requires old value for verification) |
| `credential_import(schema, id, field, hash, **kwargs)` | Import a pre-hashed credential (bcrypt, scrypt, argon2). Transparently rehashed to Argon2id on next verify. |
| `credential_reset(schema, id, field, new)` | Force-reset a credential field without requiring old value (admin/reset token) |
| `envelope_create(schema, id, json)` | Create an envelope with field routing per schema annotations |
| `envelope_delete(schema, id)` | Delete an envelope and all associated data |
| `envelope_get(schema, id)` | Get an envelope record |
| `envelope_import(schema, id, json)` | Import an envelope with pre-hashed credential fields. Non-credential fields processed normally. |
| `envelope_lookup(schema, field, value)` | Look up an envelope by indexed or searchable field value |
| `envelope_update(schema, id, json)` | Update non-credential fields on an existing envelope |
| `envelope_verify(schema, id, field, value)` | Verify a credential field on an envelope by explicit field name |
| `health()` | Health check |
| `jwks(schema)` | Get the JSON Web Key Set for external token verification |
| `password_change(schema, id, old, new)` | Sugar: change password. Infers credential field from schema. Equivalent to CREDENTIAL CHANGE with implicit field. |
| `password_import(schema, id, hash, **kwargs)` | Sugar: import pre-hashed password. Infers credential field from schema. Equivalent to CREDENTIAL IMPORT with implicit field. |
| `password_reset(schema, id, new)` | Sugar: force-reset password. Infers credential field from schema. Equivalent to CREDENTIAL RESET with implicit field. |
| `schema_get(name)` | Get a schema definition by name |
| `schema_list()` | List all registered schema names |
| `schema_register(name, json)` | Register a credential envelope schema |
| `session_create(schema, id, password, **kwargs)` | Verify credentials and issue access + refresh tokens |
| `session_list(schema, id)` | List active sessions for an entity |
| `session_refresh(schema, token)` | Rotate refresh token and issue new access token |
| `session_revoke(schema, token)` | Revoke a single refresh token (logout one session) |
| `session_revoke_all(schema, id)` | Revoke all sessions for an entity (logout everywhere) |
| `user_create(schema, id, json)` | Sugar: create an envelope. Equivalent to ENVELOPE CREATE. |
| `user_delete(schema, id)` | Sugar: delete an envelope. Equivalent to ENVELOPE DELETE. |
| `user_get(schema, id)` | Sugar: get an envelope. Equivalent to ENVELOPE GET. |
| `user_import(schema, id, json)` | Sugar: import an envelope with pre-hashed credentials. Equivalent to ENVELOPE IMPORT. |
| `user_update(schema, id, json)` | Sugar: update non-credential fields. Equivalent to ENVELOPE UPDATE. |
| `user_verify(schema, id, password)` | Sugar: verify credential. Infers the credential field from schema. Equivalent to ENVELOPE VERIFY with implicit field. |

### `db.veil`

veil

| Method | Description |
|--------|-------------|
| `auth(token)` | Authenticate this connection |
| `command_list()` | List all supported commands |
| `delete(index, id)` | Remove an entry's blind tokens from the index |
| `health()` | Health check |
| `index_create(name)` | Create a new blind index with a fresh HMAC key |
| `index_info(name)` | Get information about a blind index |
| `index_list()` | List all blind index names |
| `ping()` | Ping-pong |
| `put(index, id, data_b64, **kwargs)` | Store blind tokens for an entry. In standard mode, data_b64 is base64-encoded plaintext (server tokenizes). With BLIND flag, data_b64 is base64-encoded BlindTokenSet JSON (client pre-tokenized, for E2EE). |
| `search(index, query, **kwargs)` | Search a blind index. In standard mode, query is plain text (server tokenizes). With BLIND flag, query is base64-encoded BlindTokenSet JSON (client pre-tokenized, for E2EE). |
| `tokenize(index, plaintext_b64, **kwargs)` | Generate blind tokens from plaintext without storing. Returns HMAC-derived tokens for external use. |

### `db.sentry`

sentry

| Method | Description |
|--------|-------------|
| `auth(token)` | Authenticate the connection with a token |
| `command_list()` | List all supported commands |
| `evaluate(json)` | Evaluate an authorization request against policies and return a signed decision |
| `health()` | Server health check |
| `jwks()` | Get the JSON Web Key Set for verifying decision tokens |
| `key_info()` | Get signing key metadata |
| `key_rotate(**kwargs)` | Rotate the signing key |
| `ping()` | Connectivity check |
| `policy_create(name, json)` | Create a new authorization policy |
| `policy_delete(name)` | Delete a policy |
| `policy_get(name)` | Get a policy by name |
| `policy_list()` | List all policy names |
| `policy_update(name, json)` | Update an existing policy |

### `db.forge`

Internal certificate authority engine

| Method | Description |
|--------|-------------|
| `ca_create(name, algorithm, subject, **kwargs)` | Create a new Certificate Authority |
| `ca_export(name)` | Export the active CA certificate (PEM) |
| `ca_info(name)` | Get CA metadata and key version status |
| `ca_list()` | List all Certificate Authorities |
| `ca_rotate(name, **kwargs)` | Rotate CA signing key |
| `inspect(ca, serial)` | Get certificate details |
| `issue(ca, subject, profile, **kwargs)` | Issue a new certificate. Returns cert + private key (private key never stored). |
| `issue_from_csr(ca, csr_pem, profile, **kwargs)` | Issue a certificate from a PEM-encoded CSR |
| `list_certs(ca, **kwargs)` | List certificates for a CA |
| `renew(ca, serial, **kwargs)` | Renew a certificate (re-issue with same profile and SANs) |
| `revoke(ca, serial, **kwargs)` | Revoke a certificate |

### `db.keep`

Secrets manager with path-based access control and versioning

| Method | Description |
|--------|-------------|
| `auth(token)` | Authenticate this connection with a token. |
| `command_list()` | List all supported commands. |
| `delete(path)` | Soft-delete a secret. Version history is preserved. |
| `get(path, **kwargs)` | Retrieve a secret value. Returns the latest version by default. |
| `health()` | Health check. |
| `list(prefix)` | List secret paths, optionally filtered by prefix. Excludes deleted secrets. |
| `ping()` | Ping-pong. |
| `put(path, value)` | Store a new version of a secret. Creates the secret if it doesn't exist. Undeletes if soft-deleted. |
| `rotate(path)` | Re-encrypt the latest version with a new nonce. Creates a new version with the same plaintext. |
| `versions(path)` | Get version history for a secret. Includes deleted secrets. |

### `db.courier`

Just-in-time decryption delivery engine

| Method | Description |
|--------|-------------|
| `auth(token)` | Authenticate the connection with a token |
| `channel_create(name, type, config_json)` | Create a delivery channel |
| `channel_delete(name)` | Delete a channel |
| `channel_get(name)` | Get channel configuration |
| `channel_list()` | List all channels |
| `command_list()` | List available commands |
| `deliver(json)` | Decrypt recipient and deliver a message |
| `health()` | Server health check |
| `notify_event(channel, subject, body)` | Trigger a notification on a pre-configured channel (e.g. rotation/expiry alerts) |
| `ping()` | Connectivity check |

### `db.chronicle`

Structured audit event engine

| Method | Description |
|--------|-------------|
| `actors(**kwargs)` | Active actors in time window |
| `auth(token)` | Authenticate this connection |
| `count(**kwargs)` | Count events matching filter predicates |
| `errors(**kwargs)` | Error rates by action |
| `health()` | Health check |
| `hotspots(**kwargs)` | Top actors by event volume |
| `ingest(event_json)` | Ingest a single structured audit event |
| `ingest_batch(events_json)` | Ingest multiple events in a single call |
| `ping()` | Keepalive |
| `query(**kwargs)` | Query events with filter predicates |

### `db.stash`

Encrypted blob storage with S3 backend and envelope encryption

| Method | Description |
|--------|-------------|
| `command()` | List supported commands |
| `health()` | Health check |
| `inspect(id)` | Read blob metadata without downloading or decrypting |
| `ping()` | Ping-pong |
| `retrieve(id)` | Retrieve and decrypt a blob |
| `revoke(id, **kwargs)` | Revoke a blob (hard crypto-shred by default, SOFT for soft revoke) |
| `store(id, data_b64, **kwargs)` | Store an encrypted blob |

## Error Handling

```python
from shroudb import ShrouDBError
from shroudb.errors import ErrorCode

try:
    await db.cipher.encrypt("missing-keyring", data)
except ShrouDBError as err:
    if err.code == ErrorCode.NOTFOUND:
        print("Keyring not found")
```
