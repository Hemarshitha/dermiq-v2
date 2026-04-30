import React, { useState } from 'react';

function SignUp({ onSignup, onSwitchToLogin }: { onSignup: (name: string) => void, onSwitchToLogin: () => void }) {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!firstName || !email || !password) { alert('Fill all fields'); return; }
    setLoading(true);
    setTimeout(() => { setLoading(false); onSignup(firstName + ' ' + lastName); }, 1000);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#fdf8f0', padding: '20px' }}>
      <div style={{ background: 'white', borderRadius: '24px', padding: '40px', maxWidth: '440px', width: '100%', boxShadow: '0 8px 40px rgba(0,0,0,0.09)' }}>
        <div style={{ textAlign: 'center', marginBottom: '25px' }}>
          <span style={{ fontSize: '40px' }}>🧴</span>
          <h1 style={{ fontFamily: 'Georgia, serif', color: '#4a3218' }}>Create Account</h1>
        </div>
        <form onSubmit={handleSubmit}>
          <input type="text" value={firstName} onChange={e => setFirstName(e.target.value)} placeholder="First Name" required
            style={{ width: '100%', padding: '12px', marginBottom: '12px', borderRadius: '12px', border: '1px solid #e8c48a', background: '#fdf8f0' }} />
          <input type="text" value={lastName} onChange={e => setLastName(e.target.value)} placeholder="Last Name"
            style={{ width: '100%', padding: '12px', marginBottom: '12px', borderRadius: '12px', border: '1px solid #e8c48a', background: '#fdf8f0' }} />
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" required
            style={{ width: '100%', padding: '12px', marginBottom: '12px', borderRadius: '12px', border: '1px solid #e8c48a', background: '#fdf8f0' }} />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required
            style={{ width: '100%', padding: '12px', marginBottom: '20px', borderRadius: '12px', border: '1px solid #e8c48a', background: '#fdf8f0' }} />
          <button type="submit" disabled={loading}
            style={{ width: '100%', padding: '14px', borderRadius: '40px', border: 'none', background: '#8b5e24', color: 'white', fontSize: '16px', cursor: 'pointer' }}>
            {loading ? 'Creating...' : 'Create Free Account →'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '15px' }}>
          Have an account? <span onClick={onSwitchToLogin} style={{ color: '#8b5e24', cursor: 'pointer', textDecoration: 'underline' }}>Sign in</span>
        </p>
      </div>
    </div>
  );
}

export default SignUp;