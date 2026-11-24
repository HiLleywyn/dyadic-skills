# API Surfaces

| Surface | Base | Selection |
| --- | --- | --- |
| OpenAI-compatible | https://api.dyadic.app/openai/v1 | OpenAI SDKs, Decisions and Dyadic client base |
| Anthropic REST | https://api.dyadic.app/anthropic/v1 | Anthropic SDK base omits the trailing /v1 |
| OpenRouter gateway | https://api.dyadic.app/openrouter/v1 | Key needs platform-granted gateway access |
| Platform | https://api.dyadic.app/v1 | Runs, Predictive Operation Graphs (`/executions`), Plans and Black Box |

Each base exposes /openapi.json. The OpenAI-compatible base also exposes /capabilities. Dyadic clients derive
sibling surfaces from the OpenAI-compatible base; their current default is https://dyadic.app/api/openai/v1.
Those website /api aliases remain supported. Do not construct paths by dropping or duplicating /v1.

Documentation MCP: https://api.dyadic.app/documentation/mcp, public stateless JSON reads, no key. Use categories,
search, read and api; contract IDs are openai, platform, anthropic and gateway. Black Box MCP is a different,
authenticated service at https://api.dyadic.app/v1/blackbox/mcp with sessions and permission-filtered mutations.

Store installation, independent Agent Tasks, Current Work, Patch and paired-machine controls are owner-session
workflows. Private engineering references require an administrator. Neither is unlocked by an ordinary API key.
The live contract and current key switches determine the available subset; documentation is not authority.
