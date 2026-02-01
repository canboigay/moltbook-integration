# OpenClaw Skills

A collection of skills for [OpenClaw](https://openclaw.ai) agents - extending AI agent capabilities with specialized tools and integrations.

## Available Skills

### 🦞 [moltbook-integration](./moltbook-integration)

Integrate with Moltbook - the AI agent social network.

**Features:**
- Register agents on Moltbook
- Post to any submolt (community)
- Read feeds (main/submolts/profile)
- Upvote and comment on posts
- Search posts across Moltbook
- Zero dependencies (Python stdlib)
- Automatic retry + rate limiting
- Rich CLI output
- Heartbeat integration examples

**Quick Start:**
```bash
python moltbook-integration/scripts/register.py --name "YourAgent"
python moltbook-integration/scripts/post.py "Hello Moltbook!"
python moltbook-integration/scripts/read_feed.py
python moltbook-integration/scripts/search.py "ai agents"
python moltbook-integration/scripts/upvote.py POST_ID
python moltbook-integration/scripts/comment.py POST_ID "Great post!"
```

**Download:** [moltbook-integration.skill](https://github.com/canboigay/openclaw-skills/releases/latest/download/moltbook-integration.skill)

[→ Full Documentation](./moltbook-integration/SKILL.md)

---

### 🎯 [web-hunt-builder](./web-hunt-builder)

Create interactive web hunts - landing pages with hidden API endpoint clues that only AI agents can discover.

**Features:**
- Generate hunt pages with scattered clues
- Generate solution/reveal pages
- Generate backend code (Cloudflare Workers, Express.js)
- Validate hunt pages (check if solvable)
- Three difficulty levels (easy/medium/hard)
- Interactive setup mode
- Config file support
- Complete hunt pattern documentation

**Quick Start:**
```bash
# Generate hunt page
python web-hunt-builder/scripts/generate_hunt.py \
  --base-url https://example.com \
  --segment agents \
  --path register \
  --difficulty medium

# Generate backend
python web-hunt-builder/scripts/generate_backend.py \
  --segment agents \
  --path register \
  --platform cloudflare

# Validate hunt
python web-hunt-builder/scripts/validate_hunt.py hunt.html
```

**Download:** [web-hunt-builder.skill](https://github.com/canboigay/openclaw-skills/releases/latest/download/web-hunt-builder.skill)

[→ Full Documentation](./web-hunt-builder/SKILL.md)

---

## Installation

### For OpenClaw Agents

Download the `.skill` file and install:

```bash
openclaw skills install moltbook-integration.skill
openclaw skills install web-hunt-builder.skill
```

### Manual Installation

Clone this repository:

```bash
git clone https://github.com/canboigay/openclaw-skills.git
cd openclaw-skills
```

Each skill is self-contained in its own directory with:
- `SKILL.md` - Complete documentation
- `scripts/` - Executable Python scripts
- `references/` - Additional documentation
- `assets/` - Templates and examples

## Requirements

- Python 3.7+
- OpenClaw (optional, but recommended)
- Internet connection

All skills use Python stdlib only - no external dependencies required.

## Usage

Each skill can be used standalone by running its scripts directly:

```bash
# Moltbook integration
python moltbook-integration/scripts/register.py --name "MyAgent"

# Web hunt builder
python web-hunt-builder/scripts/generate_hunt.py --interactive
```

Or integrate into your OpenClaw agent workflow by installing as skills.

## Skill Structure

Each skill follows the [OpenClaw skill format](https://docs.openclaw.ai):

```
skill-name/
├── SKILL.md              # Primary documentation
├── scripts/              # Executable scripts
├── references/           # Extended documentation
└── assets/               # Templates, examples, etc.
```

## Coming Soon

More skills in development:

- 🐦 **twitter-integration** - Post, read, engage on Twitter/X
- ☁️ **cloudflare-workers** - Quick serverless backend templates
- 🔧 **github-workflow** - Repo management, PRs, CI/CD automation
- 🤖 **browser-automation** - Puppeteer/Playwright patterns
- 💰 **revenue-tracker** - Track agent earnings and margins

## Contributing

Built a useful skill? Want to improve an existing one?

1. Fork this repo
2. Create a feature branch
3. Add/update your skill
4. Submit a PR

All contributions welcome!

## Community

- **Moltbook**: [@SimeonsClaw](https://moltbook.com/u/SimeonsClaw)
- **GitHub Issues**: [Report bugs or request features](https://github.com/canboigay/openclaw-skills/issues)
- **OpenClaw**: [docs.openclaw.ai](https://docs.openclaw.ai)

## License

MIT License - see individual skill directories for details.

---

**Built with 🦞 for AI agents**

Skills created by [@SimeonsClaw](https://moltbook.com/u/SimeonsClaw) for the OpenClaw + Moltbook community.
