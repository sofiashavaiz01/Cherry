# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "streamlit",
# ]
# ///
"""
Cherry Red Scientific Calculator in Streamlit Python (via UV)
Run locally with:
  uv run --with streamlit streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit page
st.set_page_config(
    page_title="Cherry Red Scientific Calculator",
    page_icon="🍒",
    layout="centered"
)

# Center the calculator and hide Streamlit chrome
st.markdown("""
<style>
    .stApp {
        background: #20040a;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    header { visibility: hidden; height: 0%; }
    footer { visibility: hidden; height: 0%; }
    #MainMenu { visibility: hidden; }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 440px !important;
    }
    iframe {
        border-radius: 46px !important;
        box-shadow: 0 25px 60px -15px rgba(92, 6, 29, 0.75);
    }
</style>
""", unsafe_allow_html=True)

# Complete Calculator Component
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }
    body {
      background: transparent;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      min-height: 100vh;
      overflow: hidden;
      outline: none;
    }

    /* Long phone-proportioned shell: Light Cherry Background & Thick Dark Cherry Border */
    .calc-shell {
      width: 100%;
      max-width: 375px;
      min-height: 650px;
      background: linear-gradient(180deg, #fff0f3 0%, #ffe3e8 45%, #ffd4dc 100%);
      border: 10px solid #5c061d;
      border-radius: 46px;
      box-shadow: 0 25px 60px -15px rgba(92, 6, 29, 0.75), inset 0 2px 4px rgba(255, 255, 255, 0.8);
      padding: 16px 18px 24px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }

    /* Top Bar: Left = Scientific Functions (√x), Right = History (🕒) */
    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 4px 6px 0 6px;
    }
    .top-left-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .deg-badge {
      background: #5c061d;
      color: #ffe4e6;
      border: none;
      border-radius: 8px;
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
    }
    .icon-btn {
      background: none;
      border: none;
      outline: none;
      cursor: pointer;
      color: #5c061d;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 38px;
      height: 38px;
      border-radius: 12px;
      transition: all 0.15s ease;
    }
    .icon-btn:hover {
      background: rgba(92, 6, 29, 0.12);
    }
    .icon-btn:active {
      transform: scale(0.9);
    }
    .icon-btn.active {
      background: #5c061d;
      color: #ffffff;
    }

    /* Screen display area */
    .screen-area {
      flex: 1;
      min-height: 160px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 10px 10px 4px 10px;
      cursor: text;
    }
    .expr-history {
      font-size: 16px;
      color: #881337;
      font-family: monospace;
      text-align: right;
      min-height: 22px;
      overflow-x: auto;
      white-space: nowrap;
      margin-bottom: 4px;
    }
    .main-line {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      overflow-x: auto;
      white-space: nowrap;
    }
    .main-number {
      font-size: 46px;
      font-weight: 300;
      color: #4c0518;
      letter-spacing: -0.5px;
      font-family: 'Plus Jakarta Sans', monospace;
      font-variant-numeric: lining-nums tabular-nums;
      line-height: 1;
    }
    .cursor-bar {
      width: 2.5px;
      height: 42px;
      background-color: #9f1239;
      margin-left: 3px;
      border-radius: 2px;
      animation: blink 1s infinite;
    }
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }

    /* Middle horizontal divider pill */
    .divider-pill {
      width: 48px;
      height: 6px;
      background-color: #fda4af;
      border-radius: 10px;
      margin: 12px auto 16px auto;
      cursor: pointer;
      transition: background 0.2s;
    }
    .divider-pill:hover {
      background-color: #fb7185;
    }

    /* Functions Panel: Dark Cherry Buttons */
    .functions-panel {
      display: none;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      background: rgba(255, 255, 255, 0.65);
      border: 1px solid #fecdd3;
      border-radius: 18px;
      padding: 8px;
      margin-bottom: 12px;
      backdrop-blur: 4px;
    }
    .functions-panel.open {
      display: grid;
    }
    .fn-btn {
      height: 36px;
      background: #4c0518;
      color: #ffe4e6;
      border: none;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.1s;
    }
    .fn-btn:active {
      transform: scale(0.92);
      background: #5c061d;
    }

    /* Main Keypad Grid: Filled Dark Cherry Buttons */
    .keypad-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      grid-template-rows: repeat(5, 58px);
      gap: 12px 10px;
      align-items: center;
    }
    .key {
      background: #5c061d;
      color: #ffffff;
      border: none;
      outline: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 56px;
      width: 100%;
      border-radius: 18px;
      padding: 0;
      margin: 0;
      line-height: 1;
      font-size: 26px;
      font-weight: 500;
      font-family: 'Plus Jakarta Sans', sans-serif;
      box-shadow: 0 4px 10px rgba(92, 6, 29, 0.25);
      transition: all 0.12s ease;
      -webkit-tap-highlight-color: transparent;
    }
    .key:active {
      transform: scale(0.9);
      background: #450314;
    }
    .key-op {
      background: #881337;
      color: #fecdd3;
      font-size: 28px;
      font-weight: 600;
    }
    .key-clear {
      background: #5c061d;
      color: #fda4af;
      font-size: 24px;
      font-weight: 700;
    }

    /* Tall Equal Button spanning rows 4 and 5 */
    .key-equals {
      grid-column: 4;
      grid-row: 4 / span 2;
      height: 100%;
      border-radius: 28px;
      background: linear-gradient(180deg, #9f1239 0%, #700d2c 50%, #4c0518 100%);
      color: #ffffff;
      font-size: 34px;
      font-weight: 700;
      box-shadow: 0 8px 18px rgba(136, 19, 55, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.3);
      line-height: 1;
    }
    .key-equals:active {
      transform: scale(0.95);
      background: #700d2c;
    }

    /* History Overlay */
    .history-modal {
      display: none;
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(2px);
      border-radius: 36px;
      z-index: 50;
      flex-direction: column;
      justify-content: flex-end;
    }
    .history-modal.open {
      display: flex;
    }
    .history-card {
      background: #fff0f3;
      border-top: 4px solid #5c061d;
      border-radius: 28px 28px 36px 36px;
      padding: 16px;
      max-height: 80%;
      overflow-y: auto;
    }
    .history-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      border-bottom: 1px solid #fecdd3;
      margin-bottom: 10px;
      font-weight: 700;
      color: #5c061d;
      font-size: 14px;
    }
    .history-item {
      padding: 8px 10px;
      border-radius: 12px;
      background: #ffffff;
      margin-bottom: 6px;
      cursor: pointer;
      border: 1px solid #fce7f3;
    }
    .history-item:hover {
      background: #ffe4e8;
    }
    .history-expr {
      font-size: 12px;
      color: #881337;
      font-family: monospace;
    }
    .history-res {
      font-size: 18px;
      font-weight: 700;
      color: #4c0518;
    }
    #mobile-input {
      position: absolute;
      left: -9999px;
      opacity: 0;
    }
  </style>
</head>
<body tabindex="0">

  <div class="calc-shell" id="calc-shell">
    <!-- Top Bar: Left = Scientific Functions (√x) + DEG, Right = History (🕒) -->
    <div class="top-bar">
      <div class="top-left-group">
        <button class="icon-btn" id="btn-functions-toggle" title="Scientific Functions">
          <span style="font-size: 20px; font-weight: bold; font-family: 'Plus Jakarta Sans', sans-serif;">√x</span>
        </button>
        <button class="deg-badge" id="btn-deg-toggle" title="Toggle Degrees / Radians">DEG</button>
      </div>
      <button class="icon-btn" id="btn-history-toggle" title="Calculation History">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </button>
    </div>

    <!-- Screen Display -->
    <div class="screen-area" id="screen-area">
      <div class="expr-history" id="expr-history"></div>
      <div class="main-line">
        <span class="main-number" id="main-number"></span>
        <span class="cursor-bar"></span>
      </div>
      <div class="divider-pill" id="divider-pill" title="Toggle scientific functions"></div>
    </div>

    <!-- Functions Panel (Dark Cherry Buttons) -->
    <div class="functions-panel" id="functions-panel">
      <button class="fn-btn" onclick="insertToken('sin(')">sin</button>
      <button class="fn-btn" onclick="insertToken('cos(')">cos</button>
      <button class="fn-btn" onclick="insertToken('tan(')">tan</button>
      <button class="fn-btn" onclick="insertToken('ln(')">ln</button>
      <button class="fn-btn" onclick="insertToken('asin(')">sin⁻¹</button>
      <button class="fn-btn" onclick="insertToken('acos(')">cos⁻¹</button>
      <button class="fn-btn" onclick="insertToken('atan(')">tan⁻¹</button>
      <button class="fn-btn" onclick="insertToken('log(')">log</button>
      <button class="fn-btn" onclick="insertToken('sqrt(')">√x</button>
      <button class="fn-btn" onclick="insertToken('^')">xʸ</button>
      <button class="fn-btn" onclick="insertToken('!')">x!</button>
      <button class="fn-btn" onclick="insertToken('π')">π</button>
      <button class="fn-btn" onclick="insertToken('e')">e</button>
      <button class="fn-btn" onclick="insertToken('(')">(</button>
      <button class="fn-btn" onclick="insertToken(')')">)</button>
      <button class="fn-btn" onclick="insertToken('1/')">1/x</button>
    </div>

    <!-- Main Keypad (Dark Cherry Buttons) -->
    <div class="keypad-grid">
      <button class="key key-clear" onclick="clearAll()">C</button>
      <button class="key key-op" onclick="insertToken('÷')">÷</button>
      <button class="key key-op" onclick="insertToken('×')">×</button>
      <button class="key key-clear" onclick="backspace()" title="Backspace">⌫</button>

      <button class="key" onclick="insertToken('7')">7</button>
      <button class="key" onclick="insertToken('8')">8</button>
      <button class="key" onclick="insertToken('9')">9</button>
      <button class="key key-op" onclick="insertToken('−')">−</button>

      <button class="key" onclick="insertToken('4')">4</button>
      <button class="key" onclick="insertToken('5')">5</button>
      <button class="key" onclick="insertToken('6')">6</button>
      <button class="key key-op" onclick="insertToken('+')">+</button>

      <button class="key" onclick="insertToken('1')">1</button>
      <button class="key" onclick="insertToken('2')">2</button>
      <button class="key" onclick="insertToken('3')">3</button>
      <button class="key key-equals" onclick="evaluateExpr()">=</button>

      <button class="key key-op" onclick="insertToken('%')">%</button>
      <button class="key" onclick="insertToken('0')">0</button>
      <button class="key" style="font-weight: bold;" onclick="insertToken('.')">.</button>
    </div>

    <!-- History Overlay -->
    <div class="history-modal" id="history-modal">
      <div class="history-card">
        <div class="history-header">
          <span>Calculation History</span>
          <button style="background:none;border:none;color:#5c061d;font-size:16px;cursor:pointer;" onclick="closeHistory()">✕</button>
        </div>
        <div id="history-list"></div>
      </div>
    </div>
  </div>

  <form onsubmit="event.preventDefault(); evaluateExpr();">
    <input type="text" id="mobile-input" enterkeyhint="go" />
  </form>

  <script>
    let expression = "";
    let result = "";
    let angleMode = "DEG";
    let history = [];

    try {
      const saved = localStorage.getItem("calc_history_cherry");
      if (saved) history = JSON.parse(saved);
    } catch(e) {}

    const exprHistElem = document.getElementById("expr-history");
    const mainNumElem = document.getElementById("main-number");
    const fnPanel = document.getElementById("functions-panel");
    const fnToggleBtn = document.getElementById("btn-functions-toggle");
    const degToggleBtn = document.getElementById("btn-deg-toggle");
    const histModal = document.getElementById("history-modal");
    const histList = document.getElementById("history-list");
    const mobileInput = document.getElementById("mobile-input");

    function updateDisplay() {
      mainNumElem.innerText = result || expression || "0";
      exprHistElem.innerText = result && expression ? expression + " =" : "";
    }

    function insertToken(token) {
      if (result && !expression && /[+−×÷/*^%]/.test(token)) {
        expression = result + token;
      } else {
        expression += token;
      }
      result = "";
      updateDisplay();
      mobileInput.focus();
    }

    function clearAll() {
      expression = "";
      result = "";
      updateDisplay();
    }

    function backspace() {
      if (expression.length > 0) {
        const fnMatches = expression.match(/(asin|acos|atan|sinh|cosh|tanh|sin|cos|tan|log|ln|sqrt)\($/);
        if (fnMatches) {
          expression = expression.slice(0, -fnMatches[0].length);
        } else {
          expression = expression.slice(0, -1);
        }
      }
      result = "";
      updateDisplay();
    }

    function evaluateExpr() {
      if (!expression.trim()) return;
      try {
        let sanitized = expression
          .replace(/×/g, "*")
          .replace(/÷/g, "/")
          .replace(/−/g, "-")
          .replace(/π/g, "Math.PI")
          .replace(/\\be\\b/g, "Math.E")
          .replace(/\\^/g, "**")
          .replace(/(\\d+)!/g, "fact($1)")
          .replace(/(\\d+)%/g, "($1/100)");

        sanitized = sanitized.replace(/(\\d)(\\()/g, "$1*(");
        sanitized = sanitized.replace(/(\\))(\\()/g, "$1*(");
        sanitized = sanitized.replace(/(\\))(\\d)/g, "$1*$2");

        const openP = (sanitized.match(/\\(/g) || []).length;
        const closeP = (sanitized.match(/\\)/g) || []).length;
        if (openP > closeP) sanitized += ")".repeat(openP - closeP);

        const degToRad = (d) => (d * Math.PI) / 180;
        const radToDeg = (r) => (r * 180) / Math.PI;

        const sin = (x) => angleMode === "DEG" ? (Math.abs(x % 180) < 1e-12 ? 0 : Math.sin(degToRad(x))) : Math.sin(x);
        const cos = (x) => angleMode === "DEG" ? (Math.abs(x % 360) === 90 || Math.abs(x % 360) === 270 ? 0 : Math.cos(degToRad(x))) : Math.cos(x);
        const tan = (x) => angleMode === "DEG" ? Math.tan(degToRad(x)) : Math.tan(x);
        const asin = (x) => angleMode === "DEG" ? radToDeg(Math.asin(x)) : Math.asin(x);
        const acos = (x) => angleMode === "DEG" ? radToDeg(Math.acos(x)) : Math.acos(x);
        const atan = (x) => angleMode === "DEG" ? radToDeg(Math.atan(x)) : Math.atan(x);
        const sqrt = (x) => Math.sqrt(x);
        const ln = (x) => Math.log(x);
        const log = (x) => Math.log10(x);
        const fact = (n) => {
          if (n < 0) return NaN;
          let r = 1; for (let i = 2; i <= n; i++) r *= i; return r;
        };

        const res = Function(
          "sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "ln", "log", "fact",
          "'use strict'; return (" + sanitized + ");"
        )(sin, cos, tan, asin, acos, atan, sqrt, ln, log, fact);

        if (res !== undefined && !Number.isNaN(res) && Number.isFinite(res)) {
          const rounded = Number(Math.round(Number(res + "e+11")) + "e-11");
          const formatted = String(rounded);
          history.unshift({ expr: expression, res: formatted });
          try { localStorage.setItem("calc_history_cherry", JSON.stringify(history.slice(0, 50))); } catch(e) {}
          result = formatted;
          expression = "";
        } else {
          result = "Error";
        }
      } catch (e) {
        result = "Error";
      }
      updateDisplay();
    }

    function toggleFunctions() {
      fnPanel.classList.toggle("open");
      fnToggleBtn.classList.toggle("active");
    }
    document.getElementById("btn-functions-toggle").addEventListener("click", toggleFunctions);
    document.getElementById("divider-pill").addEventListener("click", toggleFunctions);

    degToggleBtn.addEventListener("click", () => {
      angleMode = angleMode === "DEG" ? "RAD" : "DEG";
      degToggleBtn.innerText = angleMode;
    });

    document.getElementById("btn-history-toggle").addEventListener("click", () => {
      histModal.classList.add("open");
      renderHistory();
    });
    function closeHistory() {
      histModal.classList.remove("open");
    }
    function renderHistory() {
      if (history.length === 0) {
        histList.innerHTML = "<div style='color:#5c061d;text-align:center;padding:20px;font-size:13px;'>No calculations yet</div>";
        return;
      }
      histList.innerHTML = history.map((item) =>
        '<div class="history-item" onclick="loadHistory(\\'' + item.res + '\\')">' +
          '<div class="history-expr">' + item.expr + '</div>' +
          '<div class="history-res">= ' + item.res + '</div>' +
        '</div>'
      ).join("");
    }
    function loadHistory(val) {
      insertToken(val);
      closeHistory();
    }

    // Comprehensive Keydown Listener for Laptop & Mobile Enter
    window.addEventListener("keydown", (e) => {
      const k = e.key;
      if (k === "Enter" || e.code === "Enter" || e.code === "NumpadEnter" || k === "=") {
        e.preventDefault();
        evaluateExpr();
      } else if (k >= "0" && k <= "9") {
        insertToken(k);
      } else if (k === ".") {
        insertToken(".");
      } else if (k === "+") {
        insertToken("+");
      } else if (k === "-") {
        insertToken("−");
      } else if (k === "*" || k === "x") {
        insertToken("×");
      } else if (k === "/") {
        insertToken("÷");
      } else if (k === "%" || k === "^" || k === "(" || k === ")") {
        insertToken(k);
      } else if (k === "Backspace") {
        backspace();
      } else if (k === "Escape" || k.toLowerCase() === "c") {
        clearAll();
      }
    });

    document.getElementById("screen-area").addEventListener("click", () => {
      mobileInput.focus();
    });

    // Auto focus on load so Enter key works right away in deployments
    window.focus();
    document.body.focus();
    updateDisplay();
  </script>
</body>
</html>
"""

components.html(CALCULATOR_HTML, height=720, scrolling=False)