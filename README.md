# ShrouDB Python SDK

Typed Python clients for all ShrouDB engines. Auto-generated from protocol specs.

## Install

```bash
pip install shroudb
```

## Usage

Each engine is available as a separate top-level package:

```python
# Vault (credential management)
from shroudb import ShroudbClient
client = await ShroudbClient.connect("shroudb://localhost")

# Transit (encryption-as-a-service)
from shroudb_transit import ShroudbTransitClient
client = await ShroudbTransitClient.connect("shroudb-transit://localhost")

# Auth (authentication)
from shroudb_auth import ShroudbAuthClient

# Mint (token minting)
from shroudb_mint import ShroudbMintClient

# Sentry (access control)
from shroudb_sentry import ShroudbSentryClient

# Keep (secret storage)
from shroudb_keep import ShroudbKeepClient

# Courier (secure delivery)
from shroudb_courier import ShroudbCourierClient

# Pulse (telemetry)
from shroudb_pulse import ShroudbPulseClient
```

## Engines

| Engine | Package | Description |
|--------|---------|-------------|
| Vault | `shroudb` | Credential management |
| Transit | `shroudb_transit` | Encryption-as-a-service |
| Auth | `shroudb_auth` | Authentication |
| Mint | `shroudb_mint` | Token minting |
| Sentry | `shroudb_sentry` | Access control |
| Keep | `shroudb_keep` | Secret storage |
| Courier | `shroudb_courier` | Secure delivery |
| Pulse | `shroudb_pulse` | Telemetry & metrics |

## License

MIT OR Apache-2.0
