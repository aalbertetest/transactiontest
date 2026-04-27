export function makeRequireUser(authService) {
  return function requireUser(req, res, next) {
    const header = req.headers.authorization ?? '';
    const [scheme, token] = header.split(' ');
    if (scheme !== 'Bearer' || !token) {
      return res.status(401).json({ error: 'unauthorized' });
    }
    const verified = authService.verifyAccessToken(token);
    if (!verified) {
      return res.status(401).json({ error: 'unauthorized' });
    }
    req.userId = verified.userId;
    next();
  };
}
