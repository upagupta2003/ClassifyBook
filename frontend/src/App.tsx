import React, { useState } from 'react';
import { classifyBook } from './api';
import './App.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any | null>(null);

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
      } catch (error) {
        console.error('Error classifying book:', error);
        setResult({ error: 'Failed to classify book' });
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
      {result && (
        <div>
          <h2>Classification Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
