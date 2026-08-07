import { fetchUnits } from "./api.js";
import { createCard } from "./cards/card.js";
import { GENRES } from "./cards/genres.js";
import { createScenarioCard } from "./cards/scenario-card.js";
import { SCENARIOS } from "./cards/scenarios.js";

const appEl = document.getElementById("app");

async function bootstrap() {
  appEl.innerHTML = `
    <header class="topbar">
      <span class="topbar__wordmark">byte<span>shift</span></span>
      <span class="topbar__tagline">&gt; conversor de unidades técnicas</span>
    </header>
    <main class="card-grid" id="card-grid"></main>
    <section class="scenario-section" id="scenario-section" hidden>
      <h2 class="scenario-section__heading">cenários</h2>
      <div class="scenario-list" id="scenario-list"></div>
    </section>
  `;

  const grid = document.getElementById("card-grid");
  const scenarioSection = document.getElementById("scenario-section");
  const scenarioList = document.getElementById("scenario-list");

  let unitsResponse;
  try {
    unitsResponse = await fetchUnits();
  } catch (err) {
    grid.innerHTML =
      '<p class="card__error card__error--visible">' +
      "Não foi possível carregar as unidades. Confirme se a API está rodando em localhost:8000." +
      "</p>";
    return;
  }

  // Transforma [{genre, units}] num mapa {genre: units} pra acesso direto
  const unitsByGenre = Object.fromEntries(unitsResponse.map((entry) => [entry.genre, entry.units]));

  for (const genreConfig of GENRES) {
    grid.appendChild(createCard(genreConfig, unitsByGenre));
  }

  for (const scenarioConfig of SCENARIOS) {
    scenarioList.appendChild(createScenarioCard(scenarioConfig, unitsByGenre));
  }
  scenarioSection.hidden = false;
}

bootstrap();
