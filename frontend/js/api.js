/**
 * Comunicação com o backend do ByteShift.
 *
 * Este módulo só sabe fazer requisições HTTP e traduzir erros de rede
 * em mensagens claras. Não conhece nada sobre como os cards são
 * desenhados — isso é responsabilidade de cards/card.js.
 */

import { API_BASE_URL } from "./config.js";

/**
 * Erro lançado quando a API responde, mas com um status de erro
 * (ex: 422 de unidade inválida). Diferente de um erro de rede, aqui a
 * mensagem já vem pronta do backend.
 */
export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Busca a lista de unidades disponíveis por gênero.
 * Resposta esperada: [{ genre, units: [{ key, symbol, label, system }] }]
 */
export async function fetchUnits() {
  const response = await fetch(`${API_BASE_URL}/units`);

  if (!response.ok) {
    throw new ApiError("Não foi possível carregar as unidades da API.", response.status);
  }

  return response.json();
}

/**
 * Envia um valor para conversão num gênero específico.
 *
 * @param {string} genre - chave da rota, ex: "storage", "speed",
 *   "network" ou "device-capacity" (bate com o endpoint /convert/{genre})
 * @param {number} value - valor a converter, deve ser não-negativo
 * @param {string} fromUnit - chave da unidade de origem, ex: "gigabyte"
 * @returns {Promise<{genre: string, from_unit: string, input_value: number, conversions: Record<string, number>}>}
 */
export async function convert(genre, value, fromUnit) {
  const response = await fetch(`${API_BASE_URL}/convert/${genre}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ value, from_unit: fromUnit }),
  });

  if (!response.ok) {
    // A API sempre manda uma mensagem clara em `detail` nos erros 422
    // (unidade inválida, valor negativo, overflow) — repassamos ela
    // direto, em vez de inventar uma mensagem genérica por cima.
    const body = await response.json().catch(() => null);
    const detail = body?.detail ?? "Erro ao converter. Tente novamente.";
    throw new ApiError(detail, response.status);
  }

  return response.json();
}

/**
 * Envia um cenário contextual (Fase 8) — combina dois gêneros numa
 * única pergunta, ex: "quanto tempo leva pra baixar X a Y Mbps".
 *
 * @param {string} scenarioKey - chave da rota, ex: "download-time"
 * @param {Record<string, number|string>} payload - corpo específico do cenário
 */
export async function convertContext(scenarioKey, payload) {
  const response = await fetch(`${API_BASE_URL}/convert/context/${scenarioKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = body?.detail ?? "Erro ao calcular. Tente novamente.";
    throw new ApiError(detail, response.status);
  }

  return response.json();
}
