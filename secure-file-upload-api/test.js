'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SECURE_PORT = 3001;
const BASE_URL = `http://127.0.0.1:${SECURE_PORT}`;

let passed = 0;
let failed = 0;

function assert(condition, testName) {
  if (condition) {
    console.log(`  PASS: ${testName}`);
    passed++;
  } else {
    console.error(`  FAIL: ${testName}`);
    failed++;
  }
}

function makeRequest(method, urlPath, options = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlPath, BASE_URL);
    const reqOptions = {
      method,
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      headers: options.headers || {},
    };

    const req = http.request(reqOptions, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        let parsed;
        try { parsed = JSON.parse(body); } catch { parsed = body; }
        resolve({ status: res.statusCode, headers: res.headers, body: parsed });
      });
    });

    req.on('error', reject);

    if (options.body) {
      req.write(options.body);
    }
    req.end();
  });
}

function createMultipartBody(filename, content, contentType = 'image/jpeg') {
  const boundary = '----TestBoundary' + Date.now();
  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\n`),
    Buffer.from(`Content-Disposition: form-data; name="file"; filename="${filename}"\r\n`),
    Buffer.from(`Content-Type: ${contentType}\r\n\r\n`),
    content,
    Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);
  return { body, boundary };
}

async function runTests() {
  console.log('\n=== Secure File Upload API Tests ===\n');

  // Test 1: Health check
  console.log('--- Health Check ---');
  const health = await makeRequest('GET', '/health');
  assert(health.status === 200, 'Health endpoint returns 200');
  assert(health.body.status === 'ok', 'Health status is "ok"');

  // Test 2: Security headers (from helmet)
  console.log('\n--- Security Headers ---');
  assert(health.headers['x-content-type-options'] === 'nosniff', 'X-Content-Type-Options: nosniff');
  assert(!health.headers['x-powered-by'], 'X-Powered-By header is absent');

  // Test 3: Upload with valid JPEG (JPEG magic bytes: FF D8 FF)
  console.log('\n--- Valid File Upload ---');
  const jpegContent = Buffer.concat([
    Buffer.from([0xFF, 0xD8, 0xFF, 0xE0]),
    Buffer.alloc(100, 0x00),
  ]);
  const { body: jpegBody, boundary: jpegBoundary } = createMultipartBody('test.jpg', jpegContent);
  const uploadRes = await makeRequest('POST', '/upload', {
    body: jpegBody,
    headers: { 'Content-Type': `multipart/form-data; boundary=${jpegBoundary}` },
  });
  assert(uploadRes.status === 201, 'Valid JPEG upload returns 201');
  assert(uploadRes.body.file && uploadRes.body.file.filename, 'Response contains filename');
  assert(!uploadRes.body.file.storedPath, 'Response does NOT leak storedPath');
  assert(!uploadRes.body.file.destination, 'Response does NOT leak destination');

  const uploadedFilename = uploadRes.body.file ? uploadRes.body.file.filename : null;

  // Test 4: Download the uploaded file
  if (uploadedFilename) {
    console.log('\n--- File Download ---');
    const dlRes = await makeRequest('GET', `/download/${uploadedFilename}`);
    assert(dlRes.status === 200, 'Download valid file returns 200');
    assert(
      dlRes.headers['content-disposition'] && dlRes.headers['content-disposition'].includes('attachment'),
      'Content-Disposition is attachment'
    );
  }

  // Test 5: Path traversal in download
  console.log('\n--- Path Traversal Prevention ---');
  const traversalRes = await makeRequest('GET', '/download/../../etc/passwd');
  assert(traversalRes.status === 400 || traversalRes.status === 403 || traversalRes.status === 404,
    'Path traversal in download is blocked');

  // Test 6: Reject disallowed file extension
  console.log('\n--- File Type Restrictions ---');
  const { body: phpBody, boundary: phpBoundary } = createMultipartBody(
    'shell.php', Buffer.from('<?php system($_GET["cmd"]); ?>'), 'application/x-php'
  );
  const phpRes = await makeRequest('POST', '/upload', {
    body: phpBody,
    headers: { 'Content-Type': `multipart/form-data; boundary=${phpBoundary}` },
  });
  assert(phpRes.status === 400, 'PHP file upload is rejected (400)');

  // Test 7: Reject HTML file
  const { body: htmlBody, boundary: htmlBoundary } = createMultipartBody(
    'evil.html', Buffer.from('<script>alert(1)</script>'), 'text/html'
  );
  const htmlRes = await makeRequest('POST', '/upload', {
    body: htmlBody,
    headers: { 'Content-Type': `multipart/form-data; boundary=${htmlBoundary}` },
  });
  assert(htmlRes.status === 400, 'HTML file upload is rejected (400)');

  // Test 8: Magic bytes mismatch (a .jpg with PNG content)
  console.log('\n--- Magic Bytes Validation ---');
  const pngMagic = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
  const { body: fakeJpgBody, boundary: fakeJpgBoundary } = createMultipartBody(
    'fake.jpg', Buffer.concat([pngMagic, Buffer.alloc(100)]), 'image/jpeg'
  );
  const fakeJpgRes = await makeRequest('POST', '/upload', {
    body: fakeJpgBody,
    headers: { 'Content-Type': `multipart/form-data; boundary=${fakeJpgBoundary}` },
  });
  assert(fakeJpgRes.status === 400, 'Mismatched magic bytes are rejected (400)');

  // Test 9: 404 for unknown endpoints
  console.log('\n--- 404 Handler ---');
  const notFound = await makeRequest('GET', '/nonexistent');
  assert(notFound.status === 404, 'Unknown endpoint returns 404');

  // Test 10: File listing
  console.log('\n--- File Listing ---');
  const listRes = await makeRequest('GET', '/files');
  assert(listRes.status === 200, 'File listing returns 200');
  assert(Array.isArray(listRes.body.files), 'File listing returns an array');

  // Summary
  console.log(`\n=== Results: ${passed} passed, ${failed} failed ===\n`);
  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
