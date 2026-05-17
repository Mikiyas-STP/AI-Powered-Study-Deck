// frontend/src/pages/DeckDetail.jsx
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { Sparkles, ArrowLeft, BrainCircuit } from 'lucide-react';

const DeckDetail = () => {
  const { deckId } = useParams();
  const navigate = useNavigate();
  const [deck, setDeck] = useState(null);
  const [textContent, setTextContent] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const fetchDeck = async () => {
    try {
      const response = await apiClient.get(`/decks/${deckId}`);
      setDeck(response.data);
    } catch (error) {
      navigate('/dashboard');
    }
  };

  useEffect(() => {
    fetchDeck();
  }, [deckId]);

  const handleGenerate = async () => {
    if (!textContent.trim()) return;
    setIsGenerating(true);
    try {
      // This calls your FastAPI endpoint that uses the Mock AI Service
      await apiClient.post(`/flashcards/generate/${deckId}`, { text_content: textContent });
      setTextContent('');
      fetchDeck(); // Refresh to show the new cards
    } catch (error) {
      alert("AI Generation failed. Ensure your backend is running.");
    } finally {
      setIsGenerating(false);
    }
  };

  if (!deck) return <div className="p-10 text-center">Loading Deck...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <button onClick={() => navigate('/dashboard')} className="flex items-center gap-2 text-gray-500 mb-6 hover:text-blue-600 transition">
        <ArrowLeft size={20} /> Back to Dashboard
      </button>

      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900">{deck.title}</h1>
        <p className="text-gray-500 mt-2">Manage your cards and generate new ones using AI.</p>
      </div>

      {/* AI Input Area */}
      <div className="bg-white p-6 rounded-2xl border-2 border-blue-100 shadow-sm mb-10">
        <h2 className="flex items-center gap-2 font-bold text-blue-700 mb-4 text-lg">
          <Sparkles size={20} className="text-blue-500" /> AI Flashcard Generator
        </h2>
        <textarea
          className="w-full p-4 border border-gray-200 rounded-xl h-40 mb-4 outline-none focus:ring-2 focus:ring-blue-400 transition"
          placeholder="Paste your study notes, an article, or a transcript here..."
          value={textContent}
          onChange={(e) => setTextContent(e.target.value)}
        />
        <button
          onClick={handleGenerate}
          disabled={isGenerating || !textContent.trim()}
          className={`w-full py-4 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition ${
            isGenerating ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200'
          }`}
        >
          {isGenerating ? (
            <>Processing Notes...</>
          ) : (
            <>
              <BrainCircuit size={20} /> Generate Flashcards
            </>
          )}
        </button>
      </div>

      {/* Flashcard List */}
      <div className="space-y-6">
        <h3 className="font-bold text-2xl text-gray-800">
          Flashcards <span className="text-blue-600 bg-blue-50 px-3 py-1 rounded-full text-sm ml-2">{deck.flashcards?.length || 0}</span>
        </h3>
        
        {deck.flashcards?.length === 0 && (
          <div className="text-center py-10 bg-gray-50 rounded-xl border border-dashed border-gray-300 text-gray-400">
            No cards yet. Paste some text above to get started!
          </div>
        )}

        <div className="grid gap-4">
          {deck.flashcards?.map((card) => (
            <div key={card.id} className="grid grid-cols-1 md:grid-cols-2 gap-0 md:gap-4 bg-white border rounded-xl overflow-hidden shadow-sm hover:border-blue-200 transition">
              <div className="p-6 border-b md:border-b-0 md:border-r border-gray-100">
                <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest">Front</span>
                <p className="mt-2 text-gray-800 font-medium">{card.front}</p>
              </div>
              <div className="p-6 bg-gray-50">
                <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Back</span>
                <p className="mt-2 text-gray-700">{card.back}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DeckDetail;