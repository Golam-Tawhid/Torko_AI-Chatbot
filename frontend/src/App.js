import React, { useEffect, useState } from "react";
import Chat from "./components/Chat";
import ThemeToggle from "./components/ThemeToggle";
import KeyboardShortcuts from "./components/KeyboardShortcuts";
import "./App.css";

function App() {
  const [isDarkTheme, setIsDarkTheme] = useState(false);

  useEffect(() => {
    // Create floating particles
    const createParticle = () => {
      const particle = document.createElement("div");
      particle.className = "particle";
      particle.style.left = Math.random() * 100 + "vw";
      particle.style.width = particle.style.height =
        Math.random() * 10 + 5 + "px";
      particle.style.animationDelay = Math.random() * 15 + "s";
      particle.style.animationDuration = Math.random() * 10 + 10 + "s";
      document.querySelector(".App").appendChild(particle);

      setTimeout(() => {
        particle.remove();
      }, 25000);
    };

    const interval = setInterval(createParticle, 3000);

    // Create initial particles
    for (let i = 0; i < 5; i++) {
      setTimeout(createParticle, i * 1000);
    }

    return () => clearInterval(interval);
  }, []);

  const handleThemeChange = (isDark) => {
    setIsDarkTheme(isDark);
    document.body.className = isDark ? "dark-theme" : "";
  };

  return (
    <div className={`App ${isDarkTheme ? "dark-theme" : ""}`}>
      <ThemeToggle onThemeChange={handleThemeChange} />
      <KeyboardShortcuts />

      <header className="App-header">
        <h1>✨ Torko</h1>
        <p style={{ margin: "10px 0 0 0", opacity: 0.8, fontSize: "1rem" }}>
          Your AI Assistant
        </p>
      </header>
      <main>
        <Chat />
      </main>
    </div>
  );
}

export default App;
