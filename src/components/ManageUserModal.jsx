import { useState } from 'react'

function ManageUserModal({ onClose }) {
  const [formState, setFormState] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  })

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormState((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    onClose()
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="manage-user-title">
      <div className="modal-card neon-border">
        <header className="modal-header">
          <h3 id="manage-user-title">Gerenciar usuário</h3>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Fechar modal">
            ×
          </button>
        </header>
        <p className="modal-subtitle">
          Atualize sua senha de acesso. Certifique-se de usar uma combinação segura.
        </p>
        <form className="modal-form" onSubmit={handleSubmit}>
          <label htmlFor="currentPassword">Senha atual</label>
          <input
            id="currentPassword"
            name="currentPassword"
            type="password"
            placeholder="Digite sua senha atual"
            value={formState.currentPassword}
            onChange={handleChange}
            required
          />

          <label htmlFor="newPassword">Nova senha</label>
          <input
            id="newPassword"
            name="newPassword"
            type="password"
            placeholder="Crie uma nova senha"
            value={formState.newPassword}
            onChange={handleChange}
            required
            minLength={6}
          />

          <label htmlFor="confirmPassword">Confirmar nova senha</label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            placeholder="Repita a nova senha"
            value={formState.confirmPassword}
            onChange={handleChange}
            required
            minLength={6}
          />

          <div className="modal-actions">
            <button type="button" className="button ghost-button" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" className="button primary-button">
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ManageUserModal
