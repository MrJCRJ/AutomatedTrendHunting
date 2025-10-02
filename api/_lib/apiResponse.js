// Local copy of apiResponse helper placed under api/_lib to bypass .gitignore ignoring top-level lib/
export function json(res, status, payload) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(payload));
}
export const ok = (res, data = {}, extra = {}) => json(res, 200, { success: true, data, ...extra });
export const created = (res, data = {}, extra = {}) => json(res, 201, { success: true, data, ...extra });
export const badRequest = (res, message = 'Bad request', extra = {}) => json(res, 400, { success: false, error: message, ...extra });
export const unauthorized = (res, message = 'Unauthorized', extra = {}) => json(res, 401, { success: false, error: message, ...extra });
export const notFound = (res, message = 'Not found', extra = {}) => json(res, 404, { success: false, error: message, ...extra });
export const methodNotAllowed = (res, methods = []) => json(res, 405, { success: false, error: 'Method not allowed', allow: methods });
export const serverError = (res, error) => json(res, 500, { success: false, error: 'Internal error', detail: String(error) });
