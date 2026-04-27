import { useState } from "react";
import { useAuthStore } from "../../store/auth";

export function AuthPanel() {
  const { login, register, status, error } = useAuthStore();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("alex@example.com");
  const [name, setName] = useState("Alex Engineer");
  const [password, setPassword] = useState("password123");

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (mode === "register") {
      await register(email, password, name);
    } else {
      await login(email, password);
    }
  };

  return (
    <section className="auth-card">
      <form onSubmit={submit}>
        <label>
          Email
          <input value={email} type="email" onChange={(event) => setEmail(event.target.value)} />
        </label>
        {mode === "register" ? (
          <label>
            Name
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>
        ) : null}
        <label>
          Password
          <input value={password} type="password" onChange={(event) => setPassword(event.target.value)} />
        </label>
        {error ? <p className="error">{error}</p> : null}
        <button disabled={status === "loading"}>{mode === "login" ? "Sign in" : "Create account"}</button>
      </form>

      <button className="link-button" type="button" onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "Need an account? Register" : "Already registered? Sign in"}
      </button>
    </section>
  );
}
