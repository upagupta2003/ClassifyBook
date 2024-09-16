const API_BASE_URL = '/api';

interface Genre {
  genre: string;
  probability: number;
}

interface ClassificationResult {
  filename: string;
  genres: Genre[];
}

export async function classifyBook(file: File): Promise<ClassificationResult> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload-book`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
}
