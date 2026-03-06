Weather MCP

If having issues starting Ollama server using:
```bash
ollama serve
```

logic in client so functions with Ollama  url=http://localhost:11435/api/chat and you may need to set /etc/systemd/system/ollama.service
add this: Environment="OLLAMA_HOST=127.0.0.1:11435"   
Then restart systemd and ollama if on Linux using these commands:
```bash
systemctl daemon-reload
systemctl restart ollama
```
and then ollama serve should work.
```bash
ollama serve
```


