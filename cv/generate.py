"""Gera os currículos (PT e EN) em PDF: ../public/cv.pdf e ../public/cv-en.pdf.

Uso:  python3 cv/generate.py        (precisa de: pip install reportlab)

Coluna única, sem tabelas e com texto selecionável, para boa leitura por ATS.
Usa a fonte Lato se estiver instalada; senão, cai para Helvetica.
"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, Flowable, KeepTogether, Paragraph,
                                SimpleDocTemplate, Spacer)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "public")

# ---------------------------------------------------------------- fontes
LATO_DIRS = [
    "/usr/share/fonts/truetype/lato/",
    os.path.expanduser("~/Library/Fonts/"),
    "/Library/Fonts/",
    "/System/Library/Fonts/Supplemental/",
]


def setup_fonts():
    for d in LATO_DIRS:
        files = {k: os.path.join(d, f"Lato-{k}.ttf")
                 for k in ("Regular", "Bold", "Italic", "BoldItalic", "Semibold")}
        if all(os.path.exists(p) for p in files.values()):
            for k, p in files.items():
                pdfmetrics.registerFont(TTFont(f"Lato-{k}", p))
            registerFontFamily("Lato-Regular", normal="Lato-Regular", bold="Lato-Bold",
                               italic="Lato-Italic", boldItalic="Lato-BoldItalic")
            return dict(reg="Lato-Regular", bold="Lato-Bold", ital="Lato-Italic", semi="Lato-Semibold")
    return dict(reg="Helvetica", bold="Helvetica-Bold", ital="Helvetica-Oblique", semi="Helvetica-Bold")


F = setup_fonts()
INK = colors.HexColor("#1A1A1A")
DARK = colors.HexColor("#111111")
MUTED = colors.HexColor("#5C5C5C")
RULE = colors.HexColor("#CFCFCF")
ACCENT = colors.HexColor("#333333")
LINK = "#333333"

name_st = ParagraphStyle("name", fontName=F["bold"], fontSize=26, leading=30, textColor=DARK)
headline_st = ParagraphStyle("headline", fontName=F["semi"], fontSize=11.5, leading=16, textColor=MUTED)
contact_st = ParagraphStyle("contact", fontName=F["reg"], fontSize=9.4, leading=14, textColor=MUTED)
body = ParagraphStyle("body", fontName=F["reg"], fontSize=9.4, leading=13, textColor=INK)
sub = ParagraphStyle("sub", fontName=F["ital"], fontSize=8.8, leading=12, textColor=MUTED)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=11, bulletIndent=1, spaceAfter=1.5)


class Heading(Flowable):
    """Título de seção em caixa alta com linha fina (texto simples, sem tabela)."""

    def __init__(self, text):
        super().__init__()
        self.text = text.upper()

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 26

    def draw(self):
        c = self.canv
        c.setFillColor(DARK)
        c.setFont(F["bold"], 10)
        c.drawString(0, 7, self.text)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.8)
        c.line(0, 3, self.aw, 3)
        c.setStrokeColor(ACCENT)
        c.setLineWidth(1.6)
        c.line(0, 3, 26, 3)


class Row(Flowable):
    """Título à esquerda e data à direita, na mesma linha (sem tabela)."""

    def __init__(self, title, when):
        super().__init__()
        self.title, self.when = title, when

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 15

    def draw(self):
        c = self.canv
        c.setFillColor(INK)
        c.setFont(F["bold"], 10.2)
        c.drawString(0, 4, self.title)
        if self.when:
            c.setFillColor(MUTED)
            c.setFont(F["reg"], 9.2)
            c.drawRightString(self.aw, 4, self.when)


def link(url, label=None):
    return f'<a href="{url}" color="{LINK}"><u>{label or url}</u></a>'


def entry(title, when, subtitle=None, bullets=()):
    items = [Row(title, when)]
    if subtitle:
        items.append(Paragraph(subtitle, sub))
    for b in bullets:
        items.append(Paragraph(b, bullet, bulletText="•"))
    items.append(Spacer(1, 5.5))
    return KeepTogether(items)


# ---------------------------------------------------------------- conteúdo
EMAIL = "luispim2005@gmail.com"
PHONE = "+55 94 99277-3427"
LINKEDIN = "https://www.linkedin.com/in/luisotaviosiqueira"
GITHUB = "https://github.com/eucomoareia"
SITE = "https://eucomoareia.github.io/Portfolio/"

PT = dict(
    out="cv.pdf",
    title="Currículo — Luís Otávio de Siqueira Pimentel",
    headline="Desenvolvedor Full Stack · Estudante de Sistemas de Informação",
    place="Marabá, Pará, Brasil",
    h_summary="Resumo", h_edu="Formação", h_exp="Experiência", h_proj="Projetos",
    h_extra="Atividades complementares", h_cert="Certificações", h_skills="Competências",
    summary=("Desenvolvedor Full Stack na Exception Júnior, com passagem pela Compass UOL como estagiário de "
             "desenvolvimento. Cursando Bacharelado em Sistemas de Informação na Universidade Federal do Sul e "
             "Sudeste do Pará (conclusão prevista para janeiro de 2027). Experiência prática em HTML, CSS, "
             "JavaScript, TypeScript, Java, Go, Next.js, Node.js e Tailwind CSS. Desenvolvo projetos próprios em "
             "Flutter, Rust e Godot, e tenho certificações em back-end com Spring Boot, nuvem (AWS) e Swift."),
    edu=[("Bacharelado em Sistemas de Informação", "Conclusão prevista: jan. 2027",
          "Universidade Federal do Sul e Sudeste do Pará (Unifesspa)", [])],
    exp=[
        ("Desenvolvedor Full Stack · Exception Júnior", "jul. 2024 – atual",
         "Meio período · Marabá, PA (remoto)",
         ["Desenvolvimento de aplicações full stack com HTML, CSS, JavaScript, TypeScript, Java e Go, com "
          "interfaces e serviços em Next.js, Node.js e Tailwind CSS.",
          "Back-end do Conecta Canaã, plataforma web com área autenticada do projeto Smart City de Canaã dos "
          "Carajás (PA).",
          "Front-end do site do PPMAC (Next.js, Tailwind CSS), Observatório de Políticas Públicas de Mitigação e "
          "Adaptação Climática na Amazônia (Unifesspa), com notícias, publicações, coluna de artigos e pesquisa "
          "de campo. " + link("https://ppmac.com.br", "ppmac.com.br")]),
        ("Estagiário de Desenvolvimento · Compass UOL", "mai. 2024 – out. 2024",
         "Estágio · São Paulo, SP (remoto)",
         ["Scholarship Program: trilha Back-end Development (Spring Boot) for Commerce on AWS, 400 horas, "
          "concluída com sucesso.",
          "Certificações Gen AI Technical Certification e AI-Assisted Certified Professional."]),
        ("Aluno Auxiliar de Escritório (Aprendiz) · Grupo FASA", "mai. 2023 – mai. 2024",
         "São Domingos do Araguaia, PA",
         ["Apoio a atividades administrativas e de escritório, à gestão de documentos e à manipulação de "
          "planilhas, desenvolvendo organização, gestão de tarefas e comunicação."]),
    ],
    proj=[
        ("AtestaVet — atestados e relatórios veterinários", "set. 2026 – atual",
         "Flutter · Dart · Supabase · Cloudflare Pages",
         ["Aplicativo para veterinários preencherem e gerarem em PDF os documentos do programa de brucelose e "
          "tuberculose (PNCEBT): atestado de exame, atestado de vacinação e relatório mensal.",
          "Funciona no navegador e offline, instalável no celular ou computador; contas e sincronização na nuvem "
          "com Supabase. Desenvolvido sozinho.",
          "Formulário em etapas que reaproveita clientes e propriedades já cadastrados e calcula o resultado da "
          "tuberculinização conforme a norma; plano Premium com pagamento via Pix. "
          + link("https://atestavet.com.br", "atestavet.com.br")]),
        ("Slice — editor de vídeo em Rust", "out. 2026 – atual", "Rust · egui · FFmpeg · GitHub Actions",
         ["Editor de vídeo desktop no estilo do DaVinci Resolve: Media Pool, timeline com várias faixas de vídeo "
          "e áudio, keyframes, Inspector, waveform e exportação em MP4 (H.264 + AAC).",
          "Formato de projeto próprio com autosave e recuperação, painéis reorganizáveis e atalhos editáveis. "
          "Pacotes para Windows e macOS gerados por GitHub Actions. Parte da suíte Slate, desenvolvida sozinha, "
          "com mais de 140 testes automatizados."]),
        ("Echo — gravador e editor de voz em Rust", "out. 2026 – atual", "Rust · egui · FFmpeg · Whisper",
         ["Gravador e editor de voz desktop no estilo do Audacity: gravação em mono ou estéreo com overdub, "
          "edição por clipes e envelope de volume.",
          "Dezenas de efeitos (melhorar voz, redução de ruído, equalizador, compressor, de-esser), edição pela "
          "transcrição e teleprompter; exporta com loudness ajustado ao YouTube. Parte da suíte Slate."]),
        ("Dead Hand — jogo de Blackjack na Steam", "nov. 2025 – jan. 2026", "Godot · GDScript",
         ["Jogo de Blackjack retrô com três oponentes e PvP online em tempo real, lançado na Steam em "
          "22/01/2026, com interface em seis idiomas. Desenvolvido sozinho. "
          + link("https://store.steampowered.com/app/4209090/Dead_Hand", "Página na Steam")]),
        ("Bolsista e instrutor — Montagem e Manutenção de Computadores", "dez. 2024 – ago. 2025",
         "Unifesspa · Minimizando Impactos Ambientais na Era Digital · 960 horas",
         ["Atuação como bolsista e instrutor do projeto de extensão, formando mais de 30 alunos em montagem, "
          "manutenção e descarte responsável de equipamentos de informática."]),
    ],
    extra=[("Organização da I Semana do Cálculo", "dez. 2023",
            "Faculdade de Sistemas de Informação · Unifesspa · 20 horas",
            ["Divulgação do evento, criação de flyers, banners e vídeos, e criação e aplicação de minicursos."])],
    certs=[
        "<b>Back-end Development (Spring Boot) for Commerce on AWS</b>, 400h — Compass UOL (out. 2024)",
        "<b>Gen AI Technical Certification</b> e <b>AI-Assisted Certified Professional</b> — Compass UOL (mai. 2024)",
        "<b>Algoritmos e Programação Orientada a Objetos com Swift</b>, 50h — Instituto de Pesquisas Eldorado (dez. 2023)",
        "<b>Cloud Services com Swift e Serviços Cognitivos</b>, 100h — Instituto de Pesquisas Eldorado (fev. 2024)",
        "<b>Computação em Nuvem Amazon AWS para Iniciantes</b>, 3h — Udemy (out. 2024)",
        "<b>Servidores Virtuais com EC2</b>, 3h; <b>Amazon S3, CloudFront e Snowball</b>, 4,5h — Udemy (out. 2024)",
        "<b>Modelagem de Dados UML</b>, 13h — Udemy (out. 2024)",
        "<b>Metodologias Ágeis (XP, Scrum, Lean e Kanban)</b>, 4h; <b>Cyber Security</b>, 5h — Udemy (mai. 2024)",
        "<b>Fundamentos em Go</b> e <b>Conceitos Avançados de Go</b> — Rocketseat (set. 2025)",
        "<b>Minicurso GitHub, GitLab, GitPages</b>, 4,5h — Unifesspa (mai. 2024)",
        "<b>Registro de programa de computador</b> SOSQueimadas — Marabá — INPI, processo BR512024003985-6 (2024)",
    ],
    skills=[
        ("Linguagens", "HTML, CSS, JavaScript, TypeScript, Java, Go, Rust, Dart, Swift, GDScript, Python, SQL"),
        ("Frameworks e ferramentas", "Next.js, Node.js, Tailwind CSS, Spring Boot, Flutter, egui, FFmpeg, Supabase, "
                                     "Godot, Git, GitHub, GitLab"),
        ("Nuvem e infraestrutura", "AWS (EC2, S3, CloudFront), administração de redes, montagem e manutenção de "
                                   "computadores, segurança da informação"),
        ("Práticas", "Programação orientada a objetos, UML, metodologias ágeis (Scrum, Kanban, XP)"),
        ("Comportamentais", "Trabalho em equipe, comunicação, resolução de problemas, proatividade e adaptabilidade"),
        ("Idiomas", "Português (nativo), Inglês (avançado)"),
    ],
)

EN = dict(
    out="cv-en.pdf",
    title="Résumé — Luís Otávio de Siqueira Pimentel",
    headline="Full Stack Developer · Information Systems Student",
    place="Marabá, Pará, Brazil",
    h_summary="Summary", h_edu="Education", h_exp="Experience", h_proj="Projects",
    h_extra="Complementary activities", h_cert="Certifications", h_skills="Skills",
    summary=("Full Stack Developer at Exception Júnior, previously a Development Intern at Compass UOL. "
             "Bachelor's student in Information Systems at the Federal University of Southern and Southeastern "
             "Pará (Unifesspa), expected to graduate in January 2027. Hands-on experience with HTML, CSS, "
             "JavaScript, TypeScript, Java, Go, Next.js, Node.js and Tailwind CSS. I build personal projects in "
             "Flutter, Rust and Godot, and hold certifications in back-end development with Spring Boot, cloud "
             "(AWS) and Swift."),
    edu=[("Bachelor's Degree in Information Systems", "Expected: Jan 2027",
          "Federal University of Southern and Southeastern Pará (Unifesspa)", [])],
    exp=[
        ("Full Stack Developer · Exception Júnior", "Jul 2024 – Present",
         "Part-time · Marabá, PA, Brazil (remote)",
         ["Full stack application development with HTML, CSS, JavaScript, TypeScript, Java and Go, building "
          "interfaces and services in Next.js, Node.js and Tailwind CSS.",
          "Back-end of Conecta Canaã, a web platform with an authenticated area for the Smart City project of "
          "Canaã dos Carajás (PA).",
          "Front-end of the PPMAC website (Next.js, Tailwind CSS), the Observatory of Public Policies for Climate "
          "Mitigation and Adaptation in the Amazon (Unifesspa), with news, publications, an articles column and "
          "field research. " + link("https://ppmac.com.br", "ppmac.com.br")]),
        ("Development Intern · Compass UOL", "May 2024 – Oct 2024",
         "Internship · São Paulo, SP, Brazil (remote)",
         ["Scholarship Program: Back-end Development (Spring Boot) for Commerce on AWS track, 400 hours, "
          "completed successfully.",
          "Gen AI Technical Certification and AI-Assisted Certified Professional."]),
        ("Office Assistant (Apprentice) · Grupo FASA", "May 2023 – May 2024",
         "São Domingos do Araguaia, PA, Brazil",
         ["Supported administrative and office activities, document management and spreadsheet handling, "
          "building organization, task management and communication skills."]),
    ],
    proj=[
        ("AtestaVet — veterinary certificates and reports", "Sep 2026 – Present",
         "Flutter · Dart · Supabase · Cloudflare Pages",
         ["App for veterinarians to fill in and generate, as PDFs, the standardized documents of the brucellosis "
          "and tuberculosis program (PNCEBT): exam certificate, vaccination certificate and monthly report.",
          "Works in the browser and offline, installable on phone or computer; accounts and cloud sync with "
          "Supabase. Built solo.",
          "Multi-step form that reuses saved clients and properties and automatically calculates the tuberculin "
          "test result according to the regulation; Premium plan with Pix payments. "
          + link("https://atestavet.com.br", "atestavet.com.br")]),
        ("Slice — video editor in Rust", "Oct 2026 – Present", "Rust · egui · FFmpeg · GitHub Actions",
         ["Desktop video editor in the style of DaVinci Resolve: Media Pool, multi-track video and audio "
          "timeline, keyframes, Inspector, waveform and MP4 export (H.264 + AAC).",
          "Own project format with autosave and recovery, rearrangeable panels and editable shortcuts. Windows "
          "and macOS packages built with GitHub Actions. Part of the Slate suite, built solo, with 140+ "
          "automated tests."]),
        ("Echo — voice recorder and editor in Rust", "Oct 2026 – Present", "Rust · egui · FFmpeg · Whisper",
         ["Desktop voice recorder and editor in the style of Audacity: mono or stereo recording with overdub, "
          "clip-based editing and volume envelope.",
          "Dozens of effects (voice enhancement, noise reduction, equalizer, compressor, de-esser), "
          "transcript-based editing and teleprompter; exports with loudness adjusted for YouTube. Part of the "
          "Slate suite."]),
        ("Dead Hand — Blackjack game on Steam", "Nov 2025 – Jan 2026", "Godot · GDScript",
         ["Retro-style Blackjack game with three opponents and real-time online PvP, released on Steam on "
          "Jan 22, 2026, with an interface in six languages. Built solo. "
          + link("https://store.steampowered.com/app/4209090/Dead_Hand", "Steam page")]),
        ("Scholarship holder and instructor — Computer Assembly and Maintenance", "Dec 2024 – Aug 2025",
         "Unifesspa · Minimizing Environmental Impact in the Digital Era · 960 hours",
         ["Scholarship holder and instructor of the extension project, training more than 30 students in "
          "computer assembly, maintenance and responsible disposal of equipment."]),
    ],
    extra=[("Organization of the 1st Calculus Week", "Dec 2023",
            "Faculty of Information Systems · Unifesspa · 20 hours",
            ["Event promotion, creation of flyers, banners and videos, and creation and delivery of short courses."])],
    certs=[
        "<b>Back-end Development (Spring Boot) for Commerce on AWS</b>, 400h — Compass UOL (Oct 2024)",
        "<b>Gen AI Technical Certification</b> and <b>AI-Assisted Certified Professional</b> — Compass UOL (May 2024)",
        "<b>Algorithms and Object-Oriented Programming with Swift</b>, 50h — Eldorado Research Institute (Dec 2023)",
        "<b>Cloud Services Practices with Swift and Cognitive Services</b>, 100h — Eldorado Research Institute (Feb 2024)",
        "<b>AWS Cloud Computing for Beginners</b>, 3h — Udemy (Oct 2024)",
        "<b>Virtual Servers with EC2</b>, 3h; <b>Amazon S3, CloudFront and Snowball</b>, 4.5h — Udemy (Oct 2024)",
        "<b>UML Data Modeling</b>, 13h — Udemy (Oct 2024)",
        "<b>Agile Methodologies (XP, Scrum, Lean and Kanban)</b>, 4h; <b>Cyber Security</b>, 5h — Udemy (May 2024)",
        "<b>Go Fundamentals</b> and <b>Advanced Go Concepts</b> — Rocketseat (Sep 2025)",
        "<b>GitHub, GitLab and GitPages: An Introductory Approach</b>, 4.5h — Unifesspa (May 2024)",
        "<b>Software registration</b> SOSQueimadas — Marabá — INPI, process BR512024003985-6 (2024)",
    ],
    skills=[
        ("Languages", "HTML, CSS, JavaScript, TypeScript, Java, Go, Rust, Dart, Swift, GDScript, Python, SQL"),
        ("Frameworks and tools", "Next.js, Node.js, Tailwind CSS, Spring Boot, Flutter, egui, FFmpeg, Supabase, "
                                 "Godot, Git, GitHub, GitLab"),
        ("Cloud and infrastructure", "AWS (EC2, S3, CloudFront), network administration, computer assembly and "
                                     "maintenance, information security"),
        ("Practices", "Object-oriented programming, UML, agile methodologies (Scrum, Kanban, XP)"),
        ("Soft skills", "Teamwork, communication, problem solving, proactivity and adaptability"),
        ("Languages spoken", "Portuguese (native), English (advanced)"),
    ],
)


def build(L):
    S = []

    def H(t):
        S.append(CondPageBreak(90))
        S.append(Heading(t))

    S.append(Paragraph("Luís Otávio de Siqueira Pimentel", name_st))
    S.append(Paragraph(L["headline"], headline_st))
    S.append(Spacer(1, 3))
    S.append(Paragraph(
        f'{L["place"]} · {EMAIL} · {PHONE}<br/>'
        + link(LINKEDIN, "linkedin.com/in/luisotaviosiqueira") + " · "
        + link(GITHUB, "github.com/eucomoareia") + " · "
        + link(SITE, "eucomoareia.github.io/Portfolio"), contact_st))
    S.append(Spacer(1, 6))

    H(L["h_summary"])
    S.append(Paragraph(L["summary"], body))
    S.append(Spacer(1, 8))

    H(L["h_edu"])
    for e in L["edu"]:
        S.append(entry(*e))
    H(L["h_exp"])
    for e in L["exp"]:
        S.append(entry(*e))
    H(L["h_proj"])
    for e in L["proj"]:
        S.append(entry(*e))
    H(L["h_extra"])
    for e in L["extra"]:
        S.append(entry(*e))
    H(L["h_cert"])
    for c in L["certs"]:
        S.append(Paragraph(c, bullet, bulletText="•"))
    S.append(Spacer(1, 6))
    H(L["h_skills"])
    for k, v in L["skills"]:
        S.append(Paragraph(f"<b>{k}:</b> {v}", body))

    out = os.path.join(OUT_DIR, L["out"])
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=1.9 * cm, rightMargin=1.9 * cm,
                            topMargin=1.4 * cm, bottomMargin=1.3 * cm, title=L["title"],
                            author="Luís Otávio de Siqueira Pimentel", subject=L["title"],
                            keywords="Full Stack Developer, Java, Spring Boot, Rust, Flutter, AWS")
    doc.build(S)
    print("ok", os.path.normpath(out))


if __name__ == "__main__":
    build(PT)
    build(EN)
