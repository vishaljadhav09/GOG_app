package com.gog.app;

import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebView;
import androidx.core.splashscreen.SplashScreen;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

/**
 * Single-activity host for the Capacitor WebView that runs the game (web/ submodule, copied to www/).
 *
 * Native responsibilities, all deliberately small:
 *  - Android 12 SplashScreen API (cream background + owl, see styles.xml).
 *  - Landscape is locked in the manifest (sensorLandscape); here we make the window immersive: system bars
 *    hidden, a swipe from the edge shows them transiently. Layout under the notch is handled by the
 *    display-cutout theme item (shortEdges) plus the Capacitor SystemBars plugin, which hands the insets to
 *    the web page as env(safe-area-inset-*) / --safe-area-inset-* (the game uses viewport-fit=cover).
 *  - Keep the screen awake while the game is in the foreground (long narration, children tapping slowly).
 *  - Stop WebView audio/timers/animation while in the background (Capacitor keeps them running by default).
 */
public class MainActivity extends BridgeActivity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Must run before super.onCreate(): swaps AppTheme.NoActionBarLaunch for postSplashScreenTheme.
        SplashScreen.installSplashScreen(this);
        super.onCreate(savedInstanceState);

        WebView webView = getWebViewOrNull();
        if (webView != null) {
            // Allow audio (narration, SFX) to start without the WebView's own gesture rule; the game itself
            // still waits for a first tap ("Tap to hear ...") so browsers/WebViews that block it keep working.
            webView.getSettings().setMediaPlaybackRequiresUserGesture(false);
            // No edge glow, no long-press context menu / text selection on the canvas.
            webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
            webView.setHapticFeedbackEnabled(false);
            webView.setOnLongClickListener(v -> true);
        }

        applyImmersiveMode();
    }

    @Override
    public void onResume() {
        // Timers first, so the "resume"/appStateChange events Capacitor fires in super.onResume() are delivered.
        WebView webView = getWebViewOrNull();
        if (webView != null) {
            webView.resumeTimers();
            webView.onResume();
        }
        super.onResume();
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        applyImmersiveMode();
    }

    @Override
    public void onPause() {
        // super.onPause() first so the JS side still gets its "pause" notification before we freeze it.
        super.onPause();
        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        WebView webView = getWebViewOrNull();
        if (webView != null) {
            webView.onPause(); // also suspends media playback in the Chromium WebView
            webView.pauseTimers();
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        // The bars come back after a transient swipe, the notification shade, a dialog or a split-screen switch.
        if (hasFocus) {
            applyImmersiveMode();
        }
    }

    private WebView getWebViewOrNull() {
        return (getBridge() != null) ? getBridge().getWebView() : null;
    }

    private void applyImmersiveMode() {
        Window window = getWindow();
        WindowInsetsControllerCompat controller = WindowCompat.getInsetsController(window, window.getDecorView());
        controller.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        controller.hide(WindowInsetsCompat.Type.systemBars());
    }
}
