const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'proj')));

// Serve index.html at root
app.get('/', (_req, res) => {
  res.sendFile(path.join(__dirname, 'proj', 'index.html'));
});

app.post('/chat', async (req, res) => {
  const { message } = req.body;

  try {
    const response = await axios.post('http://localhost:11434/api/generate',
      {
        model: "mistral:latest",
        prompt: message,
        stream: false
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    //  Print full response for debugging
    console.log('Raw Ollama response:', JSON.stringify(response.data,null,2));
    console.log('response keys:',Object.keys(response.data));

    const reply = response.data.response;
    console.log('status:',response.status);

    if (!reply) {
      return res.status(500).json({ reply: 'No valid reply from Ollama model' });
    }

    res.json({ reply });

  } catch (error) {
    console.error('Ollama API error:', error.message);
    res.status(500).json({ reply: 'Error connecting to Ollama' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});