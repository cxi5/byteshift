import { convertContext, ApiError } from "../api.js";

const DEBOUNCE_MS = 300;

/**
 * Cria o DOM de um card de cenário contextual. Visualmente diferente
 * do card.js de propósito (sem os "3 pontinhos" de terminal, ícone
 * ">>"  em vez disso) — o objetivo é a pessoa bater o olho e saber
 * que aquilo NÃO é uma conversão direta de unidade.
 */
export function createScenarioCard(scenarioConfig, unitsByGenre) {
  let debounceHandle = null;

  const card = document.createElement("section");
  card.className = "scenario-card";
  card.setAttribute("aria-label", scenarioConfig.title);

  const fieldsHtml = scenarioConfig.fields
    .map(
      (field, index) => `
        <label class="card__input-row scenario-card__field" data-field-index="${index}">
          <span class="card__prompt" aria-hidden="true">${field.label}</span>
          <input
            class="card__value-input"
            type="number"
            inputmode="decimal"
            min="0"
            step="any"
            placeholder="0"
            aria-label="Valor de ${field.label}"
          />
          <select class="card__unit-select" aria-label="Unidade de ${field.label}"></select>
        </label>
      `,
    )
    .join('<span class="scenario-card__operator" aria-hidden="true">÷</span>');

  card.innerHTML = `
    <header class="scenario-card__chrome">
      <span class="scenario-card__icon" aria-hidden="true">&gt;&gt;</span>
      <span class="scenario-card__title">${scenarioConfig.title}</span>
      <span class="scenario-card__description">${scenarioConfig.description}</span>
    </header>
    <div class="scenario-card__body">
      <div class="scenario-card__fields">${fieldsHtml}</div>
      <p class="card__error" role="alert"></p>
      <p class="card__loading">calculando</p>
      <p class="scenario-card__result" aria-live="polite"></p>
    </div>
  `;

  const fieldRows = Array.from(card.querySelectorAll(".scenario-card__field"));
  const errorEl = card.querySelector(".card__error");
  const loadingEl = card.querySelector(".card__loading");
  const resultEl = card.querySelector(".scenario-card__result");

  // Popula cada seletor de unidade com a lista do gênero correspondente
  fieldRows.forEach((row, index) => {
    const field = scenarioConfig.fields[index];
    const select = row.querySelector(".card__unit-select");
    const units = unitsByGenre[field.unitsGenre] ?? [];

    for (const unit of units) {
      const option = document.createElement("option");
      option.value = unit.key;
      option.textContent = unit.symbol;
      select.appendChild(option);
    }
    if (field.defaultUnit) {
      select.value = field.defaultUnit;
    }
  });

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.add("card__error--visible");
    resultEl.textContent = "";
  }

  function clearError() {
    errorEl.textContent = "";
    errorEl.classList.remove("card__error--visible");
  }

  function allFieldsFilled() {
    return fieldRows.every((row) => row.querySelector(".card__value-input").value.trim() !== "");
  }

  async function runCalculation() {
    if (!allFieldsFilled()) {
      clearError();
      resultEl.textContent = "";
      return;
    }

    const payload = {};
    for (let i = 0; i < fieldRows.length; i++) {
      const field = scenarioConfig.fields[i];
      const row = fieldRows[i];
      const rawValue = row.querySelector(".card__value-input").value.trim();
      const numericValue = Number(rawValue);

      if (Number.isNaN(numericValue)) {
        showError(`Digite um número válido em "${field.label}".`);
        return;
      }

      payload[field.valueField] = numericValue;
      payload[field.unitField] = row.querySelector(".card__unit-select").value;
    }

    clearError();
    loadingEl.classList.add("card__loading--visible");

    try {
      const data = await convertContext(scenarioConfig.endpoint, payload);
      resultEl.textContent = scenarioConfig.formatResult(data);
    } catch (err) {
      showError(
        err instanceof ApiError
          ? err.message
          : "Não foi possível conectar à API. Verifique se o servidor está rodando.",
      );
    } finally {
      loadingEl.classList.remove("card__loading--visible");
    }
  }

  function scheduleCalculation() {
    clearTimeout(debounceHandle);
    debounceHandle = setTimeout(runCalculation, DEBOUNCE_MS);
  }

  for (const row of fieldRows) {
    row.querySelector(".card__value-input").addEventListener("input", scheduleCalculation);
    row.querySelector(".card__unit-select").addEventListener("change", runCalculation);
  }

  return card;
}
