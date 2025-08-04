import React, { useState, useEffect } from "react";
import "./KeyboardShortcuts.css";

const KeyboardShortcuts = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleKeyDown = (event) => {
      // Toggle shortcuts with Ctrl/Cmd + /
      if ((event.ctrlKey || event.metaKey) && event.key === "/") {
        event.preventDefault();
        setIsVisible(!isVisible);
      }
      // Close with Escape
      if (event.key === "Escape") {
        setIsVisible(false);
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isVisible]);

  const shortcuts = [
    { key: "Ctrl + /", action: "Toggle shortcuts" },
    { key: "Enter", action: "Send message" },
    { key: "Shift + Enter", action: "New line" },
    { key: "Escape", action: "Close shortcuts" },
    { key: "Ctrl + L", action: "Clear chat (future)" },
  ];

  if (!isVisible) return null;

  return (
    <div className="shortcuts-overlay" onClick={() => setIsVisible(false)}>
      <div className="shortcuts-modal" onClick={(e) => e.stopPropagation()}>
        <div className="shortcuts-header">
          <h3>⌨️ Keyboard Shortcuts</h3>
          <button className="close-button" onClick={() => setIsVisible(false)}>
            ×
          </button>
        </div>
        <div className="shortcuts-list">
          {shortcuts.map((shortcut, index) => (
            <div key={index} className="shortcut-item">
              <kbd className="shortcut-key">{shortcut.key}</kbd>
              <span className="shortcut-action">{shortcut.action}</span>
            </div>
          ))}
        </div>
        <div className="shortcuts-footer">
          <p>
            Press <kbd>Ctrl + /</kbd> to toggle this panel
          </p>
        </div>
      </div>
    </div>
  );
};

export default KeyboardShortcuts;
