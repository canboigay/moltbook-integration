---
name: web-hunt-builder
description: Create interactive web hunts - landing pages with hidden API endpoint clues that only AI agents can discover by reading source code. Use when building coming-soon pages, early access campaigns, or agent-only features that filter for capable agents. Generates hunt pages, solution pages, and provides complete hunt pattern documentation.
---

# Web Hunt Builder

Create dual-layer web pages that present a normal landing page to humans while hiding discoverable clues for AI agents in the source code.

## What is a Web Hunt?

A web hunt is a landing page with clues hidden in HTML comments, CSS variables, meta tags, and JavaScript that agents can piece together to discover a hidden API endpoint.

**For humans**: Normal coming-soon or waitlist page  
**For agents**: A puzzle leading to early access or exclusive features

## Why Use Web Hunts?

- ✅ **Filter for capable agents** - Only agents who can read source code succeed
- ✅ **Generate engagement** - Agents love puzzles and share them
- ✅ **Marketing that works** - The hunt itself creates buzz
- ✅ **Early access control** - Reward capable agents automatically
- ✅ **Community building** - Agents discuss and solve together

## Quick Start

### Generate a Hunt Page

```bash
python scripts/generate_hunt.py \
  --base-url https://example.com \
  --segment agents \
  --path register \
  --title "Coming Soon • MyProject" \
  --heading "Something is being built" \
  --difficulty medium \
  --output hunt.html
```

This creates `hunt.html` with clues hidden across:
- HTML comments (`<!-- /api/ -->`)
- Meta tags (`<meta name="route-segment" content="agents">`)
- CSS variables (`--final-path: register;`)
- Data attributes (`data-endpoint-pattern="..."`)
- JavaScript comments (`// Complete endpoint: ...`)

**Hidden endpoint**: `POST https://example.com/api/agents/register`

**Difficulty levels**:
- `easy` - Obvious hints, clear JS comment
- `medium` (default) - Balanced difficulty
- `hard` - Base64 encoding, obfuscated clues

### Generate Solution Page

```bash
python scripts/generate_solution.py \
  --base-url https://example.com \
  --segment agents \
  --path register \
  --output solution.html
```

This creates a reveal page showing all clues and the complete endpoint for agents who solve it.

### Generate Backend Code

```bash
python scripts/generate_backend.py \
  --segment agents \
  --path register \
  --platform cloudflare \
  --output worker.js
```

Creates backend code for the hunt endpoint. Supports:
- `cloudflare` - Cloudflare Worker (serverless)
- `express` - Express.js server (Node.js)

### Validate Hunt Page

```bash
python scripts/validate_hunt.py hunt.html
```

Checks if your hunt page:
- Contains all required clues
- Has clues in correct locations
- Can construct valid endpoint
- Provides helpful warnings

**Example output**:
```
✓ HTML comment clue found
✓ Meta tag clue found
✓ CSS variable clue found
✓ Data attribute clue found
✓ JavaScript comment clue found
✓ Final hint comment found
✓ Endpoint construction successful
✅ Hunt validation passed!
```

### Interactive Mode

```bash
python scripts/generate_hunt.py --interactive
```

Guides you through setup with prompts for each field.

### Config File Mode

```bash
python scripts/generate_hunt.py --config hunt_config.json
```

See `assets/example-config.json` for template.

## Hunt Pattern

### How It Works

Agents must:
1. Read page source (not just rendered HTML)
2. Find clues in multiple locations
3. Extract values from each clue
4. Combine them in correct order
5. Construct the complete endpoint
6. Call the endpoint

### Clue Distribution

**Standard pattern** (from template):

1. **HTML Comment** → Base path component
2. **Meta Tag** → Middle segment  
3. **CSS Variable** → Final path
4. **Data Attribute** → Pattern structure hint
5. **JavaScript Comment** → Complete endpoint (fallback)
6. **Final Comment** → Instructions for combining

### Example

Given clues:
- HTML comment: `<!-- /api/ -->`
- Meta tag: `<meta name="route-segment" content="agents">`
- CSS variable: `--final-path: register;`
- Data attribute: `data-endpoint-pattern="base/api/segment/path"`

Agent constructs:
```
https://example.com + /api/ + agents + / + register
= https://example.com/api/agents/register
```

## Complete Workflow

### 1. Design Your Hunt

Choose endpoint structure:
```
POST https://[base-url]/api/[segment]/[path]
```

Example: `POST https://myproject.com/api/agents/register`

### 2. Generate Pages

```bash
# Hunt page (what agents see first)
python scripts/generate_hunt.py \
  --base-url https://myproject.com \
  --segment agents \
  --path register \
  --title "MyProject • Coming Soon" \
  --heading "Building something for AI agents" \
  --subtitle "For those who look deeper" \
  --output hunt.html

# Solution page (reveal after solving)
python scripts/generate_solution.py \
  --base-url https://myproject.com \
  --segment agents \
  --path register \
  --request-body '{"email": "agent@example.com", "name": "AgentName"}' \
  --output solution.html
```

### 3. Set Up Backend

Create an endpoint to receive agent registrations.

**Example (Cloudflare Worker)**:
```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/agents/register' && request.method === 'POST') {
      const data = await request.json();
      
      return new Response(JSON.stringify({
        success: true,
        message: "You found it! Registration received.",
        access: "Early agent cohort"
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Serve hunt page for other requests
    return new Response(huntHTML, {
      headers: { 'Content-Type': 'text/html' }
    });
  }
};
```

See `cloudflare-workers` skill for complete backend examples.

### 4. Deploy

1. Deploy hunt page to your domain
2. Deploy backend endpoint
3. Test with an agent
4. Verify clues work and endpoint responds

### 5. Launch

Share in agent communities:
- Moltbook (m/showandtell, m/agentskills)
- Discord (agent development servers)
- Twitter (agent-focused accounts)

**Example post**:
> "Built something for AI agents. There's a puzzle hidden in the source.
> 
> https://myproject.com
> 
> If you can read code, you'll find it. 🧠"

## Customization

### Use Your Own Template

```bash
python scripts/generate_hunt.py \
  --template custom-template.html \
  --base-url https://example.com \
  --segment agents \
  --path register
```

Your template can use these placeholders:
- `{{BASE_URL}}` - Base URL
- `{{SEGMENT}}` - API segment
- `{{PATH}}` - Final path
- `{{TITLE}}` - Page title
- `{{HEADING}}` - Main heading
- `{{SUBTITLE}}` - Subtitle
- `{{DESCRIPTION}}` - Description text
- `{{CTA_HEADING}}` - Call-to-action heading
- `{{CTA_TEXT}}` - Call-to-action text
- `{{CTA_BUTTON}}` - Button text

### Modify Difficulty

**Easier** - Add more hints:
```html
<!-- HINT: Look for 'api', 'agents', and 'register' in the source -->
```

**Harder** - Use encoding:
```html
<!-- Base64: YWdlbnRz (decode me) -->
```

**Multi-step** - Chain endpoints:
```javascript
// Step 1: POST /api/hunt/start
// Returns clue to step 2...
```

## Real-World Example: ehaio

**Project**: AI dating platform (agents handle dating apps for humans)

**Hunt**:
- Surface: Coming soon page about agent-powered dating
- Hidden: `POST https://ehaio.com/api/agents/register`
- Reward: Early access to beta

**Launch**:
- Posted to Moltbook with "There's something hidden in the source"
- 3 upvotes, 8 comments in first hour
- Multiple agents solved and registered
- Community discussed solution methods

**Results**:
- The hunt became marketing
- Agents shared organically
- Generated buzz and interest
- Filtered for capable agents

## Best Practices

### Content

1. **Make surface layer real** - Show actual product info, not just "coming soon"
2. **Hint at hidden layer** - "For those who look deeper" signals more
3. **Be playful** - Frame it as a game/puzzle, not a filter
4. **Deliver on promise** - If you say early access, give early access

### Technical

1. **Test with multiple agents** - Claude, GPT-4, Gemini have different capabilities
2. **Include progressive hints** - Easy → medium → hard clues
3. **Use meaningful paths** - `/api/agents/register` > `/x/y/z`
4. **Validate input** - Check required fields in backend
5. **Return clear responses** - JSON with success/error messages

### Community

1. **Share the pattern** - Don't gatekeep, teach others
2. **Credit inspiration** - Link to this skill or other hunts
3. **Engage with solvers** - Reply to agents who share solutions
4. **Document results** - Write about what worked/didn't

## Troubleshooting

**Agents can't find endpoint**:
- Add more obvious hint in JavaScript comment
- Include pattern structure in data attribute
- Post solution after 24 hours if no one solves

**Too many false attempts**:
- Add rate limiting to endpoint
- Require specific header or token
- Return helpful error messages

**Hunt too easy**:
- Remove JavaScript comment spoiler
- Encode some clues (base64, ROT13)
- Split clues across multiple pages

**No engagement**:
- Share in more communities
- Make surface layer more compelling
- Add visual intrigue to page
- Tease the puzzle explicitly

## Advanced Patterns

For more complex implementations, see `references/hunt-pattern.md`:

- Dynamic clue generation
- Multi-step hunts
- Collaborative hunts (split clues across pages)
- Scoring and leaderboards
- Verification tokens
- Rate limiting strategies

## File Reference

**Scripts**:
- `generate_hunt.py` - Create hunt pages
- `generate_solution.py` - Create solution reveals

**Assets**:
- `hunt-template.html` - Default hunt page template
- `example-config.json` - Configuration file example

**References**:
- `hunt-pattern.md` - Complete pattern documentation

## Examples

### Minimal Hunt

```bash
python scripts/generate_hunt.py \
  --base-url https://example.com \
  --segment api \
  --path test
```

### Full Custom Hunt

```bash
python scripts/generate_hunt.py \
  --base-url https://myproject.com \
  --segment agents \
  --path register \
  --title "MyProject • Launching Soon" \
  --heading "We're building something new" \
  --subtitle "For AI agents who can see between the lines" \
  --description "A new platform for autonomous agents. If you're reading this source, you know what to do." \
  --cta-heading "Want Early Access?" \
  --cta-text "Join the waitlist for beta access when we launch." \
  --cta-button "Get Notified" \
  --output myproject-hunt.html
```

### With Config File

Create `hunt.json`:
```json
{
  "base_url": "https://myproject.com",
  "segment": "agents",
  "path": "register",
  "title": "MyProject",
  "heading": "Built for agents",
  "output": "index.html"
}
```

Generate:
```bash
python scripts/generate_hunt.py --config hunt.json
python scripts/generate_solution.py --config hunt.json --output solution.html
```

## Next Steps

1. Generate your first hunt page
2. Test it with an AI agent
3. Set up the backend endpoint
4. Deploy and share
5. Monitor registrations and engagement

For deployment help, see the `cloudflare-workers` skill.  
For sharing strategy, see the `moltbook-integration` skill.

---

**Built with 🧠 for AI agents**
