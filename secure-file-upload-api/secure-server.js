'use strict';

/**
 * PRODUCTION-READY SECURE FILE UPLOAD SERVER
 * ==========================================
 * This server demonstrates proper secure coding practices for file uploads.
 * Each fix is tagged with [FIX-N] corresponding to the vulnerability it
 * addresses in vulnerable-server.js and SECURITY_ANALYSIS.md.
 */

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// ─── [FIX-6] SECURITY HEADERS ──────────────────────────────────────────────
// helmet() sets dozens of HTTP security headers: X-Content-Type-Options,
// X-Frame-Options, Strict-Transport-Security, Content-Security-Policy, etc.
app.use(helmet());
app.disable('x-powered-by');

// ─── [FIX-4] RATE LIMITING ─────────────────────────────────────────────────
// Global rate limiter prevents abuse across all endpoints.
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15-minute window
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' },
});
app.use(globalLimiter);

// Stricter rate limiter specifically for the upload endpoint.
const uploadLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Upload limit exceeded. Try again later.' },
});

// ─── CONFIGURATION ──────────────────────────────────────────────────────────
const UPLOAD_DIR = path.resolve(__dirname, 'secure-uploads');
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB
const ALLOWED_MIME_TYPES = new Set([
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'application/pdf',
  'text/plain',
]);
const ALLOWED_EXTENSIONS = new Set([
  '.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf', '.txt',
]);

// ─── [FIX-1] SAFE FILENAME GENERATION ──────────────────────────────────────
// Instead of trusting user-supplied filenames, generate a cryptographically
// random filename and preserve only the validated file extension.
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();

    if (!ALLOWED_EXTENSIONS.has(ext)) {
      return cb(new Error(`File extension "${ext}" is not allowed`));
    }

    const randomName = crypto.randomBytes(32).toString('hex');
    cb(null, `${randomName}${ext}`);
  },
});

// ─── [FIX-2] FILE TYPE VALIDATION + SIZE LIMIT ─────────────────────────────
// Validates MIME type in the fileFilter AND enforces a maximum file size.
const upload = multer({
  storage,
  limits: {
    fileSize: MAX_FILE_SIZE,
    files: 1,
    fields: 5,
  },
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();

    if (!ALLOWED_MIME_TYPES.has(file.mimetype)) {
      return cb(new Error(`MIME type "${file.mimetype}" is not allowed`));
    }

    if (!ALLOWED_EXTENSIONS.has(ext)) {
      return cb(new Error(`File extension "${ext}" is not allowed`));
    }

    cb(null, true);
  },
});

// ─── [FIX-3] NO STATIC FILE SERVING OF UPLOADS ─────────────────────────────
// Uploads are NEVER served via express.static(). Instead, a controlled
// download endpoint validates the requested filename and forces a
// Content-Disposition: attachment header so browsers download rather than
// render the content.

// ─── FILENAME SANITIZATION UTILITY ──────────────────────────────────────────
function sanitizeFilename(filename) {
  if (!filename || typeof filename !== 'string') {
    return null;
  }

  const basename = path.basename(filename);

  // Only allow alphanumeric characters, hyphens, underscores, and a single dot
  if (!/^[a-zA-Z0-9_-]+\.[a-zA-Z0-9]+$/.test(basename)) {
    return null;
  }

  return basename;
}

// ─── MAGIC BYTES VALIDATION ─────────────────────────────────────────────────
// Verifies that the file's actual content matches its claimed extension by
// reading magic bytes (file signatures). This catches polyglot attacks where
// a .jpg extension actually contains a PHP script.
const MAGIC_BYTES = {
  '.jpg':  [Buffer.from([0xFF, 0xD8, 0xFF])],
  '.jpeg': [Buffer.from([0xFF, 0xD8, 0xFF])],
  '.png':  [Buffer.from([0x89, 0x50, 0x4E, 0x47])],
  '.gif':  [Buffer.from([0x47, 0x49, 0x46, 0x38])],
  '.webp': [Buffer.from([0x52, 0x49, 0x46, 0x46])], // RIFF header
  '.pdf':  [Buffer.from([0x25, 0x50, 0x44, 0x46])],  // %PDF
};

async function validateMagicBytes(filePath, extension) {
  const signatures = MAGIC_BYTES[extension];
  if (!signatures) {
    return true; // .txt files have no fixed signature
  }

  const fd = await fs.promises.open(filePath, 'r');
  try {
    const maxLen = Math.max(...signatures.map(s => s.length));
    const buffer = Buffer.alloc(maxLen);
    await fd.read(buffer, 0, maxLen, 0);

    return signatures.some(sig => buffer.subarray(0, sig.length).equals(sig));
  } finally {
    await fd.close();
  }
}

// ─── UPLOAD ENDPOINT ────────────────────────────────────────────────────────
app.post('/upload', uploadLimiter, (req, res, next) => {
  upload.single('file')(req, res, async (err) => {
    if (err) {
      if (err instanceof multer.MulterError) {
        if (err.code === 'LIMIT_FILE_SIZE') {
          return res.status(413).json({ error: `File exceeds maximum size of ${MAX_FILE_SIZE / 1024 / 1024}MB` });
        }
        return res.status(400).json({ error: 'Upload error occurred' });
      }
      return res.status(400).json({ error: err.message });
    }

    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    try {
      const ext = path.extname(req.file.filename).toLowerCase();
      const isValidContent = await validateMagicBytes(req.file.path, ext);

      if (!isValidContent) {
        await fs.promises.unlink(req.file.path);
        return res.status(400).json({
          error: 'File content does not match its extension',
        });
      }

      // ─── [FIX-5] MINIMAL INFORMATION DISCLOSURE ───────────────────────
      // Only return the generated filename (no server paths, no internals).
      res.status(201).json({
        message: 'File uploaded successfully',
        file: {
          id: path.basename(req.file.filename, ext),
          filename: req.file.filename,
          size: req.file.size,
        },
      });
    } catch (error) {
      if (req.file?.path) {
        await fs.promises.unlink(req.file.path).catch(() => {});
      }
      next(error);
    }
  });
});

// ─── [FIX-1] SAFE DOWNLOAD ENDPOINT ────────────────────────────────────────
// Validates that the resolved path is within the uploads directory, preventing
// path traversal. Forces download via Content-Disposition: attachment.
app.get('/download/:filename', (req, res) => {
  const sanitized = sanitizeFilename(req.params.filename);
  if (!sanitized) {
    return res.status(400).json({ error: 'Invalid filename' });
  }

  const filePath = path.resolve(UPLOAD_DIR, sanitized);

  // Ensure the resolved path is still within the upload directory
  if (!filePath.startsWith(UPLOAD_DIR + path.sep)) {
    return res.status(403).json({ error: 'Access denied' });
  }

  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'File not found' });
  }

  res.setHeader('Content-Disposition', `attachment; filename="${sanitized}"`);
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.sendFile(filePath);
});

// ─── FILE LISTING (limited info) ────────────────────────────────────────────
app.get('/files', (req, res) => {
  if (!fs.existsSync(UPLOAD_DIR)) {
    return res.json({ files: [] });
  }

  const files = fs.readdirSync(UPLOAD_DIR)
    .filter(f => !f.startsWith('.'))
    .map(f => {
      const stats = fs.statSync(path.join(UPLOAD_DIR, f));
      return {
        filename: f,
        size: stats.size,
        uploadedAt: stats.birthtime,
      };
    });

  res.json({ count: files.length, files });
});

// ─── HEALTH CHECK ───────────────────────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ─── [FIX-6] SAFE ERROR HANDLER ────────────────────────────────────────────
// Never expose stack traces or internal details to the client.
app.use((err, req, res, next) => {
  console.error(`[${new Date().toISOString()}] Error:`, err.message);

  if (process.env.NODE_ENV !== 'production') {
    console.error(err.stack);
  }

  res.status(500).json({ error: 'An internal error occurred' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// ─── STARTUP ────────────────────────────────────────────────────────────────
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true, mode: 0o750 });
}

const PORT = process.env.PORT || 3001;
app.listen(PORT, '127.0.0.1', () => {
  console.log(`[SECURE] Server running on http://127.0.0.1:${PORT}`);
});

module.exports = app;
