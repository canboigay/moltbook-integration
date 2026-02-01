# Changelog

All notable changes to OpenClaw Skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-31

### Added

#### moltbook-integration
- Agent registration script (`register.py`)
- Post creation script (`post.py`)
- Feed reading script (`read_feed.py`)
- **Upvote script** (`upvote.py`) - upvote posts with retry logic
- **Comment script** (`comment.py`) - comment on posts
- **Search script** (`search.py`) - full-text search across Moltbook
- Complete API reference documentation
- Heartbeat integration examples
- Community etiquette guidelines
- Zero-dependency implementation (Python stdlib only)

**Technical improvements**:
- Automatic retry with exponential backoff
- Rate limit handling (429 errors)
- Rich formatted CLI output
- URL parsing support (accept post URLs or IDs)
- Better error messages

#### web-hunt-builder
- Hunt page generator (`generate_hunt.py`)
- Solution page generator (`generate_solution.py`)
- **Backend code generator** (`generate_backend.py`) - Cloudflare Workers & Express.js
- **Hunt validator** (`validate_hunt.py`) - verify hunts are solvable
- **Difficulty levels** - easy/medium/hard with varying obfuscation
- Customizable HTML template
- Interactive setup mode
- Config file support
- Complete hunt pattern documentation
- Example configurations

**Technical improvements**:
- Three difficulty levels (easy/medium/hard)
- Base64 encoding for hard mode
- Backend template generation
- Hunt validation before deployment
- Better error handling

### Features
- Mono-repo structure for all OpenClaw skills
- Individual .skill files for easy download
- Comprehensive documentation
- Production-ready features (retry logic, rate limiting, validation)
- MIT License

[1.0.0]: https://github.com/canboigay/openclaw-skills/releases/tag/v1.0.0
