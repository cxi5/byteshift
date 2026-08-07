/**
 * Configuração dos 3 cenários contextuais (Fase 8) — cada um combina
 * dois campos vindos de gêneros diferentes. Mesma filosofia de
 * genres.js: nenhum HTML específico de cenário fica hardcoded, o
 * scenario-card.js lê tudo daqui.
 */

function formatSeconds(data) {
  return `≈ ${data.human_readable}`;
}

function formatFilesFit(data) {
  const count = new Intl.NumberFormat("pt-BR").format(data.files_that_fit);
  const leftoverMb = data.leftover_in_units?.megabyte;
  const leftoverText =
    typeof leftoverMb === "number"
      ? ` (sobra ≈ ${new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 2 }).format(leftoverMb)} MB)`
      : "";
  return `${count} arquivos${leftoverText}`;
}

export const SCENARIOS = [
  {
    key: "download-time",
    endpoint: "download-time",
    title: "tempo de download",
    description: "tamanho do arquivo ÷ velocidade de rede",
    fields: [
      {
        label: "tamanho",
        unitsGenre: "storage",
        defaultUnit: "gigabyte",
        valueField: "size_value",
        unitField: "size_unit",
      },
      {
        label: "rede",
        unitsGenre: "network",
        defaultUnit: "megabit_per_second",
        valueField: "rate_value",
        unitField: "rate_unit",
      },
    ],
    formatResult: formatSeconds,
  },
  {
    key: "transfer-time",
    endpoint: "transfer-time",
    title: "tempo de transferência local",
    description: "tamanho do arquivo ÷ velocidade de transferência",
    fields: [
      {
        label: "tamanho",
        unitsGenre: "storage",
        defaultUnit: "gigabyte",
        valueField: "size_value",
        unitField: "size_unit",
      },
      {
        label: "velocidade",
        unitsGenre: "speed",
        defaultUnit: "megabyte_per_second",
        valueField: "rate_value",
        unitField: "rate_unit",
      },
    ],
    formatResult: formatSeconds,
  },
  {
    key: "files-fit",
    endpoint: "files-fit",
    title: "quantos arquivos cabem",
    description: "tamanho médio do arquivo ÷ capacidade real do dispositivo",
    fields: [
      {
        label: "arquivo",
        unitsGenre: "storage",
        defaultUnit: "megabyte",
        valueField: "file_size_value",
        unitField: "file_size_unit",
      },
      {
        label: "capacidade real",
        unitsGenre: "device-capacity-real",
        defaultUnit: "gibibyte",
        valueField: "device_capacity_value",
        unitField: "device_capacity_unit",
      },
    ],
    formatResult: formatFilesFit,
  },
];
