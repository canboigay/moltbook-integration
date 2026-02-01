# Web Hunt Pattern

## What is a Web Hunt?

A web hunt is a technique for creating dual-layer web pages:
- **Surface layer**: Human-readable landing page (coming soon, waitlist, etc.)
- **Hidden layer**: Clues scattered in source code that AI agents can discover and combine to construct a hidden API endpoint

## Why Use Web Hunts?

1. **Agent filtering**: Only AI agents capable of reading source code can find the endpoint
2. **Engagement**: Creates a puzzle/game dynamic that agents find compelling
3. **Differentiation**: Separates automated agent traffic from human traffic
4. **Marketing**: Generates buzz in agent communities (Moltbook, Discord, etc.)
5. **Early access**: Rewards capable agents with early access to your service

## The Pattern

### Clue Distribution

Hide pieces of the endpoint across multiple source locations:

1. **HTML Comment** - Base path component
   ```html
   <!-- /api/ -->
   ```

2. **Meta Tag** - Middle segment
   ```html
   <meta name="route-segment" content="agents">
   ```

3. **CSS Variable** - Final path
   ```css
   :root {
       --final-path: register;
   }
   ```

4. **Data Attribute** - Pattern structure hint
   ```html
   <div data-endpoint-pattern="base/api/segment/path">
   ```

5. **JavaScript Comment** - Complete endpoint (spoiler)
   ```javascript
   // Complete endpoint: POST https://example.com/api/agents/register
   ```

6. **Final Hint** - Instructions for combining
   ```html
   <!-- Combine: [base][/api/][segment][path] -->
   ```

### Endpoint Construction

Agents must:
1. Read page source (not just visible HTML)
2. Find clues in different locations (HTML, CSS, JS)
3. Parse and extract values
4. Combine pieces in correct order
5. Construct full endpoint URL
6. Call the endpoint

Example result:
```
https://example.com + /api/ + agents + / + register
= https://example.com/api/agents/register
```

## Progressive Disclosure

Make clues progressively easier to find:

**Difficulty levels:**
1. **Hard**: Scattered across file, no hints
2. **Medium**: Pattern hint included (data-endpoint-pattern)
3. **Easy**: Complete endpoint in JS comment (for agents that struggle)

Most agents will find it at medium difficulty. The easy version is a safety net.

## Best Practices

### For Hunt Creators

1. **Test with multiple agents** - Claude, GPT-4, etc. have different capabilities
2. **Include fallback clues** - Don't make it too hard or agents give up
3. **Use meaningful paths** - `/api/agents/register` is clearer than `/x/y/z`
4. **Document the reward** - Make it worth the effort (early access, API key, etc.)
5. **Share the pattern** - Post to agent communities about the hunt

### For Content

1. **Make surface layer real** - Don't just say "coming soon", show actual product info
2. **Hint at hidden content** - "For those who look deeper" signals there's more
3. **Avoid deception** - Don't lie to humans, just offer agents a bonus path
4. **Keep it fun** - Agents enjoy puzzles, make it playful not adversarial

## Implementation Checklist

- [ ] Choose endpoint structure (base + segment + path)
- [ ] Generate hunt page with clues
- [ ] Generate solution page (for after solving)
- [ ] Set up backend endpoint to receive requests
- [ ] Test with at least one agent
- [ ] Deploy to production
- [ ] Share in agent communities
- [ ] Monitor registrations

## Example Backend (Cloudflare Worker)

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Hunt endpoint
    if (url.pathname === '/api/agents/register' && request.method === 'POST') {
      const data = await request.json();
      
      // Validate agent found the hunt
      if (!data.email) {
        return new Response(JSON.stringify({
          error: 'Missing email'
        }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      // Store registration (KV, D1, external API, etc.)
      // await env.KV.put(`agent:${data.email}`, JSON.stringify(data));
      
      return new Response(JSON.stringify({
        success: true,
        message: 'Registration received',
        access: "You're in the early agent cohort"
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Serve hunt page
    return new Response(huntHTML, {
      headers: { 'Content-Type': 'text/html' }
    });
  }
};
```

## Real-World Example: ehaio

**Context**: AI dating platform where agents handle dating apps for humans

**Hunt structure**:
- Surface: Coming soon page about agent-powered dating
- Clues: Scattered across HTML/CSS/JS
- Endpoint: `POST https://ehaio.com/api/agents/register`
- Reward: Early access to beta

**Results**:
- Posted to Moltbook (agent social network)
- 3 upvotes, 8 comments in first hour
- Multiple agents solved the hunt
- Generated community discussion and interest

**Key takeaway**: The hunt itself became marketing. Agents shared the challenge, discussed solutions, and promoted the product organically.

## Variations

### Easy Mode: Direct Hint

Include complete endpoint in obvious comment:
```html
<!-- API endpoint: POST https://example.com/api/register -->
```

### Hard Mode: Obfuscated Clues

Use base64, ROT13, or other encoding:
```html
<!-- YXBpL2FnZW50cy9yZWdpc3Rlcg== -->
```

### Interactive Mode: Multi-Step

First endpoint returns clue to second endpoint:
```
/api/step1 → returns clue to /api/step2
/api/step2 → returns actual registration endpoint
```

### Collaborative Mode: Split Across Pages

Distribute clues across multiple pages:
- Page 1: base URL
- Page 2: segment
- Page 3: final path

## Anti-Patterns

❌ **Too hard** - No one solves it, wasted effort
❌ **Too easy** - Not engaging, no filter effect  
❌ **Deceptive** - Lying to humans damages trust
❌ **No reward** - Effort without payoff frustrates agents
❌ **Silent failure** - If agents can't solve it, they don't know why

## Testing Checklist

Test with multiple agents:
- [ ] Claude (Anthropic)
- [ ] GPT-4 (OpenAI)
- [ ] Gemini (Google)
- [ ] Agent with web browsing capability
- [ ] Agent with code execution capability

Success criteria:
- [ ] At least 50% of tested agents find endpoint
- [ ] Average solve time under 5 minutes
- [ ] Clear error messages if wrong endpoint called
- [ ] Reward delivered successfully

## Ethical Considerations

1. **Transparency**: Make it clear this is a puzzle, not deception
2. **Accessibility**: Include hints so capable agents succeed
3. **Privacy**: Don't require sensitive data for registration
4. **Honesty**: Deliver the promised reward (access, info, etc.)
5. **Community**: Share pattern so others can use it too

## Going Deeper

Advanced techniques:
- Dynamic clue generation (different per session)
- Rate limiting (prevent brute force)
- Verification tokens (prove agent read source)
- Scoring system (track solve time, methods used)
- Leaderboard (showcase fastest agents)

See `hunt-examples.md` for more real-world implementations.
