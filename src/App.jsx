import { useState, useEffect } from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from './firebase';

import LoginPage from './pages/LoginPage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import AccessGuidePage from './pages/AccessGuidePage.jsx';
import ManageUserModal from './components/ManageUserModal.jsx';
import ForgotPasswordModal from './components/ForgotPasswordModal.jsx';
import WhatsAppButton from './components/WhatsAppButton.jsx';

function App() {
  const [user, setUser] = useState(null);
  const [isManageUserOpen, setIsManageUserOpen] = useState(false);
  const [selectedTool, setSelectedTool] = useState(null);
  const [isForgotPasswordOpen, setIsForgotPasswordOpen] = useState(false);
  const [shouldAnimateDashboard, setShouldAnimateDashboard] = useState(false);
  const [loading, setLoading] = useState(true);

  // 🔄 Detecta login automático do Firebase (mantém o usuário logado após reload)
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const handleLogin = (firebaseUser) => {
    setUser(firebaseUser);
    setShouldAnimateDashboard(false);
    setSelectedTool(null);
  };

  const handleLogout = async () => {
    await signOut(auth);
    setUser(null);
    setIsManageUserOpen(false);
    setIsForgotPasswordOpen(false);
    setShouldAnimateDashboard(false);
    setSelectedTool(null);
  };

  const handleOpenManageUser = () => setIsManageUserOpen(true);
  const handleCloseManageUser = () => setIsManageUserOpen(false);

  const handleOpenForgotPassword = () => setIsForgotPasswordOpen(true);
  const handleCloseForgotPassword = () => setIsForgotPasswordOpen(false);

  const handleToolSelect = (tool) => {
    setShouldAnimateDashboard(false);
    setSelectedTool({ ...tool, shouldAnimateGuide: true });
  };

  const handleCloseAccessGuide = () => {
    setSelectedTool(null);
    setShouldAnimateDashboard(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-cyan-400 text-xl font-semibold">
        Carregando...
      </div>
    );
  }

  return user ? (
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
  );
}

export default App;
