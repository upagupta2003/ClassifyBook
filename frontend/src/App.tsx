import React, { useState } from 'react';
import { classifyBook } from './api';
import './App.css';

interface Genre {
  genre: string;
  probability: number;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{ filename: string; genres: Genre[] } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (file) {
      try {
        const classification = await classifyBook(file);
        setResult(classification);
        setError(null);
      } catch (error) {
        console.error('Error classifying book:', error);
        setError('Failed to classify book');
        setResult(null);
      }
    }
  };

  return (
    <div className="App">
      <h1>Book Genre Classifier</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept=".pdf" />
        <button type="submit" disabled={!file}>
          Classify Book
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {result && (
        <div>
          <h2>Classification Result for {result.filename}:</h2>
          <ul>
            {result.genres.map((genre, index) => (
              <li key={index}>
                {genre.genre}: {(genre.probability * 100).toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
