/**
 * Configuração dos 4 gêneros — nenhum HTML específico de gênero fica
 * hardcoded em outro lugar do frontend. O card.js lê daqui.
 *
 * `unitsGenre` bate com a chave `genre` que a rota GET /units devolve.
 * `resultUnitsGenre` só existe em Capacidade de Dispositivo, onde a
 * unidade de entrada (anunciada) é diferente da unidade de saída (real).
 */

export const GENRES = [
  {
    key: "storage",
    label: "armazenamento",
    endpoint: "storage",
    unitsGenre: "storage",
    defaultUnit: "gigabyte",
    primaryUnits: ["megabyte", "gigabyte", "gibibyte", "terabyte"],
  },
  {
    key: "speed",
    label: "velocidade de transferência",
    endpoint: "speed",
    unitsGenre: "speed",
    defaultUnit: "megabyte_per_second",
    primaryUnits: [
      "kilobyte_per_second",
      "megabyte_per_second",
      "mebibyte_per_second",
      "gigabyte_per_second",
    ],
  },
  {
    key: "network",
    label: "banda de rede",
    endpoint: "network",
    unitsGenre: "network",
    defaultUnit: "megabit_per_second",
    primaryUnits: ["kilobit_per_second", "megabit_per_second", "gigabit_per_second"],
  },
  {
    key: "device-capacity",
    label: "capacidade de dispositivo",
    endpoint: "device-capacity",
    unitsGenre: "device-capacity-advertised",
    resultUnitsGenre: "device-capacity-real",
    defaultUnit: "gigabyte",
    primaryUnits: ["gibibyte", "tebibyte"],
  },
];
