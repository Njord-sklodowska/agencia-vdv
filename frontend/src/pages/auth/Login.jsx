import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError('');
    const result = await login(email, password);
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.message);
    }
  };

  return (
    <div className="login-container">
      <div className="login-brand">
        <i className="bi bi-car-front-fill login-brand-icon"></i>
        <span className="login-brand-text">Agencia VDV</span>
      </div>
      <div className="accent-bar login-accent-bar"></div>

      <div className="card login-card shadow-sm">
        <div className="card-body p-4">
          <h5 className="login-title">Iniciar sesión</h5>
          <p className="login-subtitle">Ingresá tus credenciales para continuar</p>

          {error && (
            <div className="login-error">
              <i className="bi bi-exclamation-circle me-1"></i> {error}
            </div>
          )}

          <div className="mb-3">
            <label className="form-label small text-muted">Usuario / Email</label>
            <input
              type="text"
              className="form-control"
              placeholder="pardinho10"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label className="form-label small text-muted">Contraseña</label>
            <input
              type="password"
              className="form-control"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="btn btn-primary-custom w-100 py-2" onClick={handleLogin}>
            <i className="bi bi-box-arrow-in-right me-1"></i> Ingresar
          </button>
        </div>
      </div>
      <p className="login-footer-text">Agencia VDV v1.0.0 — Gestión Automotriz</p>
    </div>
  );
};

export default Login;
