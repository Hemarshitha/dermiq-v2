import React, { useState } from 'react';
import './App.css';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'chat' | 'upload' | 'results' | 'routine'>('home');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const [skinData, setSkinData] = useState<any>(null);
  const [allergyData, setAllergyData] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any>(null);
  const [routine, setRoutine] = useState<any>(null);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chatbot/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputMessage })
      });

      const data = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Unable to connect to server. Please ensure backend is running.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand" onClick={() => setCurrentPage('home')}>
            <span className="nav-logo">🧴</span>
            <span className="nav-title">DermIQ</span>
          </div>
          <div className="nav-links">
            <button className={currentPage === 'home' ? 'nav-link active' : 'nav-link'} onClick={() => setCurrentPage('home')}>Home</button>
            <button className={currentPage === 'chat' ? 'nav-link active' : 'nav-link'} onClick={() => setCurrentPage('chat')}>Chat</button>
            <button className={currentPage === 'upload' ? 'nav-link active' : 'nav-link'} onClick={() => setCurrentPage('upload')}>Analysis</button>
            <button className={currentPage === 'results' ? 'nav-link active' : 'nav-link'} onClick={() => setCurrentPage('results')}>Results</button>
            <button className={currentPage === 'routine' ? 'nav-link active' : 'nav-link'} onClick={() => setCurrentPage('routine')}>My Routine</button>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {currentPage === 'home' && <HomePage onGetStarted={() => setCurrentPage('chat')} />}
        {currentPage === 'chat' && <ChatPage messages={messages} inputMessage={inputMessage} setInputMessage={setInputMessage} sendMessage={sendMessage} isLoading={isLoading} />}
        {currentPage === 'upload' && <UploadPage setSkinData={setSkinData} setAllergyData={setAllergyData} />}
        {currentPage === 'results' && <ResultsPage skinData={skinData} allergyData={allergyData} recommendations={recommendations} setRecommendations={setRecommendations} setRoutine={setRoutine} />}
        {currentPage === 'routine' && <RoutinePage routine={routine} skinData={skinData} />}
      </main>

      <footer className="footer">
        <p>© 2024 DermIQ - AI-Powered Skincare Intelligence</p>
        <p className="footer-sub">Powered by Fine-tuned LLM & RAG Technology</p>
      </footer>
    </div>
  );
}

// Home Page
function HomePage({ onGetStarted }: { onGetStarted: () => void }) {
  return (
    <div className="home-page">
      <div className="hero">
        <h1 className="hero-title">Your Personal AI Skincare Expert</h1>
        <p className="hero-subtitle">Powered by advanced AI with fine-tuned skincare knowledge and intelligent ingredient analysis</p>
        <button className="cta-button" onClick={onGetStarted}>Start Your Skin Journey →</button>
      </div>
      <div className="features">
        <div className="feature-card"><div className="feature-icon">🧠</div><h3>Fine-Tuned AI</h3><p>Specially trained on dermatological data for expert skincare advice</p></div>
        <div className="feature-card"><div className="feature-icon">🔍</div><h3>RAG Intelligence</h3><p>Retrieves and analyzes thousands of skincare ingredients in real-time</p></div>
        <div className="feature-card"><div className="feature-icon">📷</div><h3>Visual Analysis</h3><p>CNN-powered skin type and condition detection from your photos</p></div>
        <div className="feature-card"><div className="feature-icon">🛡️</div><h3>Allergy Safe</h3><p>Automatic allergen detection and ingredient safety verification</p></div>
      </div>
    </div>
  );
}

// Chat Page
function ChatPage({ messages, inputMessage, setInputMessage, sendMessage, isLoading }: any) {
  return (
    <div className="chat-page">
      <div className="chat-header"><h2>💬 Skincare Consultation</h2><p>Chat with our AI to get personalized recommendations</p></div>
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <h3>Welcome to DermIQ! 👋</h3>
            <p>Tell me about your skin concerns:</p>
            <div className="quick-prompts">
              <button onClick={() => setInputMessage("I have oily skin with acne")}>Oily + Acne</button>
              <button onClick={() => setInputMessage("My skin is dry and sensitive")}>Dry + Sensitive</button>
              <button onClick={() => setInputMessage("I need anti-aging routine")}>Anti-aging</button>
              <button onClick={() => setInputMessage("Help with pigmentation")}>Pigmentation</button>
            </div>
          </div>
        )}
        {messages.map((msg: any) => (
          <div key={msg.id} className={`chat-message ${msg.sender}`}>
            <div className="message-avatar">{msg.sender === 'bot' ? '🧴' : '👤'}</div>
            <div className="message-content"><p>{msg.text}</p><span className="message-time">{msg.timestamp.toLocaleTimeString()}</span></div>
          </div>
        ))}
        {isLoading && (
          <div className="chat-message bot"><div className="message-avatar">🧴</div><div className="message-content typing"><span className="dot">.</span><span className="dot">.</span><span className="dot">.</span></div></div>
        )}
      </div>
      <div className="chat-input">
        <input type="text" value={inputMessage} onChange={(e) => setInputMessage(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} placeholder="Describe your skin concerns..." disabled={isLoading} />
        <button onClick={sendMessage} disabled={isLoading}>Send ✨</button>
      </div>
    </div>
  );
}

// Upload Page
function UploadPage({ setSkinData, setAllergyData }: { setSkinData?: (data: any) => void, setAllergyData?: (data: any) => void }) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedReport, setSelectedReport] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [allergyResult, setAllergyResult] = useState<any>(null);
  const [analyzingReport, setAnalyzingReport] = useState(false);
  const [routine, setRoutine] = useState<any>(null);
  const [generatingRoutine, setGeneratingRoutine] = useState(false);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) { setSelectedImage(file); setImagePreview(URL.createObjectURL(file)); setResult(null); setRoutine(null); }
  };

  const handleReportSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) { setSelectedReport(file); setAllergyResult(null); }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) { alert('Please select an image first'); return; }
    setAnalyzing(true); setResult(null); setRoutine(null);
    const formData = new FormData();
    formData.append('file', selectedImage);
    try {
      const response = await fetch('http://localhost:8000/api/analysis/analyze-image', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('Analysis failed');
      const data = await response.json();
      setResult(data);
      if (setSkinData) { setSkinData({ skin_type: data.skin_type, concerns: data.concerns, acne_severity: data.acne_severity, pigmentation: data.pigmentation, confidence: data.confidence }); }
    } catch (error) { alert('Failed to analyze image.'); }
    finally { setAnalyzing(false); }
  };

  const handleReportAnalyze = async () => {
    if (!selectedReport) { alert('Please select an allergy report first'); return; }
    setAnalyzingReport(true);
    const formData = new FormData();
    formData.append('file', selectedReport);
    try {
      const response = await fetch('http://localhost:8000/api/ocr/extract-allergens', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('OCR failed');
      const data = await response.json();
      setAllergyResult(data);
      if (setAllergyData) { setAllergyData(data); }
    } catch (error) { alert('Failed to analyze report.'); }
    finally { setAnalyzingReport(false); }
  };

  const handleGenerateRoutine = async () => {
    if (!result) return;
    setGeneratingRoutine(true);
    try {
      const response = await fetch('http://localhost:8000/api/routine/generate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skin_type: result.skin_type, concerns: result.concerns || [], lifestyle: {}, routine_type: "both" }),
      });
      if (!response.ok) throw new Error('Routine generation failed');
      const data = await response.json();
      setRoutine(data);
    } catch (error) { alert('Failed to generate routine.'); }
    finally { setGeneratingRoutine(false); }
  };

  return (
    <div className="upload-page">
      <h2>📷 Skin Analysis & Results</h2>
      <div className="upload-section">
        <h3>Facial Image</h3><p>Upload a clear photo for skin analysis</p>
        <div className="upload-box">
          {imagePreview ? <img src={imagePreview} alt="Preview" style={{ maxWidth: '200px', borderRadius: '8px' }} /> : <><span className="upload-icon">📸</span><p>Click to upload image</p></>}
          <input type="file" accept="image/*" onChange={handleImageSelect} style={{ marginTop: '10px' }} />
        </div>
        {selectedImage && <p style={{ marginTop: '8px', color: '#8b5e24' }}>✅ Selected: {selectedImage.name}</p>}
        <button onClick={handleAnalyze} disabled={analyzing || !selectedImage} style={{ marginTop: '12px', padding: '10px 24px', background: '#8b5e24', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '16px' }}>{analyzing ? '🔬 Analyzing...' : '🔬 Analyze Image'}</button>
      </div>

      <div className="upload-section">
        <h3>📄 Allergy Report (Optional)</h3><p>Upload your allergy test report to detect allergens</p>
        <div className="upload-box"><span className="upload-icon">📄</span><p>Upload PDF or Image report</p><input type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={handleReportSelect} style={{ marginTop: '10px' }} /></div>
        {selectedReport && <p style={{ marginTop: '8px', color: '#8b5e24' }}>✅ Selected: {selectedReport.name}</p>}
        <button onClick={handleReportAnalyze} disabled={analyzingReport || !selectedReport} style={{ marginTop: '12px', padding: '10px 24px', background: '#8b5e24', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '16px' }}>{analyzingReport ? '🔍 Scanning...' : '🔍 Analyze Report'}</button>
      </div>

      {result && (
        <div className="analysis-results" style={{ marginTop: '30px' }}>
          <h3>📊 Skin Analysis Results</h3>
          <div className="results-grid">
            <div className="result-card"><h3>Skin Type</h3><p className="result-value" style={{ textTransform: 'capitalize' }}>{result.skin_type}</p><p className="result-confidence">Confidence: {(result.confidence * 100).toFixed(0)}%</p></div>
            <div className="result-card"><h3>Concerns</h3><p className="result-value" style={{ fontSize: '16px' }}>{result.concerns?.join(', ') || 'None detected'}</p><p className="result-confidence">Acne Severity: {result.acne_severity}</p></div>
            <div className="result-card"><h3>Pigmentation</h3><p className="result-value" style={{ textTransform: 'capitalize' }}>{result.pigmentation || 'None'}</p></div>
          </div>
          <div className="recommendation-section">
            <h3>💡 Personalized Recommendations</h3>
            {result.recommendations?.map((rec: string, i: number) => (<div key={i} className="product-card"><p className="product-reason">{rec}</p></div>))}
          </div>
          <button className="routine-btn" onClick={handleGenerateRoutine} disabled={generatingRoutine} style={{ marginTop: '20px' }}>{generatingRoutine ? '✨ Generating...' : '✨ Generate My Skincare Routine'}</button>
        </div>
      )}

      {allergyResult && (
        <div className="analysis-results" style={{ marginTop: '30px' }}>
          <h3>🛡️ Allergens Detected</h3>
          <div className="results-grid">
            <div className="result-card"><h3>Allergens Found</h3><p className="result-value" style={{ fontSize: '18px' }}>{allergyResult.allergens_found?.length > 0 ? allergyResult.allergens_found.map((a: any) => a.allergen).join(', ') : 'None detected'}</p><p className="result-confidence">Confidence: {(allergyResult.confidence * 100).toFixed(0)}%</p></div>
          </div>
          {allergyResult.allergens_found?.length > 0 && (
            <div className="recommendation-section">
              <h3>⚠️ Safety Alerts</h3>
              {allergyResult.allergens_found.map((allergen: any, i: number) => (
                <div key={i} className="product-card" style={{ borderLeft: '4px solid #ef4444' }}><h4 style={{ color: '#8b5e24' }}>{allergen.allergen}</h4><p className="product-reason">Severity: <strong>{allergen.severity}</strong></p><p className="product-reason">Category: {allergen.category}</p></div>
              ))}
              <p style={{ marginTop: '12px', color: '#8b5e24', fontWeight: 'bold' }}>⚠️ Avoid products containing these allergens. Always check ingredient labels.</p>
            </div>
          )}
        </div>
      )}

      {routine && (
        <div className="analysis-results" style={{ marginTop: '30px' }}>
          <h3>🌅 Your Personalized Skincare Routine</h3>
          <div className="routine-section" style={{ background: '#fdf8f0', padding: '20px', borderRadius: '12px', marginTop: '20px' }}>
            <h4 style={{ color: '#4a3218' }}>☀️ Morning Routine</h4>
            {routine.morning?.map((step: any, i: number) => (
              <div key={i} style={{ marginBottom: '12px' }}><span style={{ display: 'inline-block', width: '30px', height: '30px', background: '#8b5e24', color: 'white', borderRadius: '50%', textAlign: 'center', lineHeight: '30px', marginRight: '10px' }}>{step.step_number}</span><div style={{ display: 'inline-block' }}><strong>{step.action}</strong> - {step.product}<br /><small style={{ color: '#6d4a1f' }}>{step.instructions}</small></div></div>
            ))}
          </div>
          <div className="routine-section" style={{ background: '#fdf8f0', padding: '20px', borderRadius: '12px', marginTop: '20px' }}>
            <h4 style={{ color: '#4a3218' }}>🌙 Night Routine</h4>
            {routine.night?.map((step: any, i: number) => (
              <div key={i} style={{ marginBottom: '12px' }}><span style={{ display: 'inline-block', width: '30px', height: '30px', background: '#8b5e24', color: 'white', borderRadius: '50%', textAlign: 'center', lineHeight: '30px', marginRight: '10px' }}>{step.step_number}</span><div style={{ display: 'inline-block' }}><strong>{step.action}</strong> - {step.product}<br /><small style={{ color: '#6d4a1f' }}>{step.instructions}</small></div></div>
            ))}
          </div>
          {routine.weekly?.length > 0 && (
            <div className="routine-section" style={{ background: '#fdf8f0', padding: '20px', borderRadius: '12px', marginTop: '20px' }}>
              <h4 style={{ color: '#4a3218' }}>📅 Weekly Treatments</h4>
              {routine.weekly.map((item: any, i: number) => (
                <div key={i} style={{ marginBottom: '12px' }}><span style={{ display: 'inline-block', width: '30px', height: '30px', background: '#8b5e24', color: 'white', borderRadius: '50%', textAlign: 'center', lineHeight: '30px', marginRight: '10px' }}>{i + 1}</span><div style={{ display: 'inline-block' }}><strong>{item.day}</strong> - {item.treatment}<br /><small style={{ color: '#6d4a1f' }}>{item.product}: {item.instructions}</small></div></div>
              ))}
            </div>
          )}
          {routine.explanation && (
            <div className="routine-explanation" style={{ marginTop: '20px' }}><h3>🤖 AI Explanation</h3><p>{routine.explanation}</p></div>
          )}
        </div>
      )}
    </div>
  );
}

// Results Page
function ResultsPage(props: any) {
  const { skinData, allergyData, recommendations, setRecommendations, setRoutine } = props;
  const [loading, setLoading] = useState(false);
  const [naturalRemedies, setNaturalRemedies] = useState<any>(null);

  const fetchRecommendations = async () => {
    if (!skinData?.skin_type) { alert('Please complete skin analysis first. Go to Analysis tab.'); return; }
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/recommendations/get-recommendations', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skin_type: skinData.skin_type, concerns: skinData.concerns || [], allergies: allergyData?.allergens_found?.map((a: any) => a.allergen) || [] }),
      });
      const data = await response.json();
      setRecommendations(data);
      setNaturalRemedies(data.natural_remedies);
    } catch (error) { alert('Failed to get recommendations.'); }
    finally { setLoading(false); }
  };

  const generateRoutineFromResults = async () => {
    if (!skinData?.skin_type) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/routine/generate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skin_type: skinData.skin_type, concerns: skinData.concerns || [], lifestyle: {}, routine_type: "both" }),
      });
      const data = await response.json();
      setRoutine(data);
      alert('✅ Routine generated! Go to "My Routine" tab to view it.');
    } catch (error) { console.error('Error:', error); }
    finally { setLoading(false); }
  };

  return (
    <div className="results-page">
      <h2>📊 Your Personalized Results</h2>
      {skinData && (
        <div className="results-grid" style={{ marginBottom: '20px' }}>
          <div className="result-card"><h3>Skin Type</h3><p className="result-value" style={{ textTransform: 'capitalize' }}>{skinData.skin_type}</p></div>
          <div className="result-card"><h3>Concerns</h3><p className="result-value" style={{ fontSize: '16px' }}>{skinData.concerns?.join(', ') || 'None specified'}</p></div>
          <div className="result-card"><h3>Allergies</h3><p className="result-value" style={{ fontSize: '14px' }}>{allergyData?.allergens_found?.map((a: any) => a.allergen).join(', ') || 'None detected'}</p></div>
        </div>
      )}
      {!recommendations && (
        <button className="cta-button" onClick={fetchRecommendations} disabled={loading} style={{ marginBottom: '30px' }}>{loading ? '🤖 AI Analyzing...' : '🤖 Get AI Recommendations'}</button>
      )}
      {recommendations?.products && (
        <div className="recommendation-section">
          <h3>💊 AI-Recommended Products</h3>
          <p style={{ color: '#8b5e24', marginBottom: '16px' }}>{recommendations.explanation}</p>
          {recommendations.products.map((product: any, i: number) => (
            <div key={i} className="product-card"><h4>{product.name}</h4><p className="product-brand">{product.brand} | {product.category}</p><p className="product-reason">{product.reason}</p>{product.safety_check && <span className="safety-badge safe">✅ Allergy Safe</span>}</div>
          ))}
        </div>
      )}
      {naturalRemedies && naturalRemedies.length > 0 && (
        <div className="recommendation-section">
          <h3>🌿 Traditional & Natural Remedies</h3>
          {naturalRemedies.map((remedy: any, i: number) => (
            <div key={i} className="product-card" style={{ borderLeft: '4px solid #10b981' }}><h4>{remedy.name}</h4><p className="product-reason"><strong>Ingredients:</strong> {remedy.ingredients?.join(', ')}</p><p className="product-reason"><strong>Benefits:</strong> {remedy.benefits}</p></div>
          ))}
        </div>
      )}
      {recommendations?.safety_summary && (
        <div style={{ background: '#f0fdf4', padding: '16px', borderRadius: '12px', marginTop: '20px' }}><p style={{ color: '#166534' }}>🛡️ {recommendations.safety_summary}</p></div>
      )}
      {recommendations && (
        <button className="routine-btn" onClick={generateRoutineFromResults} disabled={loading} style={{ marginTop: '30px' }}>✨ Generate Full Skincare Routine</button>
      )}
    </div>
  );
}

// Routine Page
function RoutinePage(props: any) {
  const { routine, skinData } = props;
  const [loading, setLoading] = useState(false);
  const [localRoutine, setLocalRoutine] = useState<any>(null);

  const displayRoutine = routine || localRoutine;

  const generateRoutine = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/routine/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skin_type: skinData?.skin_type || 'combination',
          concerns: skinData?.concerns || [],
          lifestyle: {},
          routine_type: "both",
        }),
      });
      const data = await response.json();
      setLocalRoutine(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!displayRoutine) {
    return (
      <div className="routine-page" style={{ textAlign: 'center', padding: '60px 20px' }}>
        <h2>🌅 Your Personalized Skincare Routine</h2>
        <p className="routine-subtitle" style={{ color: '#8b5e24', marginBottom: '30px' }}>
          Generate a routine based on your skin profile
        </p>
        <button className="cta-button" onClick={generateRoutine} disabled={loading}>
          {loading ? '✨ Generating...' : '✨ Generate My Routine'}
        </button>
      </div>
    );
  }

  return (
    <div className="routine-page">
      <h2>🌅 Your Personalized Skincare Routine</h2>
      <p className="routine-subtitle">AI-Generated based on your skin profile</p>

      {displayRoutine.morning && displayRoutine.morning.length > 0 && (
        <div className="routine-section">
          <h3>☀️ Morning Routine</h3>
          {displayRoutine.morning.map((step: any, i: number) => (
            <div key={i} className="routine-step">
              <span className="step-number">{step.step_number || i + 1}</span>
              <div className="step-content">
                <h4>{step.action}</h4>
                <p><strong>{step.product}</strong></p>
                <p>{step.instructions}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {displayRoutine.night && displayRoutine.night.length > 0 && (
        <div className="routine-section">
          <h3>🌙 Night Routine</h3>
          {displayRoutine.night.map((step: any, i: number) => (
            <div key={i} className="routine-step">
              <span className="step-number">{step.step_number || i + 1}</span>
              <div className="step-content">
                <h4>{step.action}</h4>
                <p><strong>{step.product}</strong></p>
                <p>{step.instructions}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {displayRoutine.weekly && displayRoutine.weekly.length > 0 && (
        <div className="routine-section">
          <h3>📅 Weekly Treatments</h3>
          {displayRoutine.weekly.map((item: any, i: number) => (
            <div key={i} className="routine-step">
              <span className="step-number">{i + 1}</span>
              <div className="step-content">
                <h4>{item.day} - {item.treatment}</h4>
                <p><strong>{item.product}</strong></p>
                <p>{item.instructions}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {displayRoutine.explanation && (
        <div className="routine-explanation">
          <h3>🤖 AI Explanation</h3>
          <p>{displayRoutine.explanation}</p>
        </div>
      )}
    </div>
  );
}

export default App;