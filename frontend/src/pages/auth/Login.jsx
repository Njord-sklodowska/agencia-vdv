import React, { useState } from 'react';
import logoGia from '../../assets/gia.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isHovered, setIsHovered] = useState(false);

  const styles = {
    // page: Ahora usa width: 100% para asegurar que el navegador maneje el ancho correctamente
    page: {
      minHeight: '100vh',
      width: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(200deg, #717d91 30%, #cfdef3 100%)',
      padding: '20px',
      boxSizing: 'border-box'
    },
    // card: width 90% hace que se encoja automáticamente en pantallas pequeñas
    card: {
      width: '90%', 
      maxWidth: '350px', 
      background: '#dddcdc',
      padding: '40px 30px',
      borderRadius: '15px',
      boxShadow: '0 15px 35px rgba(0, 0, 0, 0.57)',
      textAlign: 'center',
      position: 'relative',
      marginTop: '60px',
      boxSizing: 'border-box'
    },
    logoContainer: {
      position: 'absolute',
      top: '-60px',
      left: '50%',
      transform: 'translateX(-50%)',
      width: '80%', 
      maxWidth: '260px',
      height: '90px',
      borderRadius: '10px',
      boxShadow: '0 15px 20px rgba(0,0,0,0.5)',
      overflow: 'hidden',
    },
    title: { fontSize: '2rem', color: '#141414', marginBottom: '5px' },
    subtitle: { fontSize: '1rem', color: '#3a3a3a', marginBottom: '20px' },
    inputGroup: { textAlign: 'left', marginBottom: '15px' },
    label: { display: 'block', fontSize: '0.9rem', color: '#191919', marginBottom: '5px' },
    input: {
      width: '100%',
      padding: '10px',
      border: '1px solid #969494',
      borderRadius: '10px',
      boxSizing: 'border-box'
    },
    buttonContainer: { display: 'flex', justifyContent: 'center', marginTop: '20px' },
    button: {
      padding: '8px 30px',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontWeight: 'bold',
      boxShadow: 'inset 2px 2px 3px rgba(223, 223, 223, 0.6), inset -2px -2px 3px rgba(3, 1, 1, 0.3)',
      backgroundImage: isHovered 
        ? 'linear-gradient(to bottom, #c60e0e 0%, #370303 100%)' 
        : 'linear-gradient(to bottom, #e90b0b 0%, #7d0b0b 100%)', 
      transition: 'all 0.3s ease'
    },
    link: { fontSize: '0.8rem', color: '#141414', marginTop: '15px', display: 'block', textDecoration: 'none' }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.logoContainer}>
          <img src={logoGia} alt="Logo GIA" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
        
        <h2 style={styles.title}>Bienvenido</h2>
        <p style={styles.subtitle}>Inicia sesión en tu cuenta</p>

        <form onSubmit={(e) => e.preventDefault()}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Usuario</label>
            <input type="text" style={styles.input} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Contraseña</label>
            <input type="password" style={styles.input} onChange={(e) => setPassword(e.target.value)} />
          </div>
          
          <div style={styles.buttonContainer}>
            <button 
                type="submit" 
                style={styles.button}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
              Ingresar
            </button>
          </div>
        </form>
        
        <a href="#" style={styles.link}>¿Olvidaste tus datos?</a>
      </div>
    </div>
  );
};

export default Login;