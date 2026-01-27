// =============================================================================
// NEXUS PLATFORM - API GATEWAY - AUTHENTICATION MIDDLEWARE
// =============================================================================
// JWT and API key authentication.
// =============================================================================

import { Request, Response, NextFunction } from 'express';
import * as jose from 'jose';
import { config } from '../config';
import { logger } from '../utils/logger';

/**
 * Authenticated user type
 */
export interface AuthenticatedUser {
  id: string;
  email?: string;
  roles: string[];
  permissions: string[];
  tenantId?: string;
  tokenType: 'jwt' | 'api_key';
}

/**
 * Extended request type with user
 */
declare global {
  namespace Express {
    interface Request {
      user?: AuthenticatedUser;
      isAuthenticated: boolean;
      authMethod?: string;
    }
  }
}

/**
 * Public paths that don't require authentication
 */
const PUBLIC_PATHS = [
  '/',
  '/health',
  '/ready',
  '/live',
  '/metrics',
  '/auth/login',
  '/auth/register',
  '/auth/refresh',
  '/auth/password-reset',
  '/auth/verify-email',
  '/public',
];

/**
 * Check if path is public
 */
function isPublicPath(path: string): boolean {
  return PUBLIC_PATHS.some(publicPath => 
    path === publicPath || path.startsWith(`${publicPath}/`)
  );
}

/**
 * Extract Bearer token from Authorization header
 */
function extractBearerToken(req: Request): string | null {
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.slice(7);
  }
  return null;
}

/**
 * Extract API key from header
 */
function extractApiKey(req: Request): string | null {
  return req.headers[config.auth.apiKey.header.toLowerCase()] as string || null;
}

/**
 * Validate JWT token
 */
async function validateJwt(token: string): Promise<AuthenticatedUser | null> {
  try {
    const secret = new TextEncoder().encode(config.auth.jwt.secretKey);
    
    const { payload } = await jose.jwtVerify(token, secret, {
      issuer: config.auth.jwt.issuer,
      audience: config.auth.jwt.audience,
    });

    return {
      id: payload.sub as string,
      email: payload.email as string | undefined,
      roles: (payload.roles as string[]) || [],
      permissions: (payload.permissions as string[]) || [],
      tenantId: payload.tenant_id as string | undefined,
      tokenType: 'jwt',
    };
  } catch (error) {
    logger.debug({ error: (error as Error).message }, 'JWT validation failed');
    return null;
  }
}

/**
 * Validate API key
 */
async function validateApiKey(apiKey: string): Promise<AuthenticatedUser | null> {
  // Check prefix
  if (!apiKey.startsWith(config.auth.apiKey.prefix)) {
    return null;
  }

  // In production, validate against database
  // For now, accept any key with correct prefix
  logger.warn('API key validation not fully implemented - using placeholder');

  return {
    id: 'api_key_user',
    roles: ['api'],
    permissions: ['read', 'write'],
    tokenType: 'api_key',
  };
}

/**
 * Authentication middleware.
 * 
 * Validates JWT tokens and API keys for incoming requests.
 */
export async function authenticationMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  // Initialize auth state
  req.isAuthenticated = false;
  req.user = undefined;
  req.authMethod = undefined;

  // Skip public paths
  if (isPublicPath(req.path)) {
    return next();
  }

  let user: AuthenticatedUser | null = null;

  // Try JWT authentication
  const token = extractBearerToken(req);
  if (token) {
    user = await validateJwt(token);
    if (user) {
      req.authMethod = 'jwt';
    }
  }

  // Try API key authentication if JWT failed
  if (!user) {
    const apiKey = extractApiKey(req);
    if (apiKey) {
      user = await validateApiKey(apiKey);
      if (user) {
        req.authMethod = 'api_key';
      }
    }
  }

  // If no valid credentials
  if (!user) {
    res.status(401).json({
      error: {
        code: 'AUTHENTICATION_REQUIRED',
        message: 'Authentication required',
        requestId: req.requestId,
      },
    });
    return;
  }

  // Set user on request
  req.user = user;
  req.isAuthenticated = true;

  logger.debug({
    userId: user.id,
    authMethod: req.authMethod,
    requestId: req.requestId,
  }, 'Request authenticated');

  next();
}

/**
 * Require specific role middleware
 */
export function requireRole(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.isAuthenticated || !req.user) {
      res.status(401).json({
        error: {
          code: 'AUTHENTICATION_REQUIRED',
          message: 'Authentication required',
          requestId: req.requestId,
        },
      });
      return;
    }

    const hasRole = roles.some(role => req.user!.roles.includes(role));
    if (!hasRole) {
      res.status(403).json({
        error: {
          code: 'FORBIDDEN',
          message: `Required role: ${roles.join(' or ')}`,
          requestId: req.requestId,
        },
      });
      return;
    }

    next();
  };
}

/**
 * Require specific permission middleware
 */
export function requirePermission(...permissions: string[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.isAuthenticated || !req.user) {
      res.status(401).json({
        error: {
          code: 'AUTHENTICATION_REQUIRED',
          message: 'Authentication required',
          requestId: req.requestId,
        },
      });
      return;
    }

    const hasPermission = permissions.every(perm => req.user!.permissions.includes(perm));
    if (!hasPermission) {
      res.status(403).json({
        error: {
          code: 'FORBIDDEN',
          message: `Required permission: ${permissions.join(', ')}`,
          requestId: req.requestId,
        },
      });
      return;
    }

    next();
  };
}
