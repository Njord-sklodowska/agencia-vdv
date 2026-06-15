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
    <div className="d-flex align-items-center justify-content-center vh-100 flex-column gap-3" style={{ background: 'var(--primary-color)' }}>
      <div className="d-flex align-items-center gap-2 mb-1">
        <i className="bi bi-car-front-fill fs-3" style={{ color: 'var(--contrast-color)' }}></i>
        <span className="fw-semibold fs-4" style={{ color: 'var(--contrast-color)' }}>Agencia VDV</span>
      </div>
      <div className="accent-bar" style={{ width: '160px', marginBottom: '.5rem' }}></div>

      <div className="card login-card shadow-sm" style={{ width: '360px', background: '#fff' }}>
        <div className="card-body p-4">
          <h5 className="mb-1" style={{ color: 'var(--dark-text)', fontWeight: '600' }}>Iniciar sesión</h5>
          <p className="text-muted small mb-4">Ingresá tus credenciales para continuar</p>

          {error && (
            <div className="mb-3 px-3 py-2 rounded small" style={{ background: '#fde8e8', color: '#8b2020' }}>
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
      <p style={{ color: '#a0aec0', fontSize: '11px' }}>Agencia VDV v1.0.0 — Gestión Automotriz</p>
    </div>
  );
};

export default Login;
