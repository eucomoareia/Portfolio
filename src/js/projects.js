import { getLang, t, onLangChange } from './i18n.js';
import { observeReveal } from './reveal.js';

// Seus projetos. Imagens em public/images (caminho relativo: 'images/...').
// `links`: lista de { label, href } — deixe vazia se o projeto não tiver link público.
// `logo`: mostra a imagem inteira e centrada sobre a cor `logoBg` (para ícones e logotipos).
const projects = [
  {
    title: 'Slice',
    period: { pt: '2026 — Atual', en: '2026 — Present' },
    description: {
      pt: 'Parte do Slate, suíte de apps em Rust. Editor de vídeo no estilo da página Edit do DaVinci Resolve: timeline com várias faixas, keyframes, ajuste de cor, títulos e exportação em MP4. Um único compositor gera o preview e o arquivo final.',
      en: 'Part of Slate, a suite of Rust apps. Video editor in the style of DaVinci Resolve\'s Edit page: multi-track timeline, keyframes, color adjustment, titles and MP4 export. One compositor drives both the preview and the final file.',
    },
    image: 'images/slice.svg',
    logo: true,
    logoBg: 'bg-pastel-lavender',
    tags: ['Rust', 'egui'],
    links: [],
  },
  {
    title: 'Echo',
    period: { pt: '2026 — Atual', en: '2026 — Present' },
    description: {
      pt: 'Gravador e editor de voz no estilo do Audacity: faixas mono e estéreo, redução de ruído, normalização de loudness (LUFS), de-esser e teleprompter com o roteiro.',
      en: 'Voice recorder and editor in the style of Audacity: mono and stereo tracks, noise reduction, loudness normalization (LUFS), de-esser and a script teleprompter.',
    },
    image: 'images/echo.svg',
    logo: true,
    logoBg: 'bg-pastel-pink',
    tags: ['Rust', 'egui'],
    links: [],
  },
  {
    title: 'Quill',
    period: { pt: '2026 — Atual', en: '2026 — Present' },
    description: {
      pt: 'Editor de roteiros para vídeo que mostra o tempo de fala de cada seção, separa notas de edição da fala e exporta legendas (.srt) pelo ritmo. Abre o roteiro direto no Echo.',
      en: 'Script editor for video that shows the speaking time of each section, keeps edit notes apart from the spoken text and exports subtitles (.srt) from your pace. Opens the script straight in Echo.',
    },
    image: 'images/quill.svg',
    logo: true,
    logoBg: 'bg-pastel-mint',
    tags: ['Rust', 'egui'],
    links: [],
  },
  {
    title: 'Hue',
    period: { pt: '2026 — Atual', en: '2026 — Present' },
    description: {
      pt: 'Editor de imagens no estilo do Krita: motor de pincéis, camadas com 13 modos de mistura, máscaras, seleções, filtros e dockers que você arruma como quiser.',
      en: 'Image editor in the style of Krita: brush engine, layers with 13 blend modes, masks, selections, filters and dockers you can arrange however you like.',
    },
    image: 'images/hue.svg',
    logo: true,
    logoBg: 'bg-pastel-butter',
    tags: ['Rust', 'egui'],
    links: [],
  },
  {
    title: 'AtestaVet',
    period: { pt: '2026 — Atual', en: '2026 — Present' },
    description: {
      pt: 'App multiplataforma (Android, macOS e Linux) que preenche e gera em PDF atestados veterinários de brucelose e tuberculose. Funciona offline, sincroniza com a nuvem e monta sozinho o relatório mensal da ADEPARÁ.',
      en: 'Cross-platform app (Android, macOS and Linux) that fills in and generates veterinary brucellosis and tuberculosis certificates as PDFs. Works offline, syncs to the cloud and builds the monthly ADEPARÁ report automatically.',
    },
    image: 'images/atestavet-icon.png',
    logo: true,
    logoBg: 'bg-pastel-sky',
    tags: ['Flutter', 'Dart', 'Supabase'],
    links: [{ label: 'Site', href: 'https://atestavet.com.br/' }],
  },
  {
    title: 'PPMAC',
    period: { pt: '2024 — Atual', en: '2024 — Present' },
    description: {
      pt: 'Site do Observatório de Políticas Públicas de Mitigação e Adaptação Climática na Amazônia, com páginas de notícias, formulários de contato e seção sobre o projeto.',
      en: 'Website for the Observatory of Public Policies on Climate Mitigation and Adaptation in the Amazon, with news pages, contact forms and an about section.',
    },
    image: 'https://ppmac.com.br/assets/Logo-DVWhmIZw.svg',
    logo: true,
    logoBg: 'bg-white',
    tags: ['Next.js', 'JavaScript', 'Tailwind'],
    links: [{ label: 'ppmac.com.br', href: 'https://ppmac.com.br' }],
  },
  {
    title: 'Dead Hand',
    period: '2025 — 2026',
    description: {
      pt: 'Jogo de Blackjack retrô com partidas rápidas, decisões estratégicas e duelos de alta tensão. Feito sozinho na Godot e publicado na Steam.',
      en: 'Retro-style Blackjack game with quick matches, strategic decisions and high-tension duels. Built solo in Godot and published on Steam.',
    },
    image:
      'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/4209090/8f18a8631634efb0c88a2a1c83368ef20463ed06/capsule_616x353.jpg',
    tags: ['Godot', 'GDScript'],
    links: [{ label: 'Steam', href: 'https://store.steampowered.com/app/4209090/Dead_Hand/' }],
  },
  {
    title: 'SOSQueimadas Marabá',
    period: '2024',
    description: {
      pt: 'App para combater queimadas em Marabá-PA, com mapa de focos, denúncias, clima em tempo real, guia e sensores. Registrado no INPI e desenvolvido em coautoria com a equipe.',
      en: 'App to fight wildfires in Marabá, Brazil, with a fire map, reports, live weather, a guide and sensors. Registered with INPI (Brazilian IP office) and co-developed with a team.',
    },
    image: 'images/sosqueimadas.webp',
    tags: ['Swift', 'iOS'],
    links: [],
  },
];

const tagColors = [
  'bg-pastel-lavender',
  'bg-pastel-pink',
  'bg-pastel-peach',
  'bg-pastel-mint',
  'bg-pastel-sky',
  'bg-pastel-butter',
];

const allTags = [...new Set(projects.flatMap((p) => p.tags))].sort();
const colorFor = (tag) => tagColors[allTags.indexOf(tag) % tagColors.length];

let activeFilter = 'all';

const escape = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

function cardHTML(p) {
  const lang = getLang();
  const linkIcon =
    '<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14 3h7v7M10 14L21 3M21 14v5a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h5"/></svg>';
  const links = p.links
    .map(
      (l) =>
        `<a href="${escape(l.href)}" target="_blank" rel="noopener" class="inline-flex items-center gap-1.5 text-sm font-medium text-muted transition hover:text-ink">${linkIcon}${escape(l.label)}</a>`,
    )
    .join('');

  return `
    <article class="reveal glass tilt group flex flex-col overflow-hidden rounded-3xl p-3 hover:bg-white/60">
      ${
        p.logo
          ? `<div class="flex aspect-video items-center justify-center overflow-hidden rounded-2xl p-8 ${p.logoBg ?? 'bg-white'}">
              <img src="${escape(p.image)}" alt="${escape(p.title)}" loading="lazy"
                class="max-h-full max-w-full object-contain drop-shadow-sm transition duration-500 group-hover:scale-105" />
            </div>`
          : `<div class="aspect-video overflow-hidden rounded-2xl">
              <img src="${escape(p.image)}" alt="${escape(p.title)}" loading="lazy"
                class="h-full w-full object-cover transition duration-500 group-hover:scale-110" />
            </div>`
      }
      <div class="flex flex-1 flex-col px-3 pb-3 pt-5">
        <p class="font-mono text-xs text-muted">${escape(typeof p.period === 'string' ? p.period : p.period[lang])}</p>
        <h3 class="mt-1 text-xl font-bold">${escape(p.title)}</h3>
        <p class="mt-2 flex-1 text-sm text-muted">${escape(p.description[lang])}</p>
        <div class="mt-4 flex flex-wrap gap-2">
          ${p.tags.map((tag) => `<span class="chip ${colorFor(tag)}">${escape(tag)}</span>`).join('')}
        </div>
        ${links ? `<div class="mt-5 flex gap-5 border-t border-ink/10 pt-4">${links}</div>` : ''}
      </div>
    </article>`;
}

function renderFilters() {
  const container = document.getElementById('project-filters');
  const filters = ['all', ...allTags];
  container.innerHTML = filters
    .map((f) => {
      const active = f === activeFilter;
      const label = f === 'all' ? t('projects.all') : f;
      return `<button type="button" data-filter="${escape(f)}" aria-pressed="${active}"
        class="rounded-full px-4 py-1.5 text-sm font-medium transition ${
          active
            ? 'bg-ink text-cream'
            : 'border border-white/70 bg-white/45 text-muted backdrop-blur-xl hover:bg-white/70 hover:text-ink'
        }">${escape(label)}</button>`;
    })
    .join('');
}

function renderGrid() {
  const grid = document.getElementById('project-grid');
  const visible = activeFilter === 'all' ? projects : projects.filter((p) => p.tags.includes(activeFilter));
  grid.innerHTML = visible.map(cardHTML).join('');
  grid.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${i * 80}ms`;
    observeReveal(el);
  });
  grid.querySelectorAll('.tilt').forEach(attachTilt);
}

function attachTilt(card) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  card.addEventListener('mousemove', (e) => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    card.style.transform = `perspective(800px) rotateX(${-y * 6}deg) rotateY(${x * 6}deg) translateY(-4px)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
}

export function initProjects() {
  renderFilters();
  renderGrid();

  document.getElementById('project-filters').addEventListener('click', (e) => {
    const btn = e.target.closest('[data-filter]');
    if (!btn) return;
    activeFilter = btn.dataset.filter;
    renderFilters();
    renderGrid();
  });

  onLangChange(() => {
    renderFilters();
    renderGrid();
  });
}
