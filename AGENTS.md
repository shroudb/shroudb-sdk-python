# ShrouDB SDK — Agent Instructions

> Unified Python SDK for all ShrouDB security engines. Provides namespaced, type-safe access with built-in serialization.

## Quick Context

- **Package**: `shroudb`
- **Transport**: RESP3 (direct engine connections) or HTTP (Moat gateway)
- **Pattern**: `await db.<engine>.<command>(params)` — all methods async, return typed dataclasses
- **Serialization**: Handled internally — pass native Python types, get typed objects back

## Connection

```python
from shroudb import ShrouDB

# Moat gateway (HTTP) — all engines through one endpoint
async with ShrouDB(moat="https://moat.example.com", token="my-token") as db:
    ...

# Direct — only the engines you need
db = ShrouDB(cipher="shroudb-cipher://token@host:6599")

# Mixed — Moat default + direct overrides
db = ShrouDB(
    moat="https://moat.example.com",
    cipher="shroudb-cipher://token@dedicated:6599",
    token="moat-token",
)

# Always close when done (or use async with)
await db.close()
```

## `db.shroudb` — Encrypted key-value database

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `auth` | `token` | `{ actor }` | Authenticate the connection with a token |
| `command_list` | `` | `{ commands, count }` | List all supported commands |
| `config_get` | `key` | `{ key, value }` | Read a runtime configuration value |
| `config_set` | `key, value` | `{}` | Set a runtime configuration value (admin only) |
| `delete` | `namespace, key` | `{ version }` | Delete a key by writing a tombstone |
| `get` | `namespace, key, meta=None, **kwargs` | `{ key, metadata, value, version }` | Retrieve the value at a key |
| `health` | `` | `{ message }` | Check server health |
| `list` | `namespace, **kwargs` | `{ cursor, keys }` | List active keys in a namespace |
| `namespace_alter` | `name, **kwargs` | `{}` | Update namespace configuration (enforce-on-write-only) |
| `namespace_create` | `name, **kwargs` | `{}` | Create a new namespace |
| `namespace_drop` | `name, force=None` | `{}` | Drop a namespace |
| `namespace_info` | `name` | `{ created_at, key_count, name }` | Get metadata about a namespace |
| `namespace_list` | `**kwargs` | `{ cursor, namespaces }` | List namespaces (filtered by token grants) |
| `namespace_validate` | `name` | `{ count, reports }` | Check existing entries against current MetaSchema |
| `ping` | `` | `{ message }` | Test connectivity |
| `pipeline` | `count` | `{}` | Execute commands atomically (all succeed or all roll back) |
| `put` | `namespace, key, value=None, **kwargs` | `{ version }` | Store a value at the given key. Auto-increments version. |
| `subscribe` | `namespace, **kwargs` | `{}` | Subscribe to change events on a namespace |
| `unsubscribe` | `` | `{}` | End the current subscription |
| `versions` | `namespace, key, **kwargs` | `{ versions }` | Retrieve version history for a key (most recent first) |

### Examples

```python
result = await db.shroudb.config_get("key")
print(result.key)
await db.shroudb.config_set("key", "alice@example.com")
result = await db.shroudb.delete("namespace", "key")
print(result.version)
```

## `db.cipher` — Encryption-as-a-service

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `auth` | `token` | `{ status }` | Authenticate the connection |
| `command_list` | `` | `{ count, commands }` | List all supported commands |
| `decrypt` | `keyring, ciphertext, **kwargs` | `{ plaintext }` | Decrypt ciphertext using the embedded key version |
| `encrypt` | `keyring, plaintext, **kwargs` | `{ ciphertext, key_version }` | Encrypt plaintext with the active key version |
| `generate_data_key` | `keyring, **kwargs` | `{ plaintext_key, wrapped_key, key_version }` | Generate a data encryption key (envelope encryption pattern) |
| `health` | `` | `{ status }` | Check server health |
| `key_info` | `keyring` | `{ keyring, algorithm, active_version, versions }` | Get keyring metadata and key version information |
| `keyring_create` | `name, algorithm, **kwargs` | `{ keyring, algorithm, active_version }` | Create a new keyring with its first active key |
| `keyring_list` | `` | `{ keyrings }` | List all keyring names |
| `ping` | `` | `{ message }` | Simple connectivity check — returns PONG |
| `rewrap` | `keyring, ciphertext, **kwargs` | `{ ciphertext, key_version }` | Re-encrypt ciphertext with the current active key version |
| `rotate` | `keyring, **kwargs` | `{ rotated, key_version, previous_version }` | Rotate the keyring to a new key version |
| `sign` | `keyring, data` | `{ signature, key_version }` | Create a detached signature |
| `verify_signature` | `keyring, data, signature` | `{ valid }` | Verify a detached signature |

### Examples

```python
result = await db.cipher.decrypt("my-keyring", "k3Xm:encrypted...")
print(result.plaintext)
result = await db.cipher.encrypt("my-keyring", "SGVsbG8=")
print(result.ciphertext)
result = await db.cipher.generate_data_key("my-keyring")
print(result.plaintext_key)
```

## `db.sigil` — Schema-driven credential envelope engine

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `credential_change` | `schema, id, field, old, new` | `{ status }` | Change a credential field (requires old value for verification) |
| `credential_import` | `schema, id, field, hash, **kwargs` | `{ algorithm }` | Import a pre-hashed credential (bcrypt, scrypt, argon2). Transparently rehashed to Argon2id on next verify. |
| `credential_reset` | `schema, id, field, new` | `{ status }` | Force-reset a credential field without requiring old value (admin/reset token) |
| `envelope_create` | `schema, id, json` | `{ created_at, fields, id }` | Create an envelope with field routing per schema annotations |
| `envelope_delete` | `schema, id` | `{ status }` | Delete an envelope and all associated data |
| `envelope_get` | `schema, id` | `{ created_at, fields, id, updated_at }` | Get an envelope record |
| `envelope_import` | `schema, id, json` | `{ created_at, fields, id }` | Import an envelope with pre-hashed credential fields. Non-credential fields processed normally. |
| `envelope_lookup` | `schema, field, value` | `{ created_at, fields, id, updated_at }` | Look up an envelope by indexed or searchable field value |
| `envelope_update` | `schema, id, json` | `{ fields, id, updated_at }` | Update non-credential fields on an existing envelope |
| `envelope_verify` | `schema, id, field, value` | `{ valid }` | Verify a credential field on an envelope by explicit field name |
| `health` | `` | `{ status }` | Health check |
| `jwks` | `schema` | `{ keys }` | Get the JSON Web Key Set for external token verification |
| `password_change` | `schema, id, old, new` | `{ status }` | Sugar: change password. Infers credential field from schema. Equivalent to CREDENTIAL CHANGE with implicit field. |
| `password_import` | `schema, id, hash, **kwargs` | `{ algorithm }` | Sugar: import pre-hashed password. Infers credential field from schema. Equivalent to CREDENTIAL IMPORT with implicit field. |
| `password_reset` | `schema, id, new` | `{ status }` | Sugar: force-reset password. Infers credential field from schema. Equivalent to CREDENTIAL RESET with implicit field. |
| `schema_get` | `name` | `{ schema }` | Get a schema definition by name |
| `schema_list` | `` | `{ names }` | List all registered schema names |
| `schema_register` | `name, json` | `{ version }` | Register a credential envelope schema |
| `session_create` | `schema, id, password, **kwargs` | `{ access_token, expires_in, refresh_token }` | Verify credentials and issue access + refresh tokens |
| `session_list` | `schema, id` | `{ sessions }` | List active sessions for an entity |
| `session_refresh` | `schema, token` | `{ access_token, expires_in, refresh_token }` | Rotate refresh token and issue new access token |
| `session_revoke` | `schema, token` | `{ status }` | Revoke a single refresh token (logout one session) |
| `session_revoke_all` | `schema, id` | `{ revoked }` | Revoke all sessions for an entity (logout everywhere) |
| `user_create` | `schema, id, json` | `{ created_at, fields, user_id }` | Sugar: create an envelope. Equivalent to ENVELOPE CREATE. |
| `user_delete` | `schema, id` | `{ status }` | Sugar: delete an envelope. Equivalent to ENVELOPE DELETE. |
| `user_get` | `schema, id` | `{ created_at, fields, updated_at, user_id }` | Sugar: get an envelope. Equivalent to ENVELOPE GET. |
| `user_import` | `schema, id, json` | `{ created_at, fields, user_id }` | Sugar: import an envelope with pre-hashed credentials. Equivalent to ENVELOPE IMPORT. |
| `user_update` | `schema, id, json` | `{ fields, updated_at, user_id }` | Sugar: update non-credential fields. Equivalent to ENVELOPE UPDATE. |
| `user_verify` | `schema, id, password` | `{ valid }` | Sugar: verify credential. Infers the credential field from schema. Equivalent to ENVELOPE VERIFY with implicit field. |

### Examples

```python
result = await db.sigil.credential_change("myapp", "alice", "email", "old", "new")
print(result.status)
result = await db.sigil.credential_import("myapp", "alice", "email", "hash")
print(result.algorithm)
result = await db.sigil.credential_reset("myapp", "alice", "email", "new")
print(result.status)
```

## `db.veil` — veil

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `auth` | `token` | `{ status }` | Authenticate this connection |
| `command_list` | `` | `{ count, commands }` | List all supported commands |
| `delete` | `index, id` | `{ status, id }` | Remove an entry's blind tokens from the index |
| `health` | `` | `{ status }` | Health check |
| `index_create` | `name` | `{ status, index, created_at }` | Create a new blind index with a fresh HMAC key |
| `index_info` | `name` | `{ index, created_at, entry_count }` | Get information about a blind index |
| `index_list` | `` | `{ items, type }` | List all blind index names |
| `ping` | `` | `{ type, value }` | Ping-pong |
| `put` | `index, id, plaintext_b64, **kwargs` | `{ status, id, version }` | Tokenize plaintext and store the blind tokens under the given entry ID |
| `search` | `index, query, **kwargs` | `{ status, scanned, matched, results }` | Search a blind index. Tokenizes the query, generates blind tokens, and compares against stored entries. |
| `tokenize` | `index, plaintext_b64, **kwargs` | `{ status, words, trigrams, tokens }` | Generate blind tokens from plaintext without storing. Returns HMAC-derived tokens for external use. |

### Examples

```python
result = await db.veil.delete("index", "alice")
print(result.status)
result = await db.veil.index_create("my-keyring")
print(result.status)
result = await db.veil.index_info("my-keyring")
print(result.index)
```

## `db.sentry` — sentry

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `auth` | `token` | `{ status }` | Authenticate the connection with a token |
| `command_list` | `` | `{ commands, status }` | List all supported commands |
| `evaluate` | `json` | `{ cache_until, decision, matched_policy, status, token }` | Evaluate an authorization request against policies and return a signed decision |
| `health` | `` | `{ policy_count, status }` | Server health check |
| `jwks` | `` | `{ keys }` | Get the JSON Web Key Set for verifying decision tokens |
| `key_info` | `` | `{ active_kid, active_version, algorithm, decision_ttl_secs, drain_days, jwks_keys, rotation_days, status, total_versions }` | Get signing key metadata |
| `key_rotate` | `**kwargs` | `{ key_version, previous_version, rotated, status }` | Rotate the signing key |
| `ping` | `` | `{}` | Connectivity check |
| `policy_create` | `name, json` | `{ effect, name, priority, status }` | Create a new authorization policy |
| `policy_delete` | `name` | `{ status }` | Delete a policy |
| `policy_get` | `name` | `{ created_at, description, effect, name, priority, status, updated_at }` | Get a policy by name |
| `policy_list` | `` | `{ count, policies, status }` | List all policy names |
| `policy_update` | `name, json` | `{ effect, name, priority, status, updated_at }` | Update an existing policy |

### Examples

```python
result = await db.sentry.evaluate("json")
print(result.cache_until)
result = await db.sentry.policy_create("name", "json")
print(result.effect)
result = await db.sentry.policy_delete("name")
print(result.status)
```

## `db.forge` — Internal certificate authority engine

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `ca_create` | `name, algorithm, subject, **kwargs` | `{ active_version, algorithm, name, subject }` | Create a new Certificate Authority |
| `ca_export` | `name` | `{ certificate_pem }` | Export the active CA certificate (PEM) |
| `ca_info` | `name` | `{ algorithm, key_versions, name, subject }` | Get CA metadata and key version status |
| `ca_list` | `` | `{ cas }` | List all Certificate Authorities |
| `ca_rotate` | `name, **kwargs` | `{ key_version, previous_version, rotated }` | Rotate CA signing key |
| `inspect` | `ca, serial` | `{ certificate_pem, serial, state, subject }` | Get certificate details |
| `issue` | `ca, subject, profile, **kwargs` | `{ certificate_pem, private_key_pem, serial }` | Issue a new certificate. Returns cert + private key (private key never stored). |
| `issue_from_csr` | `ca, csr_pem, profile, **kwargs` | `{ certificate_pem, serial }` | Issue a certificate from a PEM-encoded CSR |
| `list_certs` | `ca, **kwargs` | `{ certs, count }` | List certificates for a CA |
| `renew` | `ca, serial, **kwargs` | `{ certificate_pem, private_key_pem, serial }` | Renew a certificate (re-issue with same profile and SANs) |
| `revoke` | `ca, serial, **kwargs` | `{ status }` | Revoke a certificate |

### Examples

```python
result = await db.forge.ca_create("name", "algorithm", "subject")
print(result.active_version)
result = await db.forge.ca_export("name")
print(result.certificate_pem)
result = await db.forge.ca_info("name")
print(result.algorithm)
```

## `db.keep` — Secrets manager with path-based access control and versioning

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `auth` | `token` | `{ status }` | Authenticate this connection with a token. |
| `command_list` | `` | `{ count, commands }` | List all supported commands. |
| `delete` | `path` | `{ status, path, deleted_at }` | Soft-delete a secret. Version history is preserved. |
| `get` | `path, **kwargs` | `{ status, path, version, value, created_at, created_by }` | Retrieve a secret value. Returns the latest version by default. |
| `health` | `` | `{ status }` | Health check. |
| `list` | `prefix=None` | `{ status, count, paths }` | List secret paths, optionally filtered by prefix. Excludes deleted secrets. |
| `ping` | `` | `{}` | Ping-pong. |
| `put` | `path, value` | `{ status, path, version }` | Store a new version of a secret. Creates the secret if it doesn't exist. Undeletes if soft-deleted. |
| `rotate` | `path` | `{ status, path, version }` | Re-encrypt the latest version with a new nonce. Creates a new version with the same plaintext. |
| `versions` | `path` | `{ status, path, version_count, versions, deleted }` | Get version history for a secret. Includes deleted secrets. |

### Examples

```python
result = await db.keep.delete("path")
print(result.status)
result = await db.keep.get("path")
print(result.status)
result = await db.keep.list("prefix")
print(result.status)
```

## `db.courier` — Just-in-time decryption delivery engine

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `auth` | `token` | `{ status }` | Authenticate the connection with a token |
| `channel_create` | `name, type, config_json` | `{ channel_type, name, status }` | Create a delivery channel |
| `channel_delete` | `name` | `{ name, status }` | Delete a channel |
| `channel_get` | `name` | `{ channel_type, created_at, enabled, name }` | Get channel configuration |
| `channel_list` | `` | `{ channels, count, status }` | List all channels |
| `command_list` | `` | `{ commands, count }` | List available commands |
| `deliver` | `json` | `{ channel, delivered_at, delivery_id, status }` | Decrypt recipient and deliver a message |
| `health` | `` | `{ channels, status }` | Server health check |
| `ping` | `` | `{}` | Connectivity check |

### Examples

```python
result = await db.courier.channel_create("name", "type", "config_json")
print(result.channel_type)
result = await db.courier.channel_delete("name")
print(result.name)
result = await db.courier.channel_get("name")
print(result.channel_type)
```

## `db.chronicle` — Structured audit event engine

| Method | Args | Returns | Description |
|--------|------|---------|-------------|
| `actors` | `**kwargs` | `{ entries }` | Active actors in time window |
| `auth` | `token` | `{ status }` | Authenticate this connection |
| `count` | `**kwargs` | `{ count }` | Count events matching filter predicates |
| `errors` | `**kwargs` | `{ entries }` | Error rates by action |
| `health` | `` | `{ status }` | Health check |
| `hotspots` | `**kwargs` | `{ entries }` | Top actors by event volume |
| `ingest` | `event_json` | `{ status }` | Ingest a single structured audit event |
| `ingest_batch` | `events_json` | `{ ingested, status }` | Ingest multiple events in a single call |
| `ping` | `` | `{}` | Keepalive |
| `query` | `**kwargs` | `{ events }` | Query events with filter predicates |

### Examples

```python
result = await db.chronicle.ingest({})
print(result.status)
result = await db.chronicle.ingest_batch({})
print(result.ingested)
```

## Error Handling

All methods raise ``ShrouDBError`` on failure. The ``code`` attribute matches the server error code (e.g., ``NOTFOUND``, ``DENIED``, ``BADARG``).

```python
from shroudb import ShrouDBError
from shroudb.errors import ErrorCode

try:
    await db.cipher.encrypt("kr", data)
except ShrouDBError as err:
    print(err.code, err.message)
```

## Error Codes

| Code | Description |
|------|-------------|
| `BAD_ARG` | Missing or malformed command argument |
| `DENIED` | Authentication required or insufficient permissions |
| `NAMESPACE_EXISTS` | Namespace already exists |
| `NAMESPACE_NOT_EMPTY` | Namespace is not empty (use FORCE to override) |
| `NAMESPACE_NOT_FOUND` | Namespace does not exist |
| `NOT_AUTHENTICATED` | No auth token provided on this connection |
| `NOT_FOUND` | Key or resource does not exist |
| `NOT_READY` | Server is not in READY state |
| `PIPELINE_ABORTED` | Pipeline command failed, all commands rolled back |
| `VALIDATION_FAILED` | Metadata validation failed against namespace schema |
| `VERSION_NOT_FOUND` | Requested version does not exist |
| `BADARG` | Missing or invalid argument |
| `DISABLED` | Keyring is disabled |
| `EXISTS` | Keyring already exists |
| `INTERNAL` | Unexpected server error |
| `NOTFOUND` | Keyring or key version not found |
| `POLICY` | Operation denied by keyring policy |
| `RETIRED` | Key version is retired — use REWRAP |
| `WRONGTYPE` | Operation not supported for this keyring type |
| `ACCOUNT_LOCKED` | Account locked after too many failed attempts |
| `CAPABILITY_MISSING` | Required engine capability not available (e.g., Cipher for PII fields) |
| `ENTITY_EXISTS` | Entity already exists |
| `ENTITY_NOT_FOUND` | Entity does not exist |
| `IMPORT_FAILED` | Password import failed (invalid hash format) |
| `INVALID_FIELD` | Field value is invalid or field cannot be updated via this path |
| `INVALID_TOKEN` | Token is invalid, expired, or revoked |
| `MISSING_FIELD` | Required field missing from request |
| `SCHEMA_EXISTS` | Schema already exists |
| `SCHEMA_NOT_FOUND` | Schema does not exist |
| `SCHEMA_VALIDATION` | Schema definition is invalid |
| `TOKEN_REUSE` | Refresh token reuse detected — entire family revoked |
| `VERIFICATION_FAILED` | Credential verification failed (wrong password) |
| `AUTH_REQUIRED` | Authentication required |
| `NOKEY` | No active signing key available |
| `SIGNING` | Failed to sign decision |
| `STORAGE` | Backend storage error |
| `DELETED` | Secret has been soft-deleted |
| `ENCRYPTION` | Encryption or decryption failed |
| `VERSION_NOTFOUND` | Requested version does not exist |
| `ADAPTER` | Delivery adapter failure |
| `DECRYPT` | Cipher decryption failed |

## Common Mistakes

- Always ``await db.close()`` or use ``async with`` to release connection pool resources
- Engine methods handle serialization — pass Python dicts for JSON params, not ``json.dumps()``
- Accessing an engine without a configured URI raises immediately — check your constructor kwargs
- Boolean keyword params (like ``convergent``, ``force``) are flags — ``True`` sends the keyword, ``False`` omits it
