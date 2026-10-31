# ui/components/tts_button.py
"""In-browser Web Speech API audio narration button component."""
import streamlit.components.v1 as components


def render_tts_button(text: str, lang_code: str, btn_label: str):
    """Render an in-browser HTML5 Web Speech synthesizer button."""
    safe_text = text.replace('"', '\\"').replace("\n", " ").replace("'", "\\'")
    components.html(
        f"""
        <button onclick="(function(){{
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance('{safe_text}');
            u.lang = '{lang_code}';
            u.rate = 0.92;
            window.speechSynthesis.speak(u);
        }})()" style="
            background: #1B3A6B; color: #FFFFFF;
            border: none; padding: 6px 14px;
            border-radius: 5px; font-size: 12px;
            font-weight: 600; cursor: pointer;
            letter-spacing: 0.3px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
            {btn_label}
        </button>
        """,
        height=40
    )
