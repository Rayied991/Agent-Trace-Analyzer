const API_URL = "http://localhost:8000";;

export async function analyzeTrace(
  file: File
) {
  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    `${API_URL}/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(
      "Analysis failed"
    );
  }

  return response.json();
}

export async function getReport(
  reportId: string
) {
  const response =
    await fetch(
      `http://localhost:8000/report/${reportId}`
    );

  if (!response.ok) {
    throw new Error(
      "Report not found"
    );
  }

  return response.json();
}
export async function getHistory() {
  const response =
    await fetch(
      `${API_URL}/history`
    );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch history"
    );
  }

  return response.json();
}
export async function exportPdf(
  file: File
) {
  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    `${API_URL}/export/pdf`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(
      "PDF export failed"
    );
  }

  return response.blob();
}
export async function exportHtml(
  file: File
) {
  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await fetch(
    `${API_URL}/export/html`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(
      "HTML export failed"
    );
  }

  return response.blob();
}