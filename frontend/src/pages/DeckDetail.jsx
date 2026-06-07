// frontend/src/pages/DeckDetail.jsx
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { Sparkles, ArrowLeft, BrainCircuit,Trash2,Edit2,Save,X,PlusCircle } from 'lucide-react';

const DeckDetail = () => {
  const { deckId } = useParams();
  const navigate = useNavigate();

const [activeTab, setActiveTab] = useState("ai");
const [manualFront, setManualFront] = useState("");
const [manualBack, setManualBack] = useState("");
const[isCreatingManual, setIsCreatingManual] = useState(false);
const[editingCard, setEditingCard] = useState(null);
const[editFront, setEditFront] = useState("");
const[editBack, setEditBack] = useState("");
const[isUpdatingCard, setIsUpdatingCard] = useState(false);
const[isRefining, setIsRefining] = useState(false);

const handleCreateManual = async () => {
  if (!manualFront.trim() || !manualBack.trim()) return;
  setIsCreatingManual(true);
  try {
    await apiClient.post(`/flashcards/${deckId}`, {
      front: manualFront,
      back: manualBack
    });
    setManualFront("");
    setManualBack("");
    setIsCreatingManual(false);
    fetchDeck();
  } catch (error) {
    alert("Failed to create manual flashcard.");
  }finally{
    setIsCreatingManual(false);
  }
};

const handleRephrase= async()=>{
  if(!manualFront.trim() ||!manualBack.trim())return;
  setIsRefining(true);
  try{
   const response = await apiClient.post('/flashcards/rephrase',{
    front:manualFront,
    back:manualBack
   }) 
   setManualFront(response.data.front);
   setManualBack(response.data.back);
   alert("Card rephrased successfully!")
  } catch (error) {
    alert("Failed to rephrase flashcard.");
  }finally{
    setIsRefining(false);
  }
}

const handleStartEdit = (card) => {
  setEditingCard(card);
  setEditFront(card.front);
  setEditBack(card.back);
};

const handleCancelEdit = () => {
  setEditingCard(null);
};

const handleUpdateCard = async () => {
  if (!editingCard) return;
  if (!editFront.trim() || !editBack.trim()) return;
  setIsUpdatingCard(true);
  try {
    await apiClient.put(`/flashcards/${editingCard.id}`, {
      front: editFront,
      back: editBack
    });
    setEditingCard(null);
    fetchDeck();
  } catch (error) {
    alert("Failed to update flashcard.");
  }finally{
    setIsUpdatingCard(false);
  }
};

const handleDeleteCard = async (cardId) => {
  if (!window.confirm("Are you sure you want to delete this flashcard?")) return;
  try {
    await apiClient.delete(`/flashcards/${cardId}`);
    fetchDeck();
  } catch (error) {
    alert("Failed to delete flashcard.");
  }
};
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
      <div className="bg-white rounded-2xl border-2 border-blue-100 shadow-sm mb-10 overflow-hidden">
        <div className="flex border-b border-gray-100 bg-gray-50">
          <button
            onClick={() => setActiveTab('ai')}
            className={`flex-1 py-4 px-6 font-bold flex items-center justify-center gap-2 border-b-2 transition ${
              activeTab === 'ai'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <Sparkles size={18} /> AI Flashcard Generator
          </button>
          <button
            onClick={() => setActiveTab('manual')}
            className={`flex-1 py-4 px-6 font-bold flex items-center justify-center gap-2 border-b-2 transition ${
              activeTab === 'manual'
                ? 'border-blue-600 text-blue-600 bg-white'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <PlusCircle size={18} /> Add Card Manually
          </button>
        </div>

        <div className="p-6">
          {activeTab === 'ai' ? (
            <div>
              <p className="text-sm text-gray-500 mb-4">Paste your study notes or reference text below, and AI will automatically generate front/back cards.</p>
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
          ) : (
            <div className="space-y-4">
              <p className="text-sm text-gray-500">Create a flashcard manually by providing the front question/term and the back answer/definition.</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] font-black text-blue-500 uppercase tracking-widest block mb-1">Front Side</label>
                  <textarea
                    className="w-full p-3 border border-gray-200 rounded-xl h-24 outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
                    placeholder="Enter card question or term..."
                    value={manualFront}
                    onChange={(e) => setManualFront(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest block mb-1">Back Side</label>
                  <textarea
                    className="w-full p-3 border border-gray-200 rounded-xl h-24 outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
                    placeholder="Enter answer or definition..."
                    value={manualBack}
                    onChange={(e) => setManualBack(e.target.value)}
                    required
                  />
                </div>
              </div>

              {/* Side-by-side Button Layout */}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={handleRephrase}
                  disabled={isRefining || isCreatingManual || (!manualFront.trim() && !manualBack.trim())}
                  className="flex-1 py-4 rounded-xl font-bold text-blue-600 border-2 border-blue-600 flex items-center justify-center gap-2 transition hover:bg-blue-50 disabled:border-gray-200 disabled:text-gray-400 disabled:hover:bg-transparent"
                >
                  {isRefining ? "Optimizing..." : "✨ Improve with AI"}
                </button>
                <button
                  type="button"
                  onClick={handleCreateManual}
                  disabled={isCreatingManual || isRefining || !manualFront.trim() || !manualBack.trim()}
                  className={`flex-1 py-4 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition ${
                    isCreatingManual ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200'
                  }`}
                >
                  {isCreatingManual ? (
                    <>Creating Flashcard...</>
                  ) : (
                    <>
                      <PlusCircle size={20} /> Add Flashcard
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

        </div>
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
          {deck.flashcards?.map((card) => {
            // Check if this specific card is the one we are editing
            const isEditing = editingCard && editingCard.id === card.id;
            
            return (
              <div 
                key={card.id} 
                className="relative group border rounded-xl overflow-hidden shadow-sm hover:border-blue-200 transition bg-white"
              >
                {isEditing ? (
                  /* --- EDITING CARD MODE --- */
                  <div className="p-6 bg-white">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <label className="text-[10px] font-black text-blue-500 uppercase tracking-widest block mb-1">Edit Front</label>
                        <textarea
                          className="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none resize-none h-24"
                          value={editFront}
                          onChange={(e) => setEditFront(e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest block mb-1">Edit Back</label>
                        <textarea
                          className="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none resize-none h-24"
                          value={editBack}
                          onChange={(e) => setEditBack(e.target.value)}
                        />
                      </div>
                    </div>
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={handleCancelEdit}
                        className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-lg text-sm flex items-center gap-1 transition"
                      >
                        <X size={16} /> Cancel
                      </button>
                      <button
                        onClick={handleUpdateCard}
                        disabled={isUpdatingCard || !editFront.trim() || !editBack.trim()}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg text-sm flex items-center gap-1 transition disabled:bg-gray-400"
                      >
                        <Save size={16} /> Save Changes
                      </button>
                    </div>
                  </div>
                ) : (
                  /* --- NORMAL CARD DISPLAY MODE --- */
                  <>
                    {/* Hover actions menu (Absolute top-right corner) */}
                    <div className="absolute top-3 right-3 flex items-center gap-1 md:opacity-0 md:group-hover:opacity-100 transition duration-150">
                      <button 
                        onClick={() => handleStartEdit(card)} 
                        className="p-1.5 bg-white text-gray-500 hover:text-blue-600 rounded-lg border shadow-sm transition"
                        title="Edit Flashcard"
                      >
                        <Edit2 size={15} />
                      </button>
                      <button 
                        onClick={() => handleDeleteCard(card.id)} 
                        className="p-1.5 bg-white text-gray-500 hover:text-red-600 rounded-lg border shadow-sm transition"
                        title="Delete Flashcard"
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-0 md:gap-4">
                      <div className="p-6 border-b md:border-b-0 md:border-r border-gray-100">
                        <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest">Front</span>
                        <p className="mt-2 text-gray-800 font-medium whitespace-pre-wrap">{card.front}</p>
                      </div>
                      <div className="p-6 bg-gray-50">
                        <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Back</span>
                        <p className="mt-2 text-gray-700 whitespace-pre-wrap">{card.back}</p>
                      </div>
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
};

export default DeckDetail;