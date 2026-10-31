# ui/components/tts_button.py
"""Interactive Web Speech audio narrator with play/pause/stop, voice selection, and transcript."""
import html
import streamlit.components.v1 as components


def render_tts_button(text: str, lang_code: str = "en-IN", btn_label: str = "Audio Narration"):
    """
    Renders an accessible speech player with:
    - Play / Pause / Stop controls
    - Multilingual voice selector (Marathi, Hindi, English)
    - Live synchronized transcript display with word highlighting
    """
    safe_text_json = text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    escaped_display = html.escape(text)

    # Determine default dropdown option
    default_lang = lang_code if lang_code in ["mr-IN", "hi-IN", "en-IN", "en-US"] else "en-IN"

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      body {{
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        background: transparent;
      }}
      .player-container {{
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 10px 12px;
        box-sizing: border-box;
      }}
      .controls-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        flex-wrap: wrap;
      }}
      .btn-group {{
        display: flex;
        gap: 6px;
        align-items: center;
      }}
      button.audio-btn {{
        font-size: 11px;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        transition: background 0.15s ease;
      }}
      #btnPlay {{
        background: #1B3A6B;
        color: #FFFFFF;
      }}
      #btnPlay:hover {{
        background: #152E56;
      }}
      #btnPause {{
        background: #475569;
        color: #FFFFFF;
      }}
      #btnPause:hover {{
        background: #334155;
      }}
      #btnStop {{
        background: #94A3B8;
        color: #FFFFFF;
      }}
      #btnStop:hover {{
        background: #64748B;
      }}
      .lang-group {{
        display: flex;
        align-items: center;
        gap: 6px;
      }}
      .lang-label {{
        font-size: 11px;
        color: #64748B;
        font-weight: 600;
      }}
      select.lang-select {{
        font-size: 11px;
        padding: 4px 6px;
        border: 1px solid #CBD5E1;
        border-radius: 4px;
        background: #FFFFFF;
        color: #1E293B;
        outline: none;
      }}
      .status-pill {{
        font-size: 11px;
        font-weight: 600;
        color: #64748B;
        min-width: 65px;
        text-align: right;
      }}
      .transcript-box {{
        margin-top: 8px;
        padding: 8px 10px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        max-height: 72px;
        overflow-y: auto;
      }}
      .transcript-title {{
        font-size: 10px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 3px;
      }}
      .transcript-content {{
        font-size: 12px;
        color: #334155;
        line-height: 1.45;
      }}
      .highlight-word {{
        background-color: #DBEAFE;
        color: #1E40AF;
        font-weight: 700;
        padding: 0 2px;
        border-radius: 2px;
      }}
    </style>
    </head>
    <body>
    <div class="player-container">
      <div class="controls-bar">
        <div class="btn-group">
          <button id="btnPlay" class="audio-btn" onclick="startPlay()">Play</button>
          <button id="btnPause" class="audio-btn" onclick="pausePlay()">Pause</button>
          <button id="btnStop" class="audio-btn" onclick="stopPlay()">Stop</button>
        </div>
        <div class="lang-group">
          <span class="lang-label">Voice:</span>
          <select id="voiceSelect" class="lang-select" onchange="onLangChange(this.value)">
            <option value="mr-IN" {"selected" if "mr" in default_lang else ""}>मराठी (mr-IN)</option>
            <option value="hi-IN" {"selected" if "hi" in default_lang else ""}>हिंदी (hi-IN)</option>
            <option value="en-IN" {"selected" if "en" in default_lang else ""}>English (en-IN)</option>
          </select>
        </div>
        <div id="statusPill" class="status-pill">Ready</div>
      </div>
      <div class="transcript-box">
        <div class="transcript-title">Spoken Transcript</div>
        <div id="transcriptDisplay" class="transcript-content">{escaped_display}</div>
      </div>
    </div>

    <script>
      var rawText = "{safe_text_json}";
      var chosenLang = "{default_lang}";
      var currentUtterance = null;
      var isPausedState = false;

      function setStatus(msg, color) {{
        var el = document.getElementById("statusPill");
        if (el) {{
          el.innerText = msg;
          el.style.color = color || "#64748B";
        }}
      }}

      function escapeHtml(str) {{
        return str
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#039;");
      }}

      function resetTranscript() {{
        var box = document.getElementById("transcriptDisplay");
        if (box) {{
          box.innerHTML = escapeHtml(rawText);
        }}
      }}

      function onLangChange(val) {{
        chosenLang = val;
        if (window.speechSynthesis && window.speechSynthesis.speaking) {{
          stopPlay();
          startPlay();
        }}
      }}

      function startPlay() {{
        if (!("speechSynthesis" in window)) {{
          setStatus("Unsupported", "#991B1B");
          return;
        }}

        if (window.speechSynthesis.paused && isPausedState) {{
          window.speechSynthesis.resume();
          isPausedState = false;
          setStatus("Playing", "#15803D");
          return;
        }}

        window.speechSynthesis.cancel();
        currentUtterance = new SpeechSynthesisUtterance(rawText);
        currentUtterance.lang = chosenLang;
        currentUtterance.rate = 0.92;

        currentUtterance.onstart = function() {{
          isPausedState = false;
          setStatus("Playing", "#15803D");
        }};

        currentUtterance.onpause = function() {{
          isPausedState = true;
          setStatus("Paused", "#B45309");
        }};

        currentUtterance.onresume = function() {{
          isPausedState = false;
          setStatus("Playing", "#15803D");
        }};

        currentUtterance.onend = function() {{
          isPausedState = false;
          setStatus("Completed", "#64748B");
          resetTranscript();
        }};

        currentUtterance.onerror = function() {{
          isPausedState = false;
          setStatus("Ready", "#64748B");
          resetTranscript();
        }};

        currentUtterance.onboundary = function(event) {{
          if (event.name === "word" && typeof event.charIndex === "number") {{
            var idx = event.charIndex;
            var len = event.charLength || 6;
            var before = rawText.substring(0, idx);
            var active = rawText.substring(idx, idx + len);
            var after = rawText.substring(idx + len);
            var box = document.getElementById("transcriptDisplay");
            if (box) {{
              box.innerHTML = escapeHtml(before) +
                '<span class="highlight-word">' + escapeHtml(active) + '</span>' +
                escapeHtml(after);
            }}
          }}
        }};

        window.speechSynthesis.speak(currentUtterance);
      }}

      function pausePlay() {{
        if (window.speechSynthesis && window.speechSynthesis.speaking && !window.speechSynthesis.paused) {{
          window.speechSynthesis.pause();
          isPausedState = true;
          setStatus("Paused", "#B45309");
        }}
      }}

      function stopPlay() {{
        if (window.speechSynthesis) {{
          window.speechSynthesis.cancel();
          isPausedState = false;
          setStatus("Ready", "#64748B");
          resetTranscript();
        }}
      }}
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=135)
