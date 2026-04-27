const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const dbFile = path.join(__dirname, 'orders.json');

function readDb() {
  if (!fs.existsSync(dbFile)) fs.writeFileSync(dbFile, JSON.stringify({ orders: [] }, null, 2));
  return JSON.parse(fs.readFileSync(dbFile, 'utf8'));
}

function writeDb(db) {
  fs.writeFileSync(dbFile, JSON.stringify(db, null, 2));
}

app.post('/orders', (req, res) => {
  console.log('POST /orders', req.body);
  const db = readDb();
  const body = req.body || {};

  if (!body.customerName || body.customerName.length < 2) {
    return res.status(400).json({ error: 'bad customerName' });
  }
  if (!body.email || body.email.indexOf('@') === -1) {
    return res.status(400).json({ error: 'bad email' });
  }
  if (!body.items || !Array.isArray(body.items) || body.items.length === 0) {
    return res.status(400).json({ error: 'bad items' });
  }

  let subtotal = 0;
  for (const item of body.items) {
    if (!item.sku || item.sku.length < 2) return res.status(400).json({ error: 'bad sku' });
    if (!item.quantity || item.quantity < 1) return res.status(400).json({ error: 'bad quantity' });
    if (!item.unitPrice || item.unitPrice < 0) return res.status(400).json({ error: 'bad price' });
    subtotal += item.quantity * item.unitPrice;
  }

  let discount = 0;
  if (body.couponCode === 'SAVE10') discount = subtotal * 0.1;
  if (body.couponCode === 'VIP20') discount = subtotal * 0.2;
  const tax = (subtotal - discount) * 0.0825;
  const total = Math.round((subtotal - discount + tax) * 100) / 100;

  const order = {
    id: String(Date.now()),
    customerName: body.customerName,
    email: body.email,
    items: body.items,
    couponCode: body.couponCode,
    status: 'pending',
    subtotal,
    discount,
    tax,
    total,
    createdAt: new Date().toISOString()
  };

  db.orders.push(order);
  writeDb(db);
  console.log('created order ' + order.id + ' total=' + order.total);
  res.status(201).json(order);
});

app.get('/orders/:id', (req, res) => {
  console.log('GET /orders/' + req.params.id);
  const db = readDb();
  const order = db.orders.find((o) => o.id === req.params.id);
  if (!order) return res.status(404).json({ error: 'missing' });

  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.quantity * item.unitPrice;
  }
  let discount = 0;
  if (order.couponCode === 'SAVE10') discount = subtotal * 0.1;
  if (order.couponCode === 'VIP20') discount = subtotal * 0.2;
  const tax = (subtotal - discount) * 0.0825;
  order.subtotal = subtotal;
  order.discount = discount;
  order.tax = tax;
  order.total = Math.round((subtotal - discount + tax) * 100) / 100;

  res.json(order);
});

app.post('/orders/:id/cancel', (req, res) => {
  console.log('POST /orders/' + req.params.id + '/cancel');
  const db = readDb();
  const order = db.orders.find((o) => o.id === req.params.id);
  if (!order) return res.status(404).json({ error: 'missing' });
  if (order.status === 'shipped') return res.status(400).json({ error: 'too late' });
  if (order.status === 'cancelled') return res.status(400).json({ error: 'already cancelled' });
  order.status = 'cancelled';
  writeDb(db);
  res.json(order);
});

app.listen(3000, () => console.log('legacy app listening on 3000'));
