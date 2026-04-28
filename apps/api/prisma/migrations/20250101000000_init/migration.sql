-- Initial migration: users, refresh tokens, plans, subscriptions, invoices.

CREATE TABLE "User" (
  "id"           TEXT    NOT NULL PRIMARY KEY,
  "email"        TEXT    NOT NULL,
  "name"         TEXT,
  "passwordHash" TEXT,
  "role"         TEXT    NOT NULL DEFAULT 'USER',
  "provider"     TEXT,
  "providerId"   TEXT,
  "createdAt"    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt"    DATETIME NOT NULL
);

CREATE UNIQUE INDEX "User_email_key" ON "User"("email");
CREATE UNIQUE INDEX "User_provider_providerId_key" ON "User"("provider", "providerId");

CREATE TABLE "RefreshToken" (
  "id"        TEXT NOT NULL PRIMARY KEY,
  "userId"    TEXT NOT NULL,
  "tokenHash" TEXT NOT NULL,
  "expiresAt" DATETIME NOT NULL,
  "revokedAt" DATETIME,
  "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "RefreshToken_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX "RefreshToken_tokenHash_key" ON "RefreshToken"("tokenHash");
CREATE INDEX "RefreshToken_userId_idx" ON "RefreshToken"("userId");

CREATE TABLE "Plan" (
  "id"         TEXT NOT NULL PRIMARY KEY,
  "name"       TEXT NOT NULL,
  "priceCents" INTEGER NOT NULL,
  "currency"   TEXT NOT NULL DEFAULT 'usd',
  "interval"   TEXT NOT NULL DEFAULT 'month',
  "features"   TEXT NOT NULL,
  "active"     BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE "Subscription" (
  "id"                TEXT NOT NULL PRIMARY KEY,
  "userId"            TEXT NOT NULL,
  "planId"            TEXT NOT NULL,
  "status"            TEXT NOT NULL,
  "currentPeriodEnd"  DATETIME NOT NULL,
  "cancelAtPeriodEnd" BOOLEAN NOT NULL DEFAULT 0,
  "createdAt"         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt"         DATETIME NOT NULL,
  CONSTRAINT "Subscription_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE,
  CONSTRAINT "Subscription_planId_fkey" FOREIGN KEY ("planId") REFERENCES "Plan" ("id")
);
CREATE INDEX "Subscription_userId_idx" ON "Subscription"("userId");

CREATE TABLE "Invoice" (
  "id"             TEXT NOT NULL PRIMARY KEY,
  "userId"         TEXT NOT NULL,
  "subscriptionId" TEXT NOT NULL,
  "amountCents"    INTEGER NOT NULL,
  "currency"       TEXT NOT NULL DEFAULT 'usd',
  "status"         TEXT NOT NULL,
  "createdAt"      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "Invoice_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE CASCADE,
  CONSTRAINT "Invoice_subscriptionId_fkey" FOREIGN KEY ("subscriptionId") REFERENCES "Subscription" ("id") ON DELETE CASCADE
);
CREATE INDEX "Invoice_userId_idx" ON "Invoice"("userId");
