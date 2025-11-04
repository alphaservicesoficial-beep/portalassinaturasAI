function LoginPage({ onLoginSuccess, onForgotPassword }) {
  const handleSubmit = (event) => {
    event.preventDefault()
    onLoginSuccess()
  }

  return (
    <main className="login-page">
      <section className="login-card neon-border">
        <h1>Portal de Ferramentas de IA</h1>
        <p className="subtitle">
          Explore e gerencie seu arsenal de inteligência artificial em um só lugar.
        </p>
        <form className="login-form" onSubmit={handleSubmit}>
          <label htmlFor="email">E-mail</label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="nome@empresa.com"
            required
            autoComplete="email"
          />

          <label htmlFor="password">Senha</label>
          <input
            id="password"
            name="password"
            type="password"
            placeholder="********"
            required
            autoComplete="current-password"
          />

          <button type="submit" className="button primary-button">
            Entrar
          </button>
          <button type="button" className="link-button" onClick={onForgotPassword}>
            Esqueci minha senha
          </button>
        </form>
      </section>
    </main>
  )
}

export default LoginPage
