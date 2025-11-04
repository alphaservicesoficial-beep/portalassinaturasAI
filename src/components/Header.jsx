import { useEffect, useState } from 'react'
import logoImage from '../logo/Logo Animatoo.png'

function Header({ onLogout, onManageUser }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  useEffect(() => {
    if (!isMenuOpen || typeof window === 'undefined') {
      return undefined
    }

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        setIsMenuOpen(false)
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [isMenuOpen])

  const toggleMenu = () => {
    setIsMenuOpen((open) => !open)
  }

  const handleManageUser = () => {
    setIsMenuOpen(false)
    onManageUser()
  }

  const handleLogout = () => {
    setIsMenuOpen(false)
    onLogout()
  }

  return (
    <>
      <header className={`app-header ${isMenuOpen ? 'app-header--menu-open' : ''}`}>
        <div className="logo-area">
          <span className="logo-emblem">
            <img src={logoImage} alt="Marca Animatoo" loading="lazy" />
          </span>
          <div className="logo-text">
            <strong>Portal de Ferramentas</strong>
            <span>Dominando Animação</span>
          </div>
        </div>

        <div className="header-actions">
          <button type="button" className="icon-pill" onClick={handleManageUser} aria-label="Gerenciar usuário">
            <span className="icon">&#9881;</span>
            <span className="icon-label">Usuário</span>
          </button>
          <button type="button" className="icon-pill icon-pill--danger" onClick={handleLogout} aria-label="Sair">
            <span className="icon">&#x2197;</span>
            <span className="icon-label">Sair</span>
          </button>
        </div>

        <button
          type="button"
          className="header-menu-toggle"
          onClick={toggleMenu}
          aria-label="Abrir menu de navegação"
          aria-expanded={isMenuOpen}
          aria-controls="header-mobile-menu"
        >
          <span className="header-menu-toggle__line" />
          <span className="header-menu-toggle__line" />
          <span className="header-menu-toggle__line" />
        </button>

        <div
          id="header-mobile-menu"
          className={`header-mobile-menu ${isMenuOpen ? 'header-mobile-menu--open' : ''}`}
        >
          <button type="button" onClick={handleManageUser} className="header-mobile-menu__item">
            <span className="header-mobile-menu__icon">&#9881;</span>
            <span>Gerenciar usuário</span>
          </button>
          <button
            type="button"
            onClick={handleLogout}
            className="header-mobile-menu__item header-mobile-menu__item--danger"
          >
            <span className="header-mobile-menu__icon">&#x2197;</span>
            <span>Sair</span>
          </button>
        </div>
      </header>

      {isMenuOpen && <div className="header-menu-backdrop" onClick={() => setIsMenuOpen(false)} aria-hidden="true" />}
    </>
  )
}

export default Header
