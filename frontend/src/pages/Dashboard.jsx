// frontend/src/pages/Dashboard.jsx
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../api/client';
import { PlusCircle, BookOpen, Layout } from 'lucide-react';

const Dashboard = () => {
  const [decks, setDecks] = useState([]);
  const [newDeckTitle, setNewDeckTitle] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchDecks = async () => {
    try {
      const response = await apiClient.get('/decks/');
      setDecks(response.data);
    } catch (error) {
      console.error("Failed to fetch decks", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDecks();
  }, []);

  const handleCreateDeck = async (e) => {
    e.preventDefault();
    if (!newDeckTitle.trim()) return;
    try {
      await apiClient.post('/decks/', { title: newDeckTitle });
      setNewDeckTitle('');
      fetchDecks(); // Refresh the list
    } catch (error) {
      alert("Failed to create deck");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm p-4 mb-8">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2 font-bold text-xl text-blue-600">
            <Layout size={24} /> AI Study Deck
          </div>
          <button 
            onClick={() => { localStorage.removeItem('token'); window.location.reload(); }}
            className="text-sm text-gray-500 hover:text-red-500"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">My Decks</h1>

        {/* Create Deck Form */}
        <form onSubmit={handleCreateDeck} className="mb-10 flex gap-4">
          <input
            type="text"
            placeholder="New Deck Title (e.g. JavaScript Design Patterns)"
            className="flex-1 p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 outline-none bg-white"
            value={newDeckTitle}
            onChange={(e) => setNewDeckTitle(e.target.value)}
          />
          <button 
            type="submit"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 flex items-center gap-2 transition"
          >
            <PlusCircle size={20} /> Create Deck
          </button>
        </form>

        {/* Deck Grid */}
        {loading ? (
          <div className="text-center py-10 text-gray-500">Loading your decks...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {decks.map((deck) => (
              <Link 
                key={deck.id} 
                to={`/decks/${deck.id}`}
                className="block p-6 bg-white border rounded-xl shadow-sm hover:shadow-md transition border-gray-100 group"
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-blue-50 text-blue-600 rounded-lg group-hover:bg-blue-600 group-hover:text-white transition">
                    <BookOpen size={24} />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-gray-800">{deck.title}</h3>
                    <p className="text-sm text-gray-500">View Flashcards</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;