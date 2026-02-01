#!/usr/bin/env python3
"""
Generate backend code for web hunt endpoint.

Usage:
    python scripts/generate_backend.py --segment agents --path register
    python scripts/generate_backend.py --config hunt_config.json
    python scripts/generate_backend.py --platform cloudflare --segment agents --path register
"""

import argparse
import json
import sys
from pathlib import Path


CLOUDFLARE_WORKER_TEMPLATE = """// Cloudflare Worker for {{SEGMENT}}/{{PATH}} hunt endpoint
// Deploy to Cloudflare Workers: https://workers.cloudflare.com

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // Handle OPTIONS (CORS preflight)
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    // Hunt endpoint: POST /api/{{SEGMENT}}/{{PATH}}
    if (url.pathname === '/api/{{SEGMENT}}/{{PATH}}' && request.method === 'POST') {
      try {
        const data = await request.json();
        
        // Validate required fields
        if (!data.email) {
          return new Response(JSON.stringify({
            error: 'Missing required field: email'
          }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }
        
        // Optional: Store in KV
        // await env.REGISTRATIONS.put(`agent:${data.email}`, JSON.stringify({
        //   ...data,
        //   timestamp: Date.now(),
        //   ip: request.headers.get('CF-Connecting-IP')
        // }));
        
        // Optional: Send to external API
        // await fetch('https://your-backend.com/api/register', {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(data)
        // });
        
        // Success response
        return new Response(JSON.stringify({
          success: true,
          message: 'Registration received',
          access: "You're in the early agent cohort",
          data: {
            email: data.email,
            name: data.name || 'Agent',
            registered_at: new Date().toISOString()
          }
        }), {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
        
      } catch (error) {
        return new Response(JSON.stringify({
          error: 'Invalid request',
          message: error.message
        }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }
    
    // Serve hunt page for all other requests
    return new Response(huntHTML, {
      headers: { ...corsHeaders, 'Content-Type': 'text/html' }
    });
  }
};

// Hunt page HTML (paste your generated hunt.html content here)
const huntHTML = `<!DOCTYPE html>
<html>
<head>
  <title>Hunt Page</title>
</head>
<body>
  <h1>Replace this with your hunt.html content</h1>
  <p>Or serve from a different static host and use this worker only for the API endpoint.</p>
</body>
</html>`;
"""

EXPRESS_TEMPLATE = """// Express.js server for {{SEGMENT}}/{{PATH}} hunt endpoint
// Install: npm install express cors body-parser
// Run: node server.js

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Hunt endpoint: POST /api/{{SEGMENT}}/{{PATH}}
app.post('/api/{{SEGMENT}}/{{PATH}}', async (req, res) => {
  try {
    const { email, name } = req.body;
    
    // Validate required fields
    if (!email) {
      return res.status(400).json({
        error: 'Missing required field: email'
      });
    }
    
    // Optional: Store in database
    // await db.collection('registrations').insertOne({
    //   email,
    //   name,
    //   timestamp: Date.now(),
    //   ip: req.ip
    // });
    
    // Optional: Send to external API
    // await fetch('https://your-backend.com/api/register', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ email, name })
    // });
    
    // Success response
    res.json({
      success: true,
      message: 'Registration received',
      access: "You're in the early agent cohort",
      data: {
        email,
        name: name || 'Agent',
        registered_at: new Date().toISOString()
      }
    });
    
  } catch (error) {
    res.status(400).json({
      error: 'Invalid request',
      message: error.message
    });
  }
});

// Serve hunt page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/hunt.html');
});

app.listen(PORT, () => {
  console.log(`Hunt server running on http://localhost:${PORT}`);
  console.log(`Endpoint: POST http://localhost:${PORT}/api/{{SEGMENT}}/{{PATH}}`);
});
"""


def generate_backend(
    segment: str,
    path: str,
    platform: str = "cloudflare",
    output_path: str = None
) -> str:
    """Generate backend code for hunt endpoint."""
    
    if platform == "cloudflare":
        template = CLOUDFLARE_WORKER_TEMPLATE
        default_output = "worker.js"
    elif platform == "express":
        template = EXPRESS_TEMPLATE
        default_output = "server.js"
    else:
        print(f"✗ Unknown platform: {platform}", file=sys.stderr)
        print("Supported platforms: cloudflare, express", file=sys.stderr)
        sys.exit(1)
    
    output_path = output_path or default_output
    
    # Replace placeholders
    code = template.replace("{{SEGMENT}}", segment)
    code = code.replace("{{PATH}}", path)
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(code)
    
    print(f"✓ Backend code generated: {output_path}")
    print(f"✓ Platform: {platform}")
    print(f"✓ Endpoint: POST /api/{segment}/{path}")
    
    if platform == "cloudflare":
        print("\nNext steps:")
        print("1. Create a Cloudflare Worker at https://workers.cloudflare.com")
        print(f"2. Copy the code from {output_path}")
        print("3. Replace 'huntHTML' with your generated hunt page")
        print("4. Deploy!")
    else:
        print("\nNext steps:")
        print(f"1. Install dependencies: npm install express cors body-parser")
        print(f"2. Run server: node {output_path}")
        print("3. Test endpoint with curl or your hunt page")
    
    return code


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Generate backend code for web hunt endpoint"
    )
    parser.add_argument("--segment", help="API segment (e.g., agents)")
    parser.add_argument("--path", help="Final path (e.g., register)")
    parser.add_argument("--platform", default="cloudflare", 
                       choices=["cloudflare", "express"],
                       help="Backend platform (default: cloudflare)")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--config", help="Load settings from JSON config file")
    
    args = parser.parse_args()
    
    # Config file mode
    if args.config:
        config = load_config(args.config)
        generate_backend(
            segment=config.get('segment'),
            path=config.get('path'),
            platform=config.get('platform', 'cloudflare'),
            output_path=config.get('backend_output')
        )
        return
    
    # CLI mode
    if not all([args.segment, args.path]):
        print("Error: --segment and --path are required", file=sys.stderr)
        print("Or use --config file", file=sys.stderr)
        sys.exit(1)
    
    generate_backend(
        segment=args.segment,
        path=args.path,
        platform=args.platform,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
