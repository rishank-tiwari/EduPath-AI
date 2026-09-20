import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Badge } from '../components/Badge';
import { GraduationCap, ArrowRight, Lock, Mail, User, AlertCircle, Loader2 } from 'lucide-react';

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { loginUser, registerUser } = useApp();

  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const redirectPath = location.state?.from || location.state?.redirectPath || '/my-path';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!usernameOrEmail && mode === 'login') {
      setError('Please enter your email or username.');
      return;
    }
    if (!password) {
      setError('Please enter your password.');
      return;
    }

    setLoading(true);
    try {
      if (mode === 'login') {
        await loginUser(usernameOrEmail, password);
      } else {
        await registerUser(usernameOrEmail, email || usernameOrEmail, password);
      }
      navigate(redirectPath, { replace: true });
    } catch (err) {
      console.error('Authentication error:', err);
      const msg = err.response?.data?.detail || 'Authentication failed. Please check your credentials and try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-12 space-y-6">
      <div className="text-center space-y-2">
        <div className="w-12 h-12 rounded-2xl bg-orange text-dark flex items-center justify-center font-extrabold mx-auto shadow-subtle">
          <GraduationCap className="w-7 h-7" />
        </div>
        <h1 className="text-2xl font-extrabold text-dark tracking-tight">
          {mode === 'login' ? 'Welcome Back to EduPath' : 'Create Your Learner Account'}
        </h1>
        <p className="text-xs text-content-secondary font-medium">
          Log in to continue your personalized learning journey.
        </p>
      </div>

      <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-6">
        {/* Toggle Mode */}
        <div className="flex bg-canvas p-1 rounded-lg border border-border-subtle">
          <button
            type="button"
            onClick={() => { setMode('login'); setError(null); }}
            className={`flex-1 py-2 text-xs font-bold rounded-md transition-all ${
              mode === 'login' ? 'bg-surface text-dark shadow-subtle' : 'text-content-secondary hover:text-dark'
            }`}
          >
            Log In
          </button>
          <button
            type="button"
            onClick={() => { setMode('register'); setError(null); }}
            className={`flex-1 py-2 text-xs font-bold rounded-md transition-all ${
              mode === 'register' ? 'bg-surface text-dark shadow-subtle' : 'text-content-secondary hover:text-dark'
            }`}
          >
            Create Account
          </button>
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-bold flex items-start gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-bold text-dark block">
              {mode === 'login' ? 'Email or Username' : 'Username'}
            </label>
            <div className="relative">
              <User className="w-4 h-4 absolute left-3 top-3 text-content-muted" />
              <input
                type="text"
                required
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                placeholder={mode === 'login' ? 'learner@edupath.ai' : 'learner123'}
                className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-border-subtle bg-canvas text-dark font-medium focus:outline-none focus:ring-2 focus:ring-orange/30"
              />
            </div>
          </div>

          {mode === 'register' && (
            <div className="space-y-1">
              <label className="text-xs font-bold text-dark block">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3 top-3 text-content-muted" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="learner@edupath.ai"
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-border-subtle bg-canvas text-dark font-medium focus:outline-none focus:ring-2 focus:ring-orange/30"
                />
              </div>
            </div>
          )}

          <div className="space-y-1">
            <label className="text-xs font-bold text-dark block">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 absolute left-3 top-3 text-content-muted" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-border-subtle bg-canvas text-dark font-medium focus:outline-none focus:ring-2 focus:ring-orange/30"
              />
            </div>
          </div>

          <Button
            variant="primary"
            type="submit"
            disabled={loading}
            className="w-full font-extrabold text-xs py-2.5 gap-2 mt-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <span>{mode === 'login' ? 'Log In & Continue' : 'Create Account & Continue'}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </Button>
        </form>
      </Card>
    </div>
  );
}
