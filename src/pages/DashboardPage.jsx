import { useMemo, useRef, useState } from 'react'
import Header from '../components/Header.jsx'
import ToolCarousel from '../components/ToolCarousel.jsx'

import img123rf from '../img/123RF.png'
import adsparoImage from '../img/ADSPARO.png'
import ahrefsElementsImage from '../img/AHREFSELEMENTS.png'
import alsoAskedImage from '../img/ALSO ASKED.png'
import aluraImage from '../img/ALURA.png'
import artlistImage from '../img/ARTLIST.png'
import buzzsumoImage from '../img/BUZZSUMO.png'
import bypassGptHumanGuruImage from '../img/BYPASSGPTHUMANGURU.png'
import canvaImage from '../img/CANVA.png'
import capcutImage from '../img/CAPCUT.png'
import digenImage from '../img/DIGEN.png'
import dinorankImage from '../img/DINORANK.png'
import dreamfaceImage from '../img/DREAMFACE.png'
import envatoElementsImage from '../img/ENVATO ELEMENTS.png'
import flaticonImage from '../img/FLATICON.png'
import freepikImage from '../img/FREEPIK.png'
import gammaAppImage from '../img/GAMMAAPP.png'
import gptSoraImage from '../img/GPT+SORA.png'
import grokImage from '../img/GROK.png'
import haloScanImage from '../img/HALOSCAN.png'
import helium10Image from '../img/HELIUM 10.png'
import heygenImage from '../img/HEYGEN.png'
import ideogramImage from '../img/IDEOGRAM.png'
import leonardoImage from '../img/LEONARDOAI.png'
import majesticImage from '../img/MAJESTIC.png'
import mangoolsElementsImage from '../img/MANGOOLSELEMENTS.png'
import motionArrayImage from '../img/MOTION ARRAY.png'
import pexdaImage from '../img/PEXDA.png'
import placeitImage from '../img/PLACEIT.png'
import quetextImage from '../img/QUETEXT.png'
import quillbotHumanGuruImage from '../img/QUILLBOTHUMANGURU.png'
import seRankingImage from '../img/SE RANKING.png'
import semrushBusinessElementsImage from '../img/SEMRUSH BUSINESSELEMENTS.png'
import semrushGuruImage from '../img/SEMRUSH GURU.png'
import semrushProImage from '../img/SEMRUSH PRO.png'
import seobserverImage from '../img/SEOBSERVER.png'
import seoptimerElementsImage from '../img/SEOPTIMERELEMENTS.png'
import serpstatElementsImage from '../img/SERPSTATELEMENTS.png'
import similarWebBusinessElementsImage from '../img/SIMILAR WEBBUSINESSELEMENTS.png'
import smartScoutImage from '../img/SMARTSCOUT.png'
import smodinHumanGuruImage from '../img/SMODINHUMANGURU.png'
import spyfuWebBusinessElementsImage from '../img/SPYFUWEBBUSINESSELEMENTS.png'
import storyblocksImage from '../img/STORYBLOCKS.png'
import ubersuggestElementsImage from '../img/UBERSUGGESTELEMENTS.png'
import vectorizerImage from '../img/VECTORIZER.png'
import voiceCloneImage from '../img/VOICE CLONE.png'
import wincherImage from '../img/WINCHER.png'
import woorankImage from '../img/WOORANK.png'
import wordAiImage from '../img/WORDAI.png'
import writeHumanGuruImage from '../img/WRITE HUMANGURU.png'
import youComImage from '../img/YOU.COM.png'
import yourTextGuruImage from '../img/YOURTEXT GURU.png'
import zonbaseImage from '../img/ZONBASE.png'

const sections = [
  {
    title: 'Conteúdo Inteligente',
    itemsPerView: 4,
    tools: [
      {
        title: 'ChatGPT + Sora',
        description: 'Planeje roteiros e storyboards prontos para geração de cenas com o Sora.',
        image: gptSoraImage,
      },
      {
        title: 'Grok',
        description: 'Analise tendências e responda perguntas com dados em tempo real do X.',
        image: grokImage,
      },
      {
        title: 'Digen',
        description: 'Centralize dados de growth e simule cenários estratégicos com IA.',
        image: digenImage,
      },
      {
        title: 'GammaApp',
        description: 'Estruture apresentações e narrativas multimídia a partir de comandos curtos.',
        image: gammaAppImage,
      },
      {
        title: 'QuillBot Human Guru',
        description: 'Reescreva conteúdos com fluidez humana ajustando tom e clareza automaticamente.',
        image: quillbotHumanGuruImage,
      },
      {
        title: 'Smodin Human Guru',
        description: 'Gere redações, resumos e traduções com suporte a múltiplos idiomas.',
        image: smodinHumanGuruImage,
      },
      {
        title: 'WordAI',
        description: 'Parafraseie textos com alta naturalidade preservando intenção e SEO.',
        image: wordAiImage,
      },
      {
        title: 'Write HumanGuru',
        description: 'Crie artigos completos e listas otimizadas com assistência contextual.',
        image: writeHumanGuruImage,
      },
      {
        title: 'YourText Guru',
        description: 'Otimize descrições e fichas de produto com recomendações de palavras-chave.',
        image: yourTextGuruImage,
      },
      {
        title: 'Bypass GPT HumanGuru',
        description: 'Personalize respostas generativas para contornar filtros e preservar naturalidade.',
        image: bypassGptHumanGuruImage,
      },
    ],
  },
  {
    title: 'Edição e Designer',
    itemsPerView: 4,
    tools: [
      {
        title: 'HeyGen',
        description: 'Crie vídeos com apresentadores virtuais, traduções labiais e roteiros automatizados.',
        image: heygenImage,
      },
      {
        title: 'Voice Clone',
        description: 'Replique vozes humanas em múltiplos idiomas mantendo timbre e emoção.',
        image: voiceCloneImage,
      },
      {
        title: 'Ideogram',
        description: 'Gere artes conceituais com tipografia coerente usando prompts detalhados.',
        image: ideogramImage,
      },
      {
        title: 'Leonardo AI',
        description: 'Produza renders hiper-realistas e variações com modelos ajustáveis.',
        image: leonardoImage,
      },
      {
        title: 'DreamFace',
        description: 'Transforme retratos com filtros avançados e geração facial realista.',
        image: dreamfaceImage,
      },
      {
        title: 'Canva',
        description: 'Crie layouts profissionais com recursos colaborativos e branding controlado.',
        image: canvaImage,
      },
      {
        title: 'CapCut',
        description: 'Edite vídeos verticais com automações de corte, legendas dinâmicas e efeitos 9:16.',
        image: capcutImage,
      },
      {
        title: 'Envato Elements',
        description: 'Acesse um arsenal premium de templates, fontes e efeitos para acelerar entregas.',
        image: envatoElementsImage,
      },
      {
        title: 'Freepik',
        description: 'Encontre vetores, mockups e fotos prontos para campanhas digitais.',
        image: freepikImage,
      },
      {
        title: 'Flaticon',
        description: 'Baixe ícones consistentes para reforçar a identidade visual de projetos.',
        image: flaticonImage,
      },
      {
        title: 'Placeit',
        description: 'Gere mockups profissionais e identidades visuais em poucos cliques.',
        image: placeitImage,
      },
      {
        title: 'Vectorizer',
        description: 'Converta imagens em vetores nítidos com ajustes guiados por IA.',
        image: vectorizerImage,
      },
    ],
  },
  {
    title: 'Bibliotecas Criativas',
    guideKey: 'bibliotecas-criativas',
    itemsPerView: 4,
    tools: [
      {
        title: '123RF',
        description: 'Banco com milhões de imagens, vídeos e músicas prontos para uso comercial.',
        image: img123rf,
      },
      {
        title: 'Artlist',
        description: 'Trilhas sonoras e SFX com licenciamento simples para produções premium.',
        image: artlistImage,
      },
      {
        title: 'Motion Array',
        description: 'Templates de vídeo, LUTs e presets para acelerar edições.',
        image: motionArrayImage,
      },
      {
        title: 'Storyblocks',
        description: 'Clipes, animações e efeitos sonoros ilimitados em assinatura anual.',
        image: storyblocksImage,
      },
    ],
  },
  {
    title: 'Mineração de Produtos',
    itemsPerView: 4,
    tools: [
      {
        title: 'Adsparo',
        description: 'Identifique anúncios vencedores e escaláveis em diferentes plataformas.',
        image: adsparoImage,
      },
      {
        title: 'Helium 10',
        description: 'Domine vendas na Amazon com pesquisa de produtos e gestão de listagens.',
        image: helium10Image,
      },
      {
        title: 'SmartScout',
        description: 'Mapeie marcas e vendedores promissores no marketplace da Amazon.',
        image: smartScoutImage,
      },
      {
        title: 'Zonbase',
        description: 'Encontre produtos lucrativos e avalie palavras-chave para operações FBA.',
        image: zonbaseImage,
      },
      {
        title: 'Pexda',
        description: 'Descubra produtos virais para e-commerce monitorando tendências globais.',
        image: pexdaImage,
      },
    ],
  },
  {
    title: 'Pesquisa e Tendências',
    itemsPerView: 4,
    tools: [
      {
        title: 'Also Asked',
        description: 'Mapeie perguntas relacionadas para enriquecer pautas e FAQ.',
        image: alsoAskedImage,
      },
      {
        title: 'BuzzSumo',
        description: 'Descubra tópicos e conteúdos virais monitorando redes e blogs.',
        image: buzzsumoImage,
      },
      {
        title: 'HaloScan',
        description: 'Monitore menções e reputação da marca em diversos canais.',
        image: haloScanImage,
      },
      {
        title: 'Quetext',
        description: 'Verifique plágio e originalidade com relatórios detalhados e sugestões de citações.',
        image: quetextImage,
      },
      {
        title: 'You.com',
        description: 'Pesquise em tempo real com respostas contextuais e integrações de IA multimodal.',
        image: youComImage,
      },
    ],
  },
  {
    title: 'SEO e Performance',
    guideKey: 'seo-performance',
    itemsPerView: 4,
    tools: [
      {
        title: 'Ahrefs Elements',
        description: 'Audite backlinks e identifique oportunidades de tráfego com métricas aprofundadas.',
        image: ahrefsElementsImage,
      },
      {
        title: 'Mangools Elements',
        description: 'Combine KWFinder, SERPChecker e LinkMiner para análises rápidas.',
        image: mangoolsElementsImage,
      },
      {
        title: 'SE Ranking',
        description: 'Acompanhe posições orgânicas e gere relatórios automáticos para clientes.',
        image: seRankingImage,
      },
      {
        title: 'SEMrush Pro',
        description: 'Suite de growth com pesquisa de palavras-chave e auditoria técnica.',
        image: semrushProImage,
      },
      {
        title: 'SEMrush Guru',
        description: 'Recursos avançados para equipes de conteúdo colaborarem com dados sólidos.',
        image: semrushGuruImage,
      },
      {
        title: 'SEMrush Business Elements',
        description: 'Relatórios empresariais com limites elevados e integrações de BI.',
        image: semrushBusinessElementsImage,
      },
      {
        title: 'SEObserver',
        description: 'Monitore SERPs e detecte movimentos decisivos dos concorrentes.',
        image: seobserverImage,
      },
      {
        title: 'SEOptimer Elements',
        description: 'Gere auditorias SEO white-label em segundos.',
        image: seoptimerElementsImage,
      },
      {
        title: 'Serpstat Elements',
        description: 'Mapeie keywords, backlinks e PPC em um painel unificado.',
        image: serpstatElementsImage,
      },
      {
        title: 'SimilarWeb Business Elements',
        description: 'Compare tráfego e origens de audiência com benchmarks competitivos.',
        image: similarWebBusinessElementsImage,
      },
      {
        title: 'SpyFu Web Business Elements',
        description: 'Descubra campanhas pagas e termos orgânicos dos principais rivais.',
        image: spyfuWebBusinessElementsImage,
      },
      {
        title: 'Ubersuggest Elements',
        description: 'Identifique ideias de conteúdo e clusters de palavras-chave com facilidade.',
        image: ubersuggestElementsImage,
      },
      {
        title: 'Wincher',
        description: 'Monitore posições diárias com alertas configuráveis e relatórios claros.',
        image: wincherImage,
      },
      {
        title: 'Woorank',
        description: 'Automatize relatórios de SEO, usabilidade e tecnologias do site.',
        image: woorankImage,
      },
      {
        title: 'Dinorank',
        description: 'Analise interlinking e densidade semântica para escalar conteúdo.',
        image: dinorankImage,
      },
      {
        title: 'Majestic',
        description: 'Explore gráficos de backlinks com métricas como Trust Flow e Citation Flow.',
        image: majesticImage,
      },
      {
        title: 'Alura',
        description: 'Participe de formações em tecnologia, negócios e criação com suporte de especialistas.',
        image: aluraImage,
      },
    ],
  },
]

const guideKeyBySectionTitle = {
  'Conteúdo Inteligente': 'conteudo-inteligente',
  'Edição e Designer': 'edicao-designer',
  'Bibliotecas Criativas': 'bibliotecas-criativas',
  'Mineração de Produtos': 'mineracao-produtos',
  'Pesquisa e Tendências': 'pesquisa-tendencias',
  'SEO e Performance': 'seo-performance',
  'Formação e Comunidade': 'formacao-comunidade',
}

function DashboardPage({ onLogout, onManageUser, onToolSelect, animateEntry = false }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [isSearchActive, setIsSearchActive] = useState(false)

  const searchFieldRef = useRef(null)
  const searchInputRef = useRef(null)

  const normalizedQuery = searchTerm.trim().toLowerCase()

  const sectionsToRender = useMemo(() => {
    if (!normalizedQuery) {
      return sections
    }

    return sections
      .map((section) => {
        const filteredTools = section.tools.filter((tool) => {
          const haystack = `${tool.title} ${tool.description}`.toLowerCase()
          return haystack.includes(normalizedQuery)
        })

        return { ...section, tools: filteredTools }
      })
      .filter((section) => section.tools.length > 0)
  }, [normalizedQuery])

  const totalResults = useMemo(
    () => sectionsToRender.reduce((accumulator, section) => accumulator + section.tools.length, 0),
    [sectionsToRender],
  )

  const hasResults = sectionsToRender.length > 0
  const isSearchOpen = isSearchActive || Boolean(searchTerm)

  const focusSearchInput = () => {
    window.requestAnimationFrame(() => {
      searchInputRef.current?.focus()
    })
  }

  const handleToggleSearch = () => {
    if (!isSearchOpen) {
      setIsSearchActive(true)
      focusSearchInput()
    } else if (!searchTerm) {
      setIsSearchActive(false)
    } else {
      focusSearchInput()
    }
  }

  const handleSearchBlur = (event) => {
    const nextTarget = event.relatedTarget
    if (!nextTarget || !searchFieldRef.current?.contains(nextTarget)) {
      setIsSearchActive(false)
    }
  }

  const handleSearchKeyDown = (event) => {
    if (event.key === 'Escape') {
      if (searchTerm) {
        setSearchTerm('')
      } else {
        setIsSearchActive(false)
        searchInputRef.current?.blur()
      }
    }
  }

  const renderSearchField = () => (
    <div className="inline-search">
      <label htmlFor="tool-search" className="visually-hidden">
        Buscar ferramenta
      </label>
      <div
        ref={searchFieldRef}
        className={`search-field ${isSearchOpen ? 'search-field--expanded' : 'search-field--collapsed'}`}
        onBlur={handleSearchBlur}
      >
        <button
          type="button"
          className="search-toggle"
          onClick={handleToggleSearch}
          aria-label="Abrir busca de ferramentas"
        >
          <svg className="search-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M15.5 14h-.79l-.28-.27a6 6 0 1 0-.71.71l.27.28v.79l4.25 4.25a1 1 0 0 0 1.42-1.42Zm-5 1a4.5 4.5 0 1 1 4.5-4.5 4.51 4.51 0 0 1-4.5 4.5Z"
              fill="currentColor"
            />
          </svg>
        </button>
        <input
          id="tool-search"
          ref={searchInputRef}
          className={`search-input ${isSearchOpen ? 'search-input--visible' : 'search-input--hidden'}`}
          type="search"
          placeholder="Pesquisar ferramentas..."
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
          onFocus={() => setIsSearchActive(true)}
          onKeyDown={handleSearchKeyDown}
          autoComplete="off"
          tabIndex={isSearchOpen ? 0 : -1}
        />
        {searchTerm && (
          <button
            type="button"
            className="clear-search"
            onClick={() => setSearchTerm('')}
            aria-label="Limpar busca"
          >
            ×
          </button>
        )}
      </div>
    </div>
  )

  const pageClassName = animateEntry ? 'dashboard-page dashboard-page--animate' : 'dashboard-page'

  return (
    <div className={pageClassName}>
      <Header onLogout={onLogout} onManageUser={onManageUser} />

      <section className="welcome-panel neon-border">
        <h1>
          Bem-vindo ao painel <span className="accent">mais completo</span> de IA do mercado.
        </h1>
        <p>
          Domine as ferramentas mais poderosas do mundo em um só lugar, com acesso rápido, simples e inteligente.
        </p>
      </section>

      {hasResults ? (
        sectionsToRender.map(({ title, tools, guideKey }, index) => {
          const [firstWord, ...restWords] = title.split(' ')
          const restOfTitle = restWords.join(' ')
          const showSearch = index === 0
          const resolvedGuideKey = guideKey || guideKeyBySectionTitle[title] || 'default'

          return (
            <section key={title} className="tools-section">
              <div className="section-header">
                <h2>
                  <span className="accent">{firstWord}</span>
                  {restOfTitle ? ` ${restOfTitle}` : ''}
                </h2>
                {showSearch && renderSearchField()}
              </div>
              {showSearch && normalizedQuery && (
                <p className="search-feedback search-feedback-inline">
                  {totalResults > 0
                    ? `${totalResults} resultado${totalResults > 1 ? 's' : ''} encontrado${
                        totalResults > 1 ? 's' : ''
                      }`
                    : 'Nenhuma ferramenta encontrada.'}
                </p>
              )}
              <ToolCarousel
                tools={tools.map((tool) => ({
                  ...tool,
                  guideKey: tool.guideKey || resolvedGuideKey,
                  categoryTitle: title,
                }))}
                onSelectTool={onToolSelect}
              />
            </section>
          )
        })
      ) : (
        <section className="tools-section">
          <div className="section-header">
            <h2>
              <span className="accent">Resultados</span> disponíveis
            </h2>
            {renderSearchField()}
          </div>
          <p className="search-feedback search-feedback-empty">Nenhuma ferramenta encontrada.</p>
        </section>
      )}
    </div>
  )
}

export default DashboardPage
