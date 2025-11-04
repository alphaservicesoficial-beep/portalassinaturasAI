import { useState } from 'react'
import LoginPage from './pages/LoginPage.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import AccessGuidePage from './pages/AccessGuidePage.jsx'
import ManageUserModal from './components/ManageUserModal.jsx'
import ForgotPasswordModal from './components/ForgotPasswordModal.jsx'
import WhatsAppButton from './components/WhatsAppButton.jsx'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isManageUserOpen, setIsManageUserOpen] = useState(false)
  const [selectedTool, setSelectedTool] = useState(null)
  const [isForgotPasswordOpen, setIsForgotPasswordOpen] = useState(false)
  const [shouldAnimateDashboard, setShouldAnimateDashboard] = useState(false)

  const handleLogin = () => {
    setIsLoggedIn(true)
    setShouldAnimateDashboard(false)
    setSelectedTool(null)
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setIsManageUserOpen(false)
    setIsForgotPasswordOpen(false)
    setShouldAnimateDashboard(false)
    setSelectedTool(null)
  }

  const handleOpenManageUser = () => {
    setIsManageUserOpen(true)
  }

  const handleCloseManageUser = () => {
    setIsManageUserOpen(false)
  }

  const handleOpenForgotPassword = () => {
    setIsForgotPasswordOpen(true)
  }

  const handleCloseForgotPassword = () => {
    setIsForgotPasswordOpen(false)
  }

  const handleToolSelect = (tool) => {
    setShouldAnimateDashboard(false)
    setSelectedTool({ ...tool, shouldAnimateGuide: true })
  }

  const handleCloseAccessGuide = () => {
    setSelectedTool(null)
    setShouldAnimateDashboard(true)
  }

  return isLoggedIn ? (
    <>
      {selectedTool ? (
        <AccessGuidePage
          tool={selectedTool}
          onBack={handleCloseAccessGuide}
          onLogout={handleLogout}
          onManageUser={handleOpenManageUser}
          animateEntry={selectedTool?.shouldAnimateGuide}
        />
      ) : (
        <DashboardPage
          onLogout={handleLogout}
          onManageUser={handleOpenManageUser}
          onToolSelect={handleToolSelect}
          animateEntry={shouldAnimateDashboard}
        />
      )}
      {isManageUserOpen && <ManageUserModal onClose={handleCloseManageUser} />}
      <WhatsAppButton />
    </>
  ) : (
    <>
      <LoginPage onLoginSuccess={handleLogin} onForgotPassword={handleOpenForgotPassword} />
      {isForgotPasswordOpen && <ForgotPasswordModal onClose={handleCloseForgotPassword} />}
      <WhatsAppButton />
    </>
  )
}

export default App
