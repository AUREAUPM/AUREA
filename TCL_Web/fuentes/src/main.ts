import './style.css';

// La portada de WordPress aporta su propio título y cabecera.
document.documentElement.classList.toggle('embedded', new URLSearchParams(window.location.search).get('embed') === '1');

// Controles y primera simulación de tiradas.
const app = document.querySelector<HTMLElement>('#app');
if (!app) throw new Error('No se encuentra el contenedor de la página.');

app.innerHTML = `
  <header class="resource-header">
    <div class="resource-identity"><span>Proyecto AUREA · Universidad Politécnica de Madrid</span><a href="https://blogs.upm.es/pie-aurea/">Web del proyecto <span aria-hidden="true">↗</span></a></div>
    <h1>Explicación intuitiva del Teorema Central del Límite</h1>
    <p>Explora cómo cambia la distribución de la suma al aumentar el número de dados por lanzamiento.</p>
  </header>
  <section class="controls" aria-label="Configuración del simulador" aria-describedby="stage-note">
    <fieldset>
      <legend>Distribución de probabilidad</legend>
      <div class="buttons distributions">
        <button type="button" aria-pressed="true">Uniforme</button>
        <button type="button" aria-pressed="false">Sesgada</button>
        <button type="button" aria-pressed="false">En V</button>
      </div>
    </fieldset>
    <fieldset>
      <legend>Nº lanzamientos</legend>
      <div class="launches">
        <output for="launches">1000</output>
        <input id="launches" aria-label="Número de lanzamientos" type="range" min="0" max="50" step="1" value="10" aria-valuetext="1000 lanzamientos" />
        <div class="limits"><span>10</span><span>5000</span></div>
      </div>
    </fieldset>
    <fieldset>
      <legend>Dados por lanzamiento</legend>
      <div class="buttons dice">
        <button type="button" aria-pressed="true">2</button>
        <button type="button" aria-pressed="false">6</button>
        <button type="button" aria-pressed="false">10</button>
        <button type="button" aria-pressed="false">16</button>
      </div>
    </fieldset>
    <button class="simulate" type="button">Simular</button>
  </section>
  <section class="scene" aria-label="Distribución y dados">
    <div class="distribution-panel" aria-live="polite"></div>
    <div class="dice-area">
      <div class="dice-panel"></div>
      <div class="run-readout" hidden><span>Progreso: <strong id="progress"></strong></span><span>Suma: <strong id="sum"></strong></span></div>
    </div>
  </section>
  <section class="sum-histogram" hidden aria-label="Distribución de la suma"></section>
  <p id="stage-note" role="status">Configura los controles y pulsa Simular.</p>
  <footer class="project-credit" aria-label="Créditos del proyecto">
    <p>Recurso realizado en el marco del proyecto <span class="project-name">AUREA: Aprendizaje y Uso del Razonamiento Estadístico y la Aleatoriedad (IE26.0405)</span></p>
    <p>Proyecto de Innovación Educativa financiado por la Universidad Politécnica de Madrid</p>
  </footer>
`;


type Face = 1 | 2 | 3 | 4 | 5 | 6;
const dots: Record<Face, [number, number][]> = {
  1: [[50, 50]],
  2: [[26, 74], [74, 26]],
  3: [[26, 74], [50, 50], [74, 26]],
  4: [[26, 26], [26, 74], [74, 26], [74, 74]],
  5: [[26, 26], [26, 74], [50, 50], [74, 26], [74, 74]],
  6: [[26, 26], [26, 50], [26, 74], [74, 26], [74, 50], [74, 74]],
};
// Una secuencia fija permite revisar todas las caras sin generar tiradas.
const examples: Face[] = [3, 5, 1, 6, 2, 4, 5, 3, 6, 1, 4, 2, 3, 6, 5, 2];
const panel = app.querySelector<HTMLDivElement>('.dice-panel')!;
const buttons = app.querySelectorAll<HTMLButtonElement>('.dice button');

function showDice(count: number, values: Face[] = examples.slice(0, count)): void {
  panel.style.setProperty('--columns', String(count === 2 ? 2 : count / 2));
  panel.innerHTML = values.map(value => `
    <svg class="die" viewBox="0 0 100 100" role="img" aria-label="Dado con valor ${value}">
      <rect x="3" y="3" width="94" height="94" rx="16" />
      ${dots[value].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="6" />`).join('')}
    </svg>
  `).join('');
  buttons.forEach(button => {
    button.setAttribute('aria-pressed', String(Number(button.textContent) === count));
  });
}

buttons.forEach(button => {
  button.addEventListener('click', () => showDice(Number(button.textContent)));
});
showDice(2);


// Las mismas probabilidades y escala relativa que en la beta ManimGL.
const distributions = [
  { name: 'Uniforme', weights: [1, 1, 1, 1, 1, 1], maximum: '1/6' },
  { name: 'Sesgada', weights: [1, 2, 3, 4, 5, 6], maximum: '0,29' },
  { name: 'En V', weights: [3, 2, 1, 1, 2, 3], maximum: '1/4' },
];
const distributionPanel = app.querySelector<HTMLDivElement>('.distribution-panel')!;
const distributionButtons = app.querySelectorAll<HTMLButtonElement>('.distributions button');

function showDistribution(index: number): void {
  const distribution = distributions[index];
  const maximum = Math.max(...distribution.weights);
  const total = distribution.weights.reduce((sum, weight) => sum + weight, 0);
  distributionPanel.innerHTML = `
    <svg class="distribution-chart" viewBox="0 0 434 170" role="img" aria-label="Distribución ${distribution.name}">
      <title>Distribución ${distribution.name}</title>
      <desc>${distribution.weights.map((weight, i) => `Cara ${i + 1}: ${weight}/${total}`).join('; ')}</desc>
      <path d="M 42 22 V 112 H 392 M 38 22 H 46" fill="none" stroke="#d8d8d8" stroke-width="1.6" />
      <text x="33" y="26" text-anchor="end" fill="#d8d8d8" font-size="14">${distribution.maximum}</text>
      ${distribution.weights.map((weight, i) => {
        const x = 84 + i * 56;
        const height = 90 * weight / maximum;
        const face = (i + 1) as Face;
        return `<rect x="${x - 24}" y="${112 - height}" width="48" height="${height}" fill="#2d9cdb" fill-opacity="0.9" />
          <svg x="${x - 12}" y="130" width="24" height="24" viewBox="0 0 100 100" aria-hidden="true">
            <rect x="3" y="3" width="94" height="94" rx="16" fill="#1f1f1f" stroke="white" stroke-width="3" />
            ${dots[face].map(([cx, cy]) => `<circle cx="${cx}" cy="${cy}" r="6" fill="white" />`).join('')}
          </svg>`;
      }).join('')}
    </svg>
    <p class="distribution-caption">Distribución de un dado</p>
  `;
  distributionButtons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
}
distributionButtons.forEach((button, index) => button.addEventListener('click', () => showDistribution(index)));
showDistribution(0);


// El deslizador recorre los mismos 51 valores permitidos en la beta.
const launchCounts = [10, ...Array.from({ length: 50 }, (_, i) => (i + 1) * 100)];
const launchSlider = app.querySelector<HTMLInputElement>('#launches')!;
const launchOutput = app.querySelector<HTMLOutputElement>('output[for="launches"]')!;
function updateLaunchCount(): void {
  const count = launchCounts[Number(launchSlider.value)];
  launchOutput.value = String(count);
  launchSlider.setAttribute('aria-valuetext', `${count} lanzamientos`);
}
launchSlider.addEventListener('input', updateLaunchCount);
updateLaunchCount();


const simulateButton = app.querySelector<HTMLButtonElement>('.simulate')!;
const readout = app.querySelector<HTMLDivElement>('.run-readout')!;
const progress = app.querySelector<HTMLElement>('#progress')!;
const sumOutput = app.querySelector<HTMLElement>('#sum')!;
const note = app.querySelector<HTMLElement>('#stage-note')!;
const histogram = app.querySelector<HTMLElement>('.sum-histogram')!;
let timer: ReturnType<typeof setTimeout> | undefined;

function resetSimulation(): void {
  clearTimeout(timer);
  timer = undefined;
  simulateButton.disabled = false;
  simulateButton.textContent = 'Simular';
  readout.hidden = true;
  histogram.hidden = true;
  histogram.replaceChildren();
  note.textContent = 'Configura los controles y pulsa Simular.';
  const selected = [...buttons].find(button => button.getAttribute('aria-pressed') === 'true')!;
  showDice(Number(selected.textContent));
}

// Cambiar cualquier ajuste cancela la animación y limpia el resultado anterior.
[...buttons, ...distributionButtons].forEach(button => button.addEventListener('click', resetSimulation));
launchSlider.addEventListener('input', resetSimulation);

simulateButton.addEventListener('click', () => {
  resetSimulation();
  const count = Number([...buttons].find(button => button.getAttribute('aria-pressed') === 'true')!.textContent);
  const distributionIndex = [...distributionButtons].findIndex(button => button.getAttribute('aria-pressed') === 'true');
  const weights = distributions[distributionIndex].weights;
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
  const launches = launchCounts[Number(launchSlider.value)];
  function roll(): Face {
    let target = Math.random() * totalWeight;
    for (let i = 0; i < weights.length; i++) {
      target -= weights[i];
      if (target < 0) return (i + 1) as Face;
    }
    return 6;
  }
  // Se calculan todas las tiradas; solo su presentación se agrupa en lotes.
  const observations = Array.from({ length: launches }, () => {
    const values = Array.from({ length: count }, roll);
    return { values, sum: values.reduce<number>((sum, value) => sum + value, 0) };
  });
  const bins = Array<number>(5 * count + 1).fill(0);
  const finalBins = Array<number>(bins.length).fill(0);
  observations.forEach(observation => finalBins[observation.sum - count]++);
  // Escala fija durante toda la animación; el bloque lima tiene altura mínima visible.
  const meanDie = weights.reduce((sum, weight, i) => sum + (i + 1) * weight / totalWeight, 0);
  const varianceDie = weights.reduce((sum, weight, i) => sum + (i + 1 - meanDie) ** 2 * weight / totalWeight, 0);
  const mean = count * meanDie;
  const deviation = Math.sqrt(count * varianceDie);
  const normalPeak = launches / (deviation * Math.sqrt(2 * Math.PI));
  const unitHeight = Math.min(12, 200 / Math.max(...finalBins, normalPeak));
  histogram.hidden = false;
  const batchSize = Math.ceil(launches / 70);
  const delay = launches === 10 ? 350 : 85;
  let completed = 0;
  simulateButton.disabled = true;
  simulateButton.textContent = 'Simulando…';
  readout.hidden = false;
  note.textContent = batchSize === 1 ? 'Simulación en curso.' : 'Simulación en curso · Se muestra la última tirada de cada lote.';
  function advance(): void {
    const next = Math.min(launches, completed + batchSize);
    for (let i = completed; i < next; i++) bins[observations[i].sum - count]++;
    completed = next;
    const observation = observations[completed - 1];
    showDice(count, observation.values);
    drawHistogram(bins, count, completed < launches ? observation.sum : null, unitHeight, completed);
    progress.textContent = `${completed} / ${launches}`;
    sumOutput.textContent = String(observation.sum);
    if (completed < launches) {
      timer = setTimeout(advance, delay);
    } else {
      timer = undefined;
      simulateButton.disabled = false;
      simulateButton.textContent = 'Simular';
      showNormal(count, launches, mean, deviation, unitHeight);
      note.textContent = 'Simulación terminada · Los dados y la suma corresponden al último lanzamiento.';
    }
  }
  advance();
});


function drawHistogram(bins: number[], minimum: number, activeSum: number | null, unitHeight: number, completed: number): void {
  const cell = 800 / bins.length;
  const labelStep = bins.length <= 20 ? 2 : bins.length <= 50 ? 5 : 10;
  histogram.innerHTML = `
    <svg viewBox="0 0 840 270" role="img" aria-label="${completed} lanzamientos acumulados.${activeSum === null ? ' Simulación terminada.' : ` Última suma: ${activeSum}.`}">
      <title>Distribución de la suma</title>
      <desc>${bins.map((frequency, i) => `${minimum + i}: ${frequency}`).join('; ')}</desc>
      ${bins.map((frequency, i) => {
        const value = minimum + i;
        const active = value === activeSum;
        const greenHeight = (frequency - (active ? 1 : 0)) * unitHeight;
        const x = 20 + (i + 0.5) * cell;
        const width = cell * 0.82;
        const activeHeight = Math.max(unitHeight, 5);
        const labelled = i === 0 || i === bins.length - 1 || value % labelStep === 0;
        return `<g data-sum="${value}" data-frequency="${frequency}">
          <rect x="${x - width / 2}" y="${230 - greenHeight}" width="${width}" height="${greenHeight}" fill="var(--color-accumulated)" />
          ${active ? `<rect class="active-observation" x="${x - width / 2}" y="${230 - greenHeight - activeHeight}" width="${width}" height="${activeHeight}" fill="var(--color-observation)" />` : ''}
          <path d="M ${x} 230 v 4" stroke="#d8d8d8" />
          ${labelled ? `<text x="${x}" y="253" text-anchor="middle" fill="#d8d8d8" font-size="14">${value}</text>` : ''}
        </g>`;
      }).join('')}
      <path d="M 20 230 H 820" stroke="#d8d8d8" stroke-width="1.6" />
    </svg>
    <p>Distribución de la suma</p>
  `;
}


function showNormal(count: number, launches: number, mean: number, deviation: number, unitHeight: number): void {
  const cell = 800 / (5 * count + 1);
  const points = Array.from({ length: 251 }, (_, i) => {
    const value = count + 5 * count * i / 250;
    const density = Math.exp(-0.5 * ((value - mean) / deviation) ** 2) / (deviation * Math.sqrt(2 * Math.PI));
    const x = 20 + (value - count + 0.5) * cell;
    const y = 230 - launches * density * unitHeight;
    return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
  }).join(' ');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', points);
  path.setAttribute('class', 'normal-curve');
  path.setAttribute('fill', 'none');
  path.setAttribute('stroke', 'var(--color-normal)');
  path.setAttribute('stroke-width', '3');
  path.setAttribute('aria-label', 'Aproximación normal teórica');
  histogram.querySelector('svg')!.append(path);
  const parameters = document.createElement('div');
  parameters.className = 'normal-parameters';
  parameters.setAttribute('aria-label', 'Parámetros teóricos de la suma');
  const format = (value: number) => value.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  parameters.innerHTML = `<span>Aproximación normal</span><span>μ = ${format(mean)}</span><span>σ = ${format(deviation)}</span>`;
  histogram.append(parameters);
}
