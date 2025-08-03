# Atlas Sync Tool Evaluation

This document evaluates potential technologies for the 'Atlas' concept, which aims to synchronize state and tasks across different machines.

| Tool | Data Model | Real-time Sync | Free Tier/Pricing | Ease of Integration (Python support) |
|---|---|---|---|---|
| **LiveStore** | Event-sourcing with embedded SQLite | Yes | Open-source | Python support is not explicitly mentioned, but since it uses SQLite, it should be possible to interact with the database from Python. |
| **Zero** | Client-side cache of server data | Yes | Open-source | Python support is not explicitly mentioned. The focus is on a client-side JavaScript/TypeScript API. |
| **Convex** | Reactive database with serverless functions | Yes | Managed cloud platform with a free tier, and open-source for self-hosting. | Convex has a Python client library, making it easy to integrate with our existing Python codebase. |

## Recommendation

Based on this evaluation, **Convex** is the recommended tool for a proof-of-concept of the Atlas sync concept. It has a Python client, a generous free tier, and is open-source for self-hosting, which makes it a flexible and low-risk option.
