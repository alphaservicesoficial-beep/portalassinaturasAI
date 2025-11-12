import { useMemo, useState } from "react";
import Header from "../components/Header.jsx";
import { useEffect, useRef } from "react";
import { getAuth } from "firebase/auth";


const API_URL = "https://kirvano-backend-warn.onrender.com";

const tutorialConfigs = {
  default: {
    tutorialUrl: "",
    credentials: {
      subtitle: "Credenciais rotativas",
      emailLabel: "E-mail",
      emailValue: "testeconcursopdf@gmail.com",
      passwordLabel: "Senha",
      passwordValue: "Gabi0902#",
      actionLabel: "Baixar ADSPOWER",
      actionHref:
        "https://activity.adspower.com/ap/dist/fast/?utm_source=google&utm_medium=cpc&utm_term=Search-Brand-EN-%E5%B7%B4%E8%A5%BF-9.30&utm_content=Brand-exact&utm_campaign=adspower&campaignid=23056423146&adgroupid=186663175152&adid=776294560691&network=g&device=c&locid=9101282&utm_matchtype=e&utm_targetid=kwd-366215528852&gad_source=1&gad_campaignid=23056423146&gbraid=0AAAAACQgKVN6_ZMNJ-tUazQcCwpztrgXi&gclid=Cj0KCQjwgpzIBhCOARIsABZm7vEfjP4iFsfzGFqknaPJajFypCsU50O2kqtugsaKyDWvARc91MtsFawaAt7hEALw_wcB",
      note: "As credenciais são atualizadas periodicamente portanto, caso mude, retorne a esta página para obter os dados mais recentes.",
    },
    generator: {
      title: "Gerar códigos de autenticação",
      greeting:
        "Gere seu código de autenticação de dois fatores para acessar a ferramenta {tool}.",
      hint: "Certifique-se de que você está na opção AUTENTICADOR antes de gerar o código de acesso. O código dura somente 30s.",
      actionLabel: "Gerar código",
      note: "Você pode solicitar até 2 CÓDIGOS válidos por dia. Utilize somente quando necessário.",
    },
  },
};

const highlightGeneratorHint = (hint) => {
  if (!hint || typeof hint !== "string") return hint;
  const sanitized = hint.trim();
  if (sanitized.toLowerCase().includes("autenticador")) {
    return <span className="accent">{sanitized}</span>;
  }
  return sanitized;
};

const fillTemplate = (value, tool) => {
  if (typeof value !== "string") return value;
  return value
    .replace(/{tool}/g, tool.title)
    .replace(/{toolEncoded}/g, encodeURIComponent(tool.title))
    .replace(/{category}/g, tool.categoryTitle || "Ferramenta")
    .replace(
      /{categoryEncoded}/g,
      encodeURIComponent(tool.categoryTitle || "Ferramenta")
    );
};

const mapValues = (object, tool) =>
  Object.fromEntries(
    Object.entries(object).map(([key, val]) => [key, fillTemplate(val, tool)])
  );

function buildContent(tool) {
  const base = tutorialConfigs.default;
  const preset = tutorialConfigs[tool.guideKey] || {};

  const credentials = mapValues(
    { ...base.credentials, ...(preset.credentials || {}) },
    tool
  );
  const generator = mapValues(
    { ...base.generator, ...(preset.generator || {}) },
    tool
  );

  const credentialsOpenInNewTab =
    typeof credentials.actionHref === "string" &&
    /^https?:\/\//i.test(credentials.actionHref);
  const generatorOpenInNewTab =
    typeof generator.actionHref === "string" &&
    /^https?:\/\//i.test(generator.actionHref);

  return {
    tutorialUrl: fillTemplate(preset.tutorialUrl ?? base.tutorialUrl ?? "", tool),
    credentials: { ...credentials, openInNewTab: credentialsOpenInNewTab },
    generator: { ...generator, openInNewTab: generatorOpenInNewTab },
  };
}

function AccessGuidePage({
  tool,
  onBack,
  onLogout,
  onManageUser,
  animateEntry = false,
}) {
  const content = useMemo(() => buildContent(tool), [tool]);
  const { credentials, generator } = content;
  const pageClassName = animateEntry
    ? "access-page access-page--animate"
    : "access-page";

    // --- Estados do código e timer ---
  const [codigo, setCodigo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [timer, setTimer] = useState(0);

const timerRef = useRef(null); 


const auth = getAuth();
const user = auth.currentUser;


const handleGerarCodigo = async () => {
  setLoading(true);
  setError(null);
  setCodigo(null);
  setTimer(0);

  try {
    const response = await fetch(`${API_URL}/gerar-codigo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: user?.email || credentials.emailValue }),

    });

    // Se o status for 403, trata de forma amigável
    if (response.status === 403) {
      const text = await response.text();
      let msg = "Limite de 2 códigos atingido. Tente novamente amanhã.";
      try {
        const json = JSON.parse(text);
        msg = json.error || msg;
      } catch (_) {}
      setError(msg);
      return; // não segue para o resto
    }

    if (!response.ok) {
      const text = await response.text();
      console.warn("Resposta não OK:", response.status, text);
      setError("Erro ao gerar código. Tente novamente mais tarde.");
      return;
    }

    // Se deu tudo certo
    const data = await response.json();
    if (data.ok && data.code) {
      setCodigo(data.code);
      setTimer(30);

      if (timerRef.current) clearInterval(timerRef.current);
      timerRef.current = setInterval(() => {
        setTimer((prev) => {
          if (prev <= 1) {
            clearInterval(timerRef.current);
            timerRef.current = null;
            setCodigo(null);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      setError(data.error || "Não foi possível gerar o código.");
    }
  } catch (err) {
    console.error("Erro de rede:", err);
    setError("Erro ao conectar ao servidor.");
  } finally {
    setLoading(false);
  }
};


useEffect(() => {
  return () => {
    if (timerRef.current) clearInterval(timerRef.current);
  };
}, []);

  return (
    <div className={pageClassName}>
      <Header onLogout={onLogout} onManageUser={onManageUser} />

      <main className="access-content tutorial-layout">
        <button
          type="button"
          className="back-button"
          onClick={onBack}
          aria-label="Voltar para o painel"
        >
          <span className="back-button__icon">←</span>
          <span>Voltar para o painel</span>
        </button>

        <h1 className="tutorial-heading">ASSISTA O TUTORIAL ABAIXO:</h1>

        <section className="tutorial-player neon-border">
          <div className="tutorial-player__frame">
            {content.tutorialUrl ? (
              <iframe
                src={content.tutorialUrl}
                title={`Tutorial de acesso para ${tool.title}`}
                loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            ) : (
              <div className="tutorial-player__placeholder">
                <span className="tutorial-placeholder__badge">Em breve</span>
                <h2>Tutorial em atualização</h2>
                <p>
                  Estamos preparando um novo walkthrough para a {tool.title}.
                  Você receberá um aviso assim que estiver disponível.
                </p>
              </div>
            )}
          </div>
        </section>

        <section className="access-info-row">
          {/* --- Card de credenciais --- */}
          <article className="access-info-card neon-border access-info-card--credentials">
            <header>
              <span className="card-badge" aria-hidden="true">
                <svg className="card-badge__icon" viewBox="0 0 24 24">
                  <circle cx="12" cy="8" r="4" />
                  <path d="M5 18.5c0-3.25 3.35-5.5 7-5.5s7 2.25 7 5.5v1a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1Z" />
                </svg>
              </span>
              <div>
                <h2>DADOS DE ACESSO</h2>
                {credentials.subtitle && <p>{credentials.subtitle}</p>}
              </div>
            </header>

            <dl className="credentials-list">
              <div className="credentials-item">
                <dt>{credentials.emailLabel}</dt>
                <dd>{credentials.emailValue}</dd>
              </div>
              <div className="credentials-item">
                <dt>{credentials.passwordLabel}</dt>
                <dd>{credentials.passwordValue}</dd>
              </div>
            </dl>

            {credentials.actionHref && (
              <a
                className="button primary-button access-card-action"
                href={credentials.actionHref}
                target={credentials.openInNewTab ? "_blank" : undefined}
                rel={
                  credentials.openInNewTab ? "noopener noreferrer" : undefined
                }
              >
                {credentials.actionLabel}
              </a>
            )}

            {credentials.note && (
              <p className="access-card-note">{credentials.note}</p>
            )}
          </article>

          {/* --- Card de código --- */}
    {/* --- Card de código --- */}
<article className="access-info-card neon-border access-info-card--generator">
  <header>
    <h2>{generator.title}</h2>
  </header>

  {generator.greeting && (
    <p className="generator-text">{generator.greeting}</p>
  )}

  {/* --- Área principal --- */}
  <div
    className="generator-callout"
    style={{
      background: "rgba(10, 20, 35, 0.8)",
      border: "1px solid rgba(0, 255, 255, 0.3)",
      borderRadius: "12px",
      padding: "16px",
      textAlign: "center",
      marginBottom: "20px",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minHeight: "120px",
    }}
  >
    {codigo ? (
      <>
        <h1
          style={{
            color: "#00ffff",
            fontSize: "20px",
            fontWeight: "700",
            margin: "0",
            letterSpacing: "4px",
            textAlign: "center",
          }}
        >
          {codigo}
        </h1>
        <p
          style={{
            color: "#00ffff",
            marginTop: "10px",
            fontSize: "14px",
            opacity: 0.8,
          }}
        >
          expira em <strong>{timer}s</strong>
        </p>
      </>
    ) : (
      <>
        <span className="generator-callout__icon">⚠</span>
        <p
          style={{
            color: "#00ffff",
            fontSize: "12px",
            lineHeight: 1.5,
          }}
        >
          Certifique-se de que você está na opção <b>AUTENTICADOR</b> antes de gerar o código de acesso.
          O código dura somente 30 s.
        </p>
      </>
    )}
  </div>

 
   {/* Botão */}
  <button
    onClick={handleGerarCodigo}
    className="button secondary-button access-card-action"
    disabled={loading}
  >
    {loading ? "Buscando..." : generator.actionLabel}
  </button>

  {/* Mensagem amigável de limite ou erro */}
  {/* Erro */} {error && <p className="text-red-500 mt-2">{error}</p>} {generator.note && ( <p className="access-card-note">{generator.note}</p> )}



</article>


        </section>
      </main>
    </div>
  );
}

export default AccessGuidePage;
