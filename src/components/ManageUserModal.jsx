import { useState } from "react";
import { Eye, EyeOff } from "lucide-react"; // Ícones modernos

function ManageUserModal({ onClose }) {
  const [formState, setFormState] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  const [showPassword, setShowPassword] = useState({
    current: false,
    new: false,
    confirm: false,
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormState((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const togglePassword = (field) => {
    setShowPassword((prev) => ({
      ...prev,
      [field]: !prev[field],
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onClose();
  };

  return (
    <div
      className="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="manage-user-title"
    >
      <div className="modal-card neon-border">
        <header className="modal-header">
          <h3 id="manage-user-title">Gerenciar usuário</h3>
          <button
            type="button"
            className="icon-button"
            onClick={onClose}
            aria-label="Fechar modal"
          >
            ×
          </button>
        </header>

        <p className="modal-subtitle">
          Atualize sua senha de acesso. Certifique-se de usar uma combinação
          segura.
        </p>

        <form className="modal-form" onSubmit={handleSubmit}>
          {/* Senha Atual */}
          <label htmlFor="currentPassword">Senha atual</label>
          <div className="relative w-full">
            <input
              id="currentPassword"
              name="currentPassword"
              type={showPassword.current ? "text" : "password"}
              placeholder="Digite sua senha atual"
              value={formState.currentPassword}
              onChange={handleChange}
              required
              className="w-full bg-[#0e1726] border border-cyan-500/40 text-white rounded-lg px-4 py-2 pr-10 
                         placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/70 transition-all"
            />
            {/* Ícone de olho para mostrar/ocultar a senha */}
            
          </div>

          {/* Nova Senha */}
          <label htmlFor="newPassword">Nova senha</label>
          <div className="relative w-full">
            <input
              id="newPassword"
              name="newPassword"
              type={showPassword.new ? "text" : "password"}
              placeholder="Crie uma nova senha"
              value={formState.newPassword}
              onChange={handleChange}
              required
              minLength={6}
              className="w-full bg-[#0e1726] border border-cyan-500/40 text-white rounded-lg px-4 py-2 pr-10 
                         placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/70 transition-all"
            />
            {/* Ícone de olho para mostrar/ocultar a senha */}
            
          </div>

          {/* Confirmar Nova Senha */}
          <label htmlFor="confirmPassword">Confirmar nova senha</label>
          <div className="relative w-full">
            <input
              id="confirmPassword"
              name="confirmPassword"
              type={showPassword.confirm ? "text" : "password"}
              value={formState.confirmPassword}
              onChange={handleChange}
              placeholder="Repita a nova senha"
              required
              minLength={6}
              className="w-full bg-[#0e1726] border border-cyan-500/40 text-white rounded-lg px-4 py-2 pr-12 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/70 transition-all"
            />
            {/* Ícone de olho para mostrar/ocultar a senha */}
           
          </div>

          {/* Botões */}
          <div className="modal-actions">
            <button
              type="button"
              className="button ghost-button"
              onClick={onClose}
            >
              Cancelar
            </button>
            <button type="submit" className="button primary-button">
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ManageUserModal;
