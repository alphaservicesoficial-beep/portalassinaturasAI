import { useState } from 'react'
import { sendPasswordResetEmail } from 'firebase/auth'
import { auth } from '../firebase' // Certifique-se de que você tem a configuração do Firebase exportada de um arquivo 'firebase.js' ou similar.

function ForgotPasswordModal({ onClose }) {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('') // Para lidar com erros, se necessário
  const [success, setSuccess] = useState('') // Mensagem de sucesso

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('') // Limpar qualquer erro anterior
    setSuccess('') // Limpar qualquer mensagem de sucesso anterior

    try {
      // Envia o e-mail de redefinição de senha usando o Firebase
      await sendPasswordResetEmail(auth, email)
      setSuccess('Instruções para redefinir sua senha foram enviadas para o e-mail informado.')
      // Você pode fechar o modal ou executar outra ação aqui, por exemplo:
      // onClose()
    } catch (err) {
      // Lidar com erros (caso o e-mail não esteja registrado ou ocorra algum erro no processo)
      setError('Houve um erro ao enviar as instruções. Verifique se o e-mail está correto.')
      console.error("Erro ao tentar enviar o e-mail de recuperação: ", err)
    }
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

          {/* Exibir mensagens de erro ou sucesso */}
          {error && <p className="text-red-500 text-sm">{error}</p>}
          {success && <p className="text-green-500 text-sm">{success}</p>}

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
