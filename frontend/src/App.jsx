import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Discover from './pages/Discover';
import Search from './pages/Search';
import Explore from './pages/Explore';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Discover />} />
          <Route path="/search" element={<Search />} />
          <Route path="/explore" element={<Explore />} />
          {/* Fallback */}
          <Route path="*" element={<Discover />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
