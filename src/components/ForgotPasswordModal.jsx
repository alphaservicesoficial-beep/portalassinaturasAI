import { useState } from 'react'

function ForgotPasswordModal({ onClose }) {
  const [email, setEmail] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()
    onClose()
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="forgot-password-title">
      <div className="modal-card neon-border">
        <header className="modal-header">
          <h3 id="forgot-password-title">Recuperar acesso</h3>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Fechar modal">
            ×
          </button>
        </header>
        <p className="modal-subtitle">
          Informe o e-mail cadastrado e enviaremos instruções para redefinir sua senha.
        </p>
        <form className="modal-form" onSubmit={handleSubmit}>
          <label htmlFor="email-recovery">E-mail</label>
          <input
            id="email-recovery"
            name="email"
            type="email"
            placeholder="nome@empresa.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
          <div className="modal-actions">
            <button type="button" className="button ghost-button" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" className="button primary-button">
              Enviar
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ForgotPasswordModal
