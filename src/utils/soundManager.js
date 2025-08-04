// Simple sound utility for UI feedback
class SoundManager {
  constructor() {
    this.audioContext = null;
    this.enabled = true;
    this.init();
  }

  async init() {
    try {
      this.audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
    } catch (error) {
      console.warn("AudioContext not supported:", error);
      this.enabled = false;
    }
  }

  createBeep(frequency = 440, duration = 100, type = "sine") {
    if (!this.enabled || !this.audioContext) return;

    try {
      const oscillator = this.audioContext.createOscillator();
      const gainNode = this.audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(this.audioContext.destination);

      oscillator.frequency.setValueAtTime(
        frequency,
        this.audioContext.currentTime
      );
      oscillator.type = type;

      gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(
        0.01,
        this.audioContext.currentTime + duration / 1000
      );

      oscillator.start(this.audioContext.currentTime);
      oscillator.stop(this.audioContext.currentTime + duration / 1000);
    } catch (error) {
      console.warn("Sound playback failed:", error);
    }
  }

  playMessageSent() {
    this.createBeep(800, 100);
  }

  playMessageReceived() {
    this.createBeep(400, 150);
  }

  playError() {
    this.createBeep(200, 200);
  }

  playNotification() {
    this.createBeep(600, 120);
  }

  toggle() {
    this.enabled = !this.enabled;
    return this.enabled;
  }
}

const soundManager = new SoundManager();
export default soundManager;
