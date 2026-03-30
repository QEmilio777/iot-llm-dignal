const promptInput = document.getElementById("prompt");
const sendBtn = document.getElementById("sendBtn");
const output = document.getElementById("output");

sendBtn.addEventListener("click", async () => {
  const prompt = promptInput.value.trim();

  if (!prompt) {
    output.textContent = "Escribe una petición antes de enviar.";
    return;
  }

  output.textContent = "Procesando...";

  try {
    const response = await fetch("/api/prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();

    if (!response.ok) {
      output.textContent = data.detail || "Ocurrió un error en el servidor.";
      return;
    }

    output.textContent =
      "Prompt: " + data.prompt + "\n\n" +
      "Salida del modelo: " + data.llm_output + "\n\n" +
      "Respuesta final: " + data.answer;

  } catch (error) {
    output.textContent = "Error de conexión: " + error;
  }
});