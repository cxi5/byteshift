import { fetchUnits } from "./api.js";
import { createCard } from "./cards/card.js";
import { GENRES } from "./cards/genres.js";
import { createScenarioCard } from "./cards/scenario-card.js";
import { SCENARIOS } from "./cards/scenarios.js";

const appEl = document.getElementById("app");

async function bootstrap() {
  appEl.innerHTML = `
    <div class="page">
      <header class="topbar">
        <div class="topbar__brand">
          <span class="topbar__wordmark">byte<span>shift</span></span>
          <span class="topbar__tagline">conversor de unidades técnicas</span>
        </div>
      </header>

      <section class="intro" aria-label="Sobre">
        <p class="intro__text">
          Digite um valor numa unidade e veja o equivalente em todas as outras.
          <strong>Laranja</strong> marca decimal (base 1000).
          <strong class="intro__binary">Roxo</strong> marca binário (base 1024).
        </p>
        <div class="legend" aria-hidden="true">
          <span class="legend__item">
            <span class="legend__dot legend__dot--decimal"></span>
            decimal · 1000
          </span>
          <span class="legend__item">
            <span class="legend__dot legend__dot--binary"></span>
            binário · 1024
          </span>
        </div>
      </section>

      <main class="card-grid" id="card-grid"></main>

      <section class="scenario-section" id="scenario-section" hidden>
        <div class="scenario-section__header">
          <h2 class="scenario-section__heading">cenários</h2>
          <p class="scenario-section__sub">perguntas práticas que combinam dois gêneros</p>
        </div>
        <div class="scenario-list" id="scenario-list"></div>
      </section>

      <footer class="footer">
        <p class="footer__text">ByteShift · portfólio</p>
      </footer>
    </div>
  `;

  const grid = document.getElementById("card-grid");
  const scenarioSection = document.getElementById("scenario-section");
  const scenarioList = document.getElementById("scenario-list");

  let unitsResponse;
  try {
    unitsResponse = await fetchUnits();
  } catch (err) {
    grid.innerHTML =
      '<p class="card__error card__error--visible page-error">' +
      "Não foi possível carregar as unidades. Verifique se a API está acessível." +
      "</p>";
    return;
  }

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
