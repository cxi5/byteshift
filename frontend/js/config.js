/**
 * Configuração de ambiente do frontend.
 *
 * Em desenvolvimento local (localhost/127.0.0.1), fala com o backend
 * rodando na máquina. Em qualquer outro domínio, assume que é produção
 * e usa a URL do backend publicado.
 */

const PRODUCTION_API_URL = "https://byteshift-t5oi.onrender.com";

const isLocalDev =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";

export const API_BASE_URL = isLocalDev ? "http://localhost:8000" : PRODUCTION_API_URL;
