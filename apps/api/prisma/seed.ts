import { PrismaClient } from '@prisma/client';
import { PLANS } from '../../../packages/shared/src';

const prisma = new PrismaClient();

async function main() {
  for (const p of PLANS) {
    await prisma.plan.upsert({
      where: { id: p.id },
      update: {
        name: p.name,
        priceCents: p.priceCents,
        currency: p.currency,
        interval: p.interval,
        features: JSON.stringify(p.features),
        active: true,
      },
      create: {
        id: p.id,
        name: p.name,
        priceCents: p.priceCents,
        currency: p.currency,
        interval: p.interval,
        features: JSON.stringify(p.features),
      },
    });
  }
  console.log(`Seeded ${PLANS.length} plans.`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
