import { z } from 'zod';

export const metricsSchema = z.object({
  totalTrends: z.number().int().nonnegative(),
  newslettersSent: z.number().int().nonnegative(),
  premiumSubs: z.number().int().nonnegative(),
  revenueEstimate: z.number().int().nonnegative(),
  delta24h: z.object({
    totalTrends: z.number().int(),
    newslettersSent: z.number().int(),
    premiumSubs: z.number().int(),
    revenueEstimate: z.number().int(),
  }).optional(),
  lastUpdated: z.string().datetime().optional()
});

export function validateMetrics(data) {
  const parsed = metricsSchema.safeParse(data);
  if (!parsed.success) {
    return { ok: false, errors: parsed.error.issues.map(i => ({ path: i.path.join('.'), message: i.message })) };
  }
  return { ok: true, data: parsed.data };
}
