import { useState } from "react";
import {
  signInWithEmailAndPassword,
  setPersistence,
  browserLocalPersistence,
} from "firebase/auth";
import { auth, db } from "../firebase"; // 👈 precisa importar db
import { doc, getDocs, collection, query, where } from "firebase/firestore";
import { Eye, EyeOff } from "lucide-react";

function LoginPage({ onLoginSuccess, onForgotPassword }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      // 🔐 Mantém login persistente
      await setPersistence(auth, browserLocalPersistence);

      // 🔸 Faz login no Firebase Auth
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      const user = userCredential.user;

      // 🔍 Verifica status no Firestore
      const q = query(
        collection(db, "usuarios"),
        where("email", "==", user.email)
      );
      const snapshot = await getDocs(q);

      if (snapshot.empty) {
        setError("Usuário não encontrado no banco de dados.");
        await auth.signOut();
        return;
      }

      const dados = snapshot.docs[0].data();
      const ativo = dados.ativo !== false; // se não existir o campo, assume ativo

      if (!ativo) {
        setError(
          "Sua assinatura foi cancelada ou está atrasada. Regularize para reativar o acesso."
        );
        await auth.signOut();
        return;
      }

      // ✅ Tudo certo, guarda login local
      localStorage.setItem("kirvanoUser", JSON.stringify({ email: user.email }));
      console.log("Usuário logado:", user);
      onLoginSuccess(user);
    } catch (err) {
      console.error("Erro no login:", err);
      setError("E-mail ou senha incorretos.");
    } finally {
      setLoading(false);
    }
  };

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
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="nome@empresa.com"
            required
            autoComplete="email"
            className="input-field"
          />

          <label htmlFor="password">Senha</label>
          <div className="relative w-full">
            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="********"
              required
              autoComplete="current-password"
              className="w-full bg-[#0e1726] border border-cyan-500/40 text-white rounded-lg px-4 py-2 pr-12 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/70 transition-all"
            />
          </div>

          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

          <button
            type="submit"
            className="button primary-button mt-3"
            disabled={loading}
          >
            {loading ? "Entrando..." : "Entrar"}
          </button>

          <button type="button" className="link-button" onClick={onForgotPassword}>
            Esqueci minha senha
          </button>
        </form>
      </section>
    </main>
  );
}

export default LoginPage;
