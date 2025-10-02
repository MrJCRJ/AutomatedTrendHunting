#!/usr/bin/env node
// Script para validar arquivos de configuração usando schemas Zod
// Uso: node scripts/check-configs.js

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { adsenseConfigSchema, mailchimpConfigSchema, telegramConfigSchema, whatsappConfigSchema, safeParse } from '../lib/schemas.js';
import { logger } from '../lib/log.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONFIG_MAP = [
  { file: 'config_adsense.json', example: 'config_adsense.json.example', schema: adsenseConfigSchema },
  { file: 'config_mailchimp.json', example: 'config_mailchimp.json.example', schema: mailchimpConfigSchema },
  { file: 'config_telegram.json', example: 'config_telegram.json.example', schema: telegramConfigSchema },
  { file: 'config_whatsapp.json', example: 'config_whatsapp.json.example', schema: whatsappConfigSchema },
];

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf-8'));
}

function main() {
  logger.info('Iniciando verificação de configurações');
  const baseDir = path.resolve(__dirname, '..');
  const errors = [];

  for (const cfg of CONFIG_MAP) {
    const filePath = path.join(baseDir, cfg.file);
    if (!fs.existsSync(filePath)) {
      errors.push({ file: cfg.file, error: 'Arquivo ausente', example: cfg.example });
      logger.warn(`Arquivo ausente: ${cfg.file}`);
      continue;
    }
    try {
      const json = readJSON(filePath);
      const result = safeParse(cfg.schema, json);
      if (!result.ok) {
        errors.push({ file: cfg.file, validation: result.errors });
        logger.error(`Falha de validação: ${cfg.file}`, { errors: result.errors });
      } else {
        logger.info(`OK: ${cfg.file}`);
      }
    } catch (e) {
      errors.push({ file: cfg.file, error: String(e) });
      logger.error(`Erro lendo ${cfg.file}`, e);
    }
  }

  if (errors.length) {
    logger.error('Configurações inválidas ou faltando', { count: errors.length, errors });
    process.exitCode = 1;
  } else {
    logger.info('Todas as configurações válidas ✅');
  }
}

main();
