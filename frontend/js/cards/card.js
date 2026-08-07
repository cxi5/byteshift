import { convert, ApiError } from "../api.js";

const DEBOUNCE_MS = 300;

const numberFormatter = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 6 });

/**
 * Cria o DOM de um card de conversão. Este é o único template — os 4
 * gêneros usam exatamente esta função, o que muda é só a configuração
 * (genres.js) e a lista de unidades (vinda de GET /units). Nada de
 * gênero específico é hardcoded aqui dentro.
 */
export function createCard(genreConfig, unitsByGenre) {
  const inputUnits = unitsByGenre[genreConfig.unitsGenre] ?? [];
  const outputUnits = unitsByGenre[genreConfig.resultUnitsGenre ?? genreConfig.unitsGenre] ?? [];
  const outputUnitsByKey = Object.fromEntries(outputUnits.map((unit) => [unit.key, unit]));

  let expanded = false;
  let debounceHandle = null;

  const card = document.createElement("section");
  card.className = "card";
  card.setAttribute("aria-label", genreConfig.label);

  card.innerHTML = `
    <header class="card__chrome">
      <span class="card__dots" aria-hidden="true">
        <span class="card__dot card__dot--primary"></span>
        <span class="card__dot card__dot--decimal"></span>
        <span class="card__dot card__dot--binary"></span>
      </span>
      <span class="card__title">${genreConfig.label}</span>
    </header>
    <div class="card__body">
      <label class="card__input-row">
        <span class="card__prompt" aria-hidden="true">&gt;</span>
        <input
          class="card__value-input"
          type="number"
          inputmode="decimal"
          min="0"
          step="any"
          placeholder="0"
          aria-label="Valor a converter"
        />
        <select class="card__unit-select" aria-label="Unidade de origem"></select>
      </label>
      <p class="card__error" role="alert"></p>
      <p class="card__loading">convertendo</p>
      <div class="card__results" aria-live="polite"></div>
      <button type="button" class="card__toggle">show --all</button>
    </div>
  `;

  const valueInput = card.querySelector(".card__value-input");
  const unitSelect = card.querySelector(".card__unit-select");
  const errorEl = card.querySelector(".card__error");
  const loadingEl = card.querySelector(".card__loading");
  const resultsEl = card.querySelector(".card__results");
  const toggleBtn = card.querySelector(".card__toggle");

  for (const unit of inputUnits) {
    const option = document.createElement("option");
    option.value = unit.key;
    option.textContent = `${unit.symbol} — ${unit.label}`;
    unitSelect.appendChild(option);
  }
  if (genreConfig.defaultUnit) {
    unitSelect.value = genreConfig.defaultUnit;
  }

  function showError(message) {
    errorEl.textContent = message;
    errorEl.classList.add("card__error--visible");
    resultsEl.innerHTML = "";
  }

  function clearError() {
    errorEl.textContent = "";
    errorEl.classList.remove("card__error--visible");
  }

  function badgeClassFor(system) {
    if (system === "decimal") return "card__result-badge card__result-badge--decimal";
    if (system === "binary") return "card__result-badge card__result-badge--binary";
    return "card__result-badge";
  }

  function renderResults(conversions) {
    resultsEl.innerHTML = "";
    const keysToShow = expanded ? Object.keys(conversions) : genreConfig.primaryUnits;

    for (const key of keysToShow) {
      const unitMeta = outputUnitsByKey[key];
      const value = conversions[key];
      if (unitMeta === undefined || value === undefined) continue;

      const row = document.createElement("div");
      row.className = "card__result-row";
      row.innerHTML = `
        <span class="card__result-label">
          <span class="${badgeClassFor(unitMeta.system)}" aria-hidden="true"></span>
          ${unitMeta.symbol}
        </span>
        <span class="card__result-value">${numberFormatter.format(value)}</span>
      `;
      resultsEl.appendChild(row);
    }
  }

  async function runConversion() {
    const rawValue = valueInput.value.trim();

    if (rawValue === "") {
      clearError();
      loadingEl.classList.remove("card__loading--visible");
      resultsEl.innerHTML = "";
      return;
    }

    const numericValue = Number(rawValue);
    if (Number.isNaN(numericValue)) {
      showError("Digite um número válido.");
      return;
    }

    clearError();
    loadingEl.classList.add("card__loading--visible");
    resultsEl.classList.add("card__results--loading");

    try {
      const result = await convert(genreConfig.endpoint, numericValue, unitSelect.value);
      renderResults(result.conversions);
    } catch (err) {
      showError(
        err instanceof ApiError
          ? err.message
          : "Não foi possível conectar à API. Verifique se o servidor está rodando.",
      );
    } finally {
      loadingEl.classList.remove("card__loading--visible");
      resultsEl.classList.remove("card__results--loading");
    }
  }

  function scheduleConversion() {
    clearTimeout(debounceHandle);
    debounceHandle = setTimeout(runConversion, DEBOUNCE_MS);
  }

  valueInput.addEventListener("input", scheduleConversion);
  unitSelect.addEventListener("change", runConversion);

  toggleBtn.addEventListener("click", () => {
    expanded = !expanded;
    toggleBtn.textContent = expanded ? "show --primary" : "show --all";
    if (valueInput.value.trim() !== "") {
      runConversion();
    }
  });

  return card;
}
