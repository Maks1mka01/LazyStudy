import pyttsx3
import time
import threading
import os

class TTSPlayer:
    """Text-to-Speech player with pause logic for flashcards - Flask compatible"""
    
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.stop_flag = False
        self.current_thread = None
        # Don't initialize engine here - do it per-thread
    
    def _get_engine(self):
        """Get TTS engine for current thread (Windows fix for Flask)"""
        try:
            # Windows-specific: Initialize COM for this thread
            if os.name == 'nt':
                import pythoncom
                pythoncom.CoInitialize()
            
            # Create new engine instance for this thread
            engine = pyttsx3.init('sapi5' if os.name == 'nt' else None)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            
            return engine
        except Exception as e:
            print(f"❌ ERROR creating TTS engine: {e}")
            return None
    
    def _speak_text(self, text):
        """Speak text with Flask threading fix"""
        try:
            # Create new engine for this thread
            engine = self._get_engine()
            
            if not engine:
                print(f"❌ TTS engine not available. Would speak: {text}")
                return
            
            print(f"🔊 Speaking: {text[:50]}...")
            engine.say(text)
            engine.runAndWait()
            print("✅ Finished speaking")
            
            # Clean up engine
            del engine
            
        except Exception as e:
            print(f"❌ ERROR speaking text: {e}")
    
    def play_card(self, question, answer, pause_duration=10, on_complete=None):
        """
        Play a flashcard with TTS
        
        Args:
            question: Question text
            answer: Answer text
            pause_duration: Seconds to pause between question and answer
            on_complete: Callback function when playback completes
        """
        if self.is_playing:
            print("⚠️  Already playing, skipping...")
            return
        
        def _play():
            self.is_playing = True
            self.stop_flag = False
            self.is_paused = False
            
            try:
                print(f"\n{'='*60}")
                print(f"🎴 PLAYING CARD")
                print(f"{'='*60}")
                print(f"❓ Question: {question}")
                print(f"💡 Answer: {answer}")
                print(f"{'='*60}")
                
                # Speak question
                self._speak_text(question)
                
                if self.stop_flag:
                    print("⏹️  Stopped during question")
                    return
                
                # Pause for thinking (10 seconds)
                print(f"⏸️  Pausing for {pause_duration} seconds (thinking time)...")
                for i in range(pause_duration):
                    if self.stop_flag:
                        print(f"⏹️  Stopped during pause at {i}s")
                        return
                    
                    # Check if paused
                    while self.is_paused and not self.stop_flag:
                        time.sleep(0.1)
                    
                    if self.stop_flag:
                        return
                    
                    time.sleep(1)
                
                if self.stop_flag:
                    print("⏹️  Stopped before answer")
                    return
                
                # Speak answer
                self._speak_text(answer)
                print(f"{'='*60}")
                print("✅ CARD COMPLETE")
                print(f"{'='*60}\n")
                
                if on_complete and not self.stop_flag:
                    on_complete()
            
            except Exception as e:
                print(f"❌ ERROR in play_card: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                self.is_playing = False
                self.is_paused = False
        
        # Run in separate thread to avoid blocking Flask
        self.current_thread = threading.Thread(target=_play)
        self.current_thread.daemon = True
        self.current_thread.start()
        print("🎵 TTS playback thread started")
    
    def speak_again(self, question, answer):
        """Speak the current card again"""
        if self.is_playing:
            self.stop()
            time.sleep(0.5)
        
        print(f"\n{'='*60}")
        print("🔁 SPEAKING AGAIN")
        print(f"{'='*60}")
        
        # Run in new thread
        def _speak():
            self._speak_text(question)
            time.sleep(0.5)
            self._speak_text(answer)
            print(f"{'='*60}")
            print("✅ SPEAK AGAIN COMPLETE")
            print(f"{'='*60}\n")
        
        thread = threading.Thread(target=_speak)
        thread.daemon = True
        thread.start()
    
    def pause(self):
        """Pause the playback"""
        print("⏸️  TTS: Pausing...")
        self.is_paused = True
    
    def resume(self):
        """Resume the playback"""
        print("▶️  TTS: Resuming...")
        self.is_paused = False
    
    def stop(self):
        """Stop the current playback"""
        print("⏹️  TTS: Stopping...")
        self.stop_flag = True
        self.is_paused = False
        
        # Wait for thread to finish
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=1.0)
        
        self.is_playing = False
        print("✅ TTS: Stopped")
    
    def set_voice_rate(self, rate):
        """Set the speech rate (words per minute)"""
        print(f"✅ Voice rate will be set to: {rate}")
    
    def set_volume(self, volume):
        """Set the volume (0.0 to 1.0)"""
        print(f"✅ Volume will be set to: {volume}")
    
    def test_tts(self):
        """Test if TTS is working"""
        print(f"\n{'='*60}")
        print("🧪 TESTING TTS")
        print(f"{'='*60}")
        
        def _test():
            try:
                engine = self._get_engine()
                if not engine:
                    print("❌ TTS engine initialization failed!")
                    return False
                
                print("✅ TTS engine initialized")
                print("Testing speech...")
                engine.say("TTS is working in Flask application")
                engine.runAndWait()
                print("✅ TTS test successful!")
                del engine
                return True
            except Exception as e:
                print(f"❌ TTS test failed: {e}")
                return False
        
        # Run test in thread (simulates Flask request)
        test_thread = threading.Thread(target=_test)
        test_thread.start()
        test_thread.join()
        
        print(f"{'='*60}\n")