import { getLang, t, onLangChange } from './i18n.js';
import { observeReveal } from './reveal.js';

// Sua experiência, em ordem cronológica (a mais antiga primeiro).
// `current: true` marca o cargo atual.
const experience = [
  {
    date: { pt: 'mai/2023 — mai/2024', en: 'May 2023 — May 2024' },
    role: { pt: 'Aluno Auxiliar de Escritório', en: 'Office Assistant (Student)' },
    company: 'Grupo FASA',
    location: 'São Domingos do Araguaia, PA',
    description: {
      pt: 'Apoio a atividades administrativas e de escritório, à gestão de documentos e à manipulação de planilhas, desenvolvendo organização, gestão de tarefas e comunicação.',
      en: 'Supported administrative and office activities, document management and spreadsheet handling, building organization, task management and communication skills.',
    },
    tags: [],
  },
  {
    date: { pt: 'mai/2024 — out/2024', en: 'May 2024 — Oct 2024' },
    role: { pt: 'Estagiário de Desenvolvimento', en: 'Development Intern' },
    company: 'Compass UOL',
    location: { pt: 'São Paulo, SP (remoto)', en: 'São Paulo, Brazil (remote)' },
    description: {
      pt: 'Scholarship Program na trilha Back-end Development (Spring Boot) for Commerce on AWS, com 400 horas de prática em back-end e serviços de nuvem voltados a e-commerce.',
      en: 'Scholarship Program on the Back-end Development (Spring Boot) for Commerce on AWS track — 400 hours of hands-on back-end and cloud work for e-commerce.',
    },
    tags: ['Java', 'Spring Boot', 'AWS'],
  },
  {
    date: { pt: 'jul/2024 — atual', en: 'Jul 2024 — Present' },
    role: { pt: 'Desenvolvedor Full Stack', en: 'Full Stack Developer' },
    company: 'Exception Júnior',
    location: 'Marabá, PA',
    description: {
      pt: 'Desenvolvimento de aplicações full stack, com interfaces e serviços em Next.js, Node.js e Tailwind CSS. Back-end do Conecta Canaã (Smart City de Canaã dos Carajás) e front-end do site do PPMAC (ppmac.com.br).',
      en: 'Building full stack applications, with interfaces and services in Next.js, Node.js and Tailwind CSS. Back-end of Conecta Canaã (Canaã dos Carajás Smart City) and front-end of the PPMAC website (ppmac.com.br).',
    },
    tags: ['TypeScript', 'Next.js', 'Node.js', 'Go', 'Java'],
    current: true,
  },
  {
    date: { pt: 'dez/2024 — ago/2025', en: 'Dec 2024 — Aug 2025' },
    role: { pt: 'Bolsista e Instrutor de Projeto de Extensão', en: 'Scholarship Holder and Extension Project Instructor' },
    company: 'UNIFESSPA',
    location: 'Marabá, PA',
    description: {
      pt: 'Instrutor no projeto "Montagem e Manutenção de Computadores: Minimizando Impactos Ambientais na Era Digital" (960 h), formando mais de 30 alunos em montagem, manutenção e descarte consciente de equipamentos.',
      en: 'Instructor for the "Computer Assembly and Maintenance: Minimizing Environmental Impact in the Digital Era" project (960 h), training 30+ students in assembly, maintenance and responsible e-waste disposal.',
    },
    tags: ['Hardware', { pt: 'Ensino', en: 'Teaching' }],
  },
];

// Links do cartão "Próximo capítulo"
const contactLinks = [
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/luisotaviosiqueira' },
  { label: 'GitHub', href: 'https://github.com/eucomoareia' },
  { label: 'Email', href: 'mailto:luispim2005@gmail.com' },
];

const markerColors = ['bg-pastel-lavender', 'bg-pastel-pink', 'bg-pastel-peach', 'bg-pastel-mint', 'bg-pastel-sky'];

const tr = (v) => (typeof v === 'string' ? v : v[getLang()]);

const escape = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

// Marcador na estrada: fica na linha (à esquerda no mobile, ao centro no desktop)
const marker = (content, color) => `
  <div class="absolute left-5 top-6 z-10 -translate-x-1/2 md:left-1/2">
    <span class="relative flex h-11 w-11 items-center justify-center rounded-full border-4 border-cream ${color} font-display text-sm font-bold text-ink">
      ${content}
    </span>
  </div>`;

function itemHTML(item, i) {
  const lang = getLang();
  const left = i % 2 === 0;
  const color = markerColors[i % markerColors.length];
  return `
    <li class="relative pb-12 pl-16 md:grid md:grid-cols-2 md:pl-0">
      ${marker(String(i + 1).padStart(2, '0'), color)}
      <div class="reveal ${left ? 'md:col-start-1 md:pr-14 md:text-right' : 'md:col-start-2 md:pl-14'}">
        <article class="glass rounded-3xl p-6">
          <div class="flex flex-wrap items-center gap-2 ${left ? 'md:justify-end' : ''}">
            <span class="chip ${color}">${escape(item.date[lang])}</span>
            ${item.current ? `<span class="chip bg-ink text-cream">${escape(t('experience.now'))}</span>` : ''}
          </div>
          <h3 class="mt-3 text-xl font-bold">${escape(item.role[lang])}</h3>
          <p class="text-sm font-medium text-muted">${escape(item.company)} · ${escape(tr(item.location))}</p>
          <p class="mt-3 text-sm text-muted">${escape(item.description[lang])}</p>
          ${
            item.tags.length
              ? `<div class="mt-4 flex flex-wrap gap-2 ${left ? 'md:justify-end' : ''}">
                  ${item.tags.map((tag) => `<span class="chip border border-ink/10 bg-white/60">${escape(tr(tag))}</span>`).join('')}
                </div>`
              : ''
          }
        </article>
      </div>
    </li>`;
}

function nextHTML(i) {
  const left = i % 2 === 0;
  return `
    <li class="relative pl-16 md:grid md:grid-cols-2 md:pl-0">
      ${marker('→', 'bg-white')}
      <div class="reveal ${left ? 'md:col-start-1 md:pr-14 md:text-right' : 'md:col-start-2 md:pl-14'}">
        <div class="rounded-3xl border-2 border-dashed border-ink/20 bg-white/30 p-6 backdrop-blur-xl">
          <h3 class="text-xl font-bold">${escape(t('experience.next_title'))}</h3>
          <p class="mt-2 text-sm text-muted">${escape(t('experience.next_desc'))}</p>
          <div class="mt-4 flex flex-wrap gap-2 ${left ? 'md:justify-end' : ''}">
            ${contactLinks
              .map(
                (l) =>
                  `<a href="${escape(l.href)}" ${l.href.startsWith('http') ? 'target="_blank" rel="noopener"' : ''}
                    class="rounded-full bg-ink px-4 py-1.5 text-sm font-medium text-cream transition hover:bg-ink/85">${escape(l.label)}</a>`,
              )
              .join('')}
          </div>
        </div>
      </div>
    </li>`;
}

function render() {
  const list = document.getElementById('roadmap');
  list.innerHTML = experience.map(itemHTML).join('') + nextHTML(experience.length);
  list.querySelectorAll('.reveal').forEach(observeReveal);
}

export function initExperience() {
  render();
  onLangChange(render);
}
