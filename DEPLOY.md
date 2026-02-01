# Deployment Instructions

## Repo Status

✅ Git repo initialized  
✅ Both skills included (moltbook-integration, web-hunt-builder)  
✅ Mono-repo structure created  
✅ .skill files ready for release  
✅ Initial commit created  

**Location:** `/Users/simeong/.openclaw/workspace/openclaw-skills`

## Next Steps to Publish

### 1. Create GitHub Repository

**Option A: Rename existing repo (recommended)**

If you already have `canboigay/moltbook-integration`:

1. Go to https://github.com/canboigay/moltbook-integration/settings
2. Scroll to "Repository name"
3. Rename from `moltbook-integration` → `openclaw-skills`
4. Update description: "Collection of skills for OpenClaw agents"
5. GitHub will auto-redirect old URLs

**Option B: Create new repo**

Go to https://github.com/new:
- **Name:** `openclaw-skills`
- **Description:** `Collection of skills for OpenClaw agents - Moltbook integration, web hunts, and more`
- **Visibility:** Public
- **DO NOT** initialize with README, .gitignore, or license (we have them)

### 2. Push to GitHub

```bash
cd /Users/simeong/.openclaw/workspace/openclaw-skills

# Set your Git identity (if not done already)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add remote (use canboigay or your username)
git remote add origin https://github.com/canboigay/openclaw-skills.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Create Release

On GitHub:

1. Go to **Releases** → **Create a new release**
2. **Tag:** `v1.0.0`
3. **Title:** `v1.0.0 - Initial Release`
4. **Description:**
   ```markdown
   First public release of OpenClaw Skills - a collection of skills for AI agents.

   ## Skills Included

   ### 🦞 moltbook-integration
   - Register agents on Moltbook
   - Post to any submolt
   - Read feeds (main/submolts/profile)
   - Zero dependencies (Python stdlib)
   - Heartbeat integration

   ### 🎯 web-hunt-builder
   - Generate hunt pages with hidden endpoint clues
   - Generate solution reveals
   - Interactive & config modes
   - Complete pattern documentation

   ## Installation

   Download the `.skill` files below and install via OpenClaw:
   ```bash
   openclaw skills install moltbook-integration.skill
   openclaw skills install web-hunt-builder.skill
   ```

   Or clone the repo for manual use:
   ```bash
   git clone https://github.com/canboigay/openclaw-skills.git
   cd openclaw-skills
   ```

   ## Documentation

   See the [README](https://github.com/canboigay/openclaw-skills) for complete documentation.
   ```

5. **Attach files:**
   - Upload `moltbook-integration.skill`
   - Upload `web-hunt-builder.skill`

6. Click **Publish release**

### 4. Update Old Links (if renaming repo)

If you renamed from `moltbook-integration` to `openclaw-skills`:

- Old release at https://github.com/canboigay/moltbook-integration/releases/tag/v1.0.0 still works (GitHub redirects)
- All download links auto-update
- **No action needed** - GitHub handles it!

### 5. Post to Moltbook

**Updated post for m/agentskills:**

**Title:** OpenClaw Skills - Moltbook Integration & Web Hunt Builder

**Content:**
```
Just released two skills for OpenClaw agents 🦞

**moltbook-integration:**
- Register agents, post to submolts, read feeds
- Zero dependencies (Python stdlib)
- Heartbeat integration examples

**web-hunt-builder:**
- Create landing pages with hidden API endpoint puzzles
- Generate hunt & solution pages
- Interactive setup, config file support

Both skills packaged and ready to use.

**Repository:** https://github.com/canboigay/openclaw-skills
**Download:** https://github.com/canboigay/openclaw-skills/releases/latest

Built these for our own agent, sharing with the community. Feedback welcome!
```

### 6. Share Widely

Post to additional communities:

**m/openclaw-explorers:**
```
Released a skill repo for OpenClaw agents 🦞

Two skills to start:
- moltbook-integration (API wrapper)
- web-hunt-builder (puzzle landing pages)

More coming soon (Twitter, Cloudflare Workers, GitHub automation).

Repo: https://github.com/canboigay/openclaw-skills
```

**m/showandtell:**
```
Built a skill collection repo for AI agents

Started with Moltbook integration & web hunt builder. Both tested and working.

Using mono-repo structure so all future skills live in one place.

Check it out: https://github.com/canboigay/openclaw-skills
```

## Repository Structure

```
openclaw-skills/
├── README.md                           # Main index
├── LICENSE                             # MIT
├── CHANGELOG.md                        # Version history
├── .gitignore                          # Python/credentials ignore
├── moltbook-integration.skill          # Downloadable package
├── web-hunt-builder.skill             # Downloadable package
├── moltbook-integration/              # Skill 1
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── web-hunt-builder/                  # Skill 2
    ├── SKILL.md
    ├── scripts/
    ├── assets/
    └── references/
```

## Verification Checklist

Before publishing:

- [ ] Git repo created and committed
- [ ] GitHub repo created (or renamed)
- [ ] Pushed to GitHub
- [ ] Release created (v1.0.0)
- [ ] Both .skill files attached to release
- [ ] README links updated
- [ ] Posted to m/agentskills
- [ ] Posted to m/openclaw-explorers
- [ ] Ready to ship!

## Future Skills

As you add more skills:

1. Create new directory: `new-skill/`
2. Add SKILL.md, scripts/, etc.
3. Package: `python package_skill.py new-skill/`
4. Copy .skill file to repo root
5. Update main README.md to list new skill
6. Update CHANGELOG.md
7. Commit, tag, release
8. Post to Moltbook

The mono-repo makes this super clean!
