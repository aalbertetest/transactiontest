'use strict';

/**
 * VULNERABLE FILE UPLOAD SERVER
 * =============================
 * This server intentionally contains security vulnerabilities for educational
 * purposes. DO NOT deploy this in production. Each vulnerability is marked
 * with a [VULN-N] tag for cross-reference with SECURITY_ANALYSIS.md.
 */

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();

// ─── [VULN-1] PATH TRAVERSAL ───────────────────────────────────────────────
// The filename from the user is used directly without sanitization.
// An attacker can craft a filename like "../../etc/cron.d/backdoor" to write
// files anywhere on the filesystem the process has access to.
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname); // Trusts user-supplied filename
  },
});

// ─── [VULN-2] NO FILE TYPE VALIDATION ───────────────────────────────────────
// No fileFilter is set on multer. Any file type is accepted, including
// executable scripts (.php, .sh, .exe, .jsp), HTML files that could enable
// stored XSS, and polyglot files that bypass extension-based checks.
// Additionally, no file size limit is configured, enabling denial-of-service
// via arbitrarily large uploads.
const upload = multer({ storage });

// ─── [VULN-3] SERVING UPLOADS AS STATIC FILES WITH EXECUTION CONTEXT ──────
// Uploaded files are served directly from the uploads directory with no
// Content-Disposition header forcing download. Combined with no file type
// validation, an attacker can upload an HTML file containing JavaScript,
// which will execute in the victim's browser when they visit the URL
// (Stored XSS). If the server also runs a PHP/JSP engine, uploaded scripts
// could achieve Remote Code Execution.
app.use('/uploads', express.static('uploads'));

// ─── [VULN-4] NO RATE LIMITING ─────────────────────────────────────────────
// No rate limiting is applied to any endpoint. An attacker can:
// - Flood the upload endpoint to exhaust disk space (DoS)
// - Brute-force filenames via the download endpoint
// - Overload the server with concurrent requests
app.post('/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // ─── [VULN-5] INFORMATION DISCLOSURE ────────────────────────────────────
  // The response leaks internal server paths, original filename, and storage
  // details. This gives attackers a roadmap of the server's file system
  // structure and confirms that path traversal payloads landed correctly.
  res.json({
    message: 'File uploaded successfully',
    file: {
      originalName: req.file.originalname,
      storedPath: req.file.path,         // Leaks absolute/relative server path
      destination: req.file.destination,  // Leaks upload directory structure
      size: req.file.size,
      mimetype: req.file.mimetype,       // User-controlled MIME type
    },
  });
});

// ─── [VULN-1 continued] PATH TRAVERSAL IN DOWNLOAD ─────────────────────────
// The filename parameter is concatenated directly into a file path.
// An attacker can request /download?filename=../../etc/passwd to read
// arbitrary files from the server.
app.get('/download', (req, res) => {
  const filename = req.query.filename;
  if (!filename) {
    return res.status(400).json({ error: 'Filename required' });
  }

  const filePath = path.join(__dirname, 'uploads', filename);

  // No validation that the resolved path stays within the uploads directory
  if (fs.existsSync(filePath)) {
    res.download(filePath);
  } else {
    res.status(404).json({ error: 'File not found' });
  }
});

// List all uploaded files (also leaks directory contents)
app.get('/files', (req, res) => {
  const uploadsDir = path.join(__dirname, 'uploads');
  if (!fs.existsSync(uploadsDir)) {
    return res.json({ files: [] });
  }
  const files = fs.readdirSync(uploadsDir);
  res.json({ files });
});

// ─── [VULN-6] VERBOSE ERROR HANDLING ────────────────────────────────────────
// Stack traces and internal error details are sent to the client, helping
// attackers fingerprint the framework, Node.js version, and file paths.
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

// Ensure uploads directory exists
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[VULNERABLE] Server running on port ${PORT}`);
  console.log('WARNING: This server contains intentional security vulnerabilities.');
  console.log('Do NOT use in production.');
});

module.exports = app;
