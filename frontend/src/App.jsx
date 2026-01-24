import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import WelcomeScreen from './pages/WelcomeScreen';
import RadarScreen from './pages/RadarScreen';
import JoinNetworkScreen from './pages/JoinNetworkScreen';
import SecureVaultScreen from './pages/SecureVaultScreen';
import Dashboard from './pages/Dashboard';
import Layout from './components/Layout';
import LoginScreen from './pages/LoginScreen';
import WalletScreen from './pages/WalletScreen';
import WithdrawalDestinationScreen from './pages/WithdrawalDestinationScreen';
import WithdrawalReviewScreen from './pages/WithdrawalReviewScreen';
import WithdrawalSuccessScreen from './pages/WithdrawalSuccessScreen';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<WelcomeScreen />} />
        <Route path="/login" element={<LoginScreen />} />
        <Route path="/onboarding/radar" element={<RadarScreen />} />
        <Route path="/onboarding/join" element={<JoinNetworkScreen />} />
        <Route path="/onboarding/secure" element={<SecureVaultScreen />} />
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/wallet" element={<Layout><WalletScreen /></Layout>} />
        <Route path="/withdraw/destination" element={<WithdrawalDestinationScreen />} />
        <Route path="/withdraw/review" element={<WithdrawalReviewScreen />} />
        <Route path="/withdraw/success" element={<WithdrawalSuccessScreen />} />
      </Routes>
    </Router>
  );
}

export default App;