import React, { useState } from 'react';

function Login({ onLogin, onSwitchToSignup }: { onLogin: (name: string) => void, onSwitchToSignup: () => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      alert('Please fill in all fields');
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      const name = email.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase());
      onLogin(name);
    }, 1000);
  };

  return (
    <div style={{
      minHeight: 'calc(100vh - 64px)', display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        background: 'white', borderRadius: '24px', padding: '40px', maxWidth: '440px', width: '100%',
        boxShadow: '0 8px 40px rgba(0,0,0,0.09)', border: '1px solid #f2dbb4'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <span style={{ fontSize: '40px' }}>🧴</span>
          <h1 style={{ fontFamily: 'Georgia, serif', fontSize: '28px', color: '#4a3218', margin: '10px 0' }}>Welcome Back</h1>
          <p style={{ color: '#8b5e24', fontSize: '14px' }}>Sign in to your DermIQ account</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#4a3218', marginBottom: '5px' }}>Email</label>
            <input 
              type="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              style={{ width: '100%', padding: '12px 15px', borderRadius: '12px', border: '1.5px solid #e8c48a', fontSize: '14px', background: '#fdf8f0', color: '#4a3218', outline: 'none' }} 
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#4a3218', marginBottom: '5px' }}>Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              style={{ width: '100%', padding: '12px 15px', borderRadius: '12px', border: '1.5px solid #e8c48a', fontSize: '14px', background: '#fdf8f0', color: '#4a3218', outline: 'none' }} 
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            style={{ width: '100%', padding: '14px', borderRadius: '40px', border: 'none', background: '#8b5e24', color: 'white', fontSize: '16px', fontWeight: 600, cursor: 'pointer' }}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '20px', fontSize: '14px', color: '#8b5e24' }}>
          Don't have an account?{' '}
          <span onClick={onSwitchToSignup} style={{ color: '#4a3218', fontWeight: 600, cursor: 'pointer', textDecoration: 'underline' }}>
            Create one free →
          </span>
        </p>
      </div>
    </div>
  );
}

export default Login;