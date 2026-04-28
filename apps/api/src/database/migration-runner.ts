import { Client } from 'pg';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const migrationsDir = join(__dirname, '..', 'migrations');

async function ensureTable(client: Client) {
  await client.query(`
    create table if not exists schema_migrations (
      id text primary key,
      applied_at timestamptz not null default now()
    )
  `);
}

async function run() {
  const command = process.argv[2] ?? 'status';
  const client = new Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  await ensureTable(client);
  const applied = new Set((await client.query('select id from schema_migrations')).rows.map((row) => row.id));
  const files = readdirSync(migrationsDir).filter((file) => file.endsWith('.sql')).sort();

  for (const file of files) {
    const isApplied = applied.has(file);
    if (command === 'status') {
      console.log(`${isApplied ? 'up' : 'down'} ${file}`);
      continue;
    }
    if (!isApplied && command === 'up') {
      await client.query('begin');
      try {
        await client.query(readFileSync(join(migrationsDir, file), 'utf8'));
        await client.query('insert into schema_migrations (id) values ($1)', [file]);
        await client.query('commit');
        console.log(`applied ${file}`);
      } catch (error) {
        await client.query('rollback');
        throw error;
      }
    }
  }

  await client.end();
}

void run().catch((error) => {
  console.error(error);
  process.exit(1);
});
